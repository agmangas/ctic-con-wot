import time, machine, sys, network, ulogging, gc
from uStorage import Storage
import uasyncio as asyncio
from network import WLAN
# from ping.ping import ping

from machine import I2C, ADC, WDT
from onewire.onewire import OneWire
from onewire.onewire import DS18X20
from AM2315.AM2315 import AM2315
from pysense.LIS2HH12 import LIS2HH12
from pysense.SI7006A20 import SI7006A20

from conf import configuration

VERSION = "0.0.1"
SLEEP_INTERVAL = 45000 # Milliseconds
WATCHDOG_TIMEOUT = 300000 # Milliseconds


class main(object):
    def __init__(self, logger):
        self.logger = logger
        self.watchdog = WDT(timeout=WATCHDOG_TIMEOUT)

        try:
            self.Air_Probe = DS18X20(OneWire(machine.Pin('P8'))) # Not in demo
        except Exception as ex:
            self.logger.error(ex)


        ###### STORED VALUES ######
        self.Temperature_Air = None

        self.restart = False

        self.rssi = 0

        ###### ASYNCHRONOUS TASKS ######
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.read_Air_Probe())
        # self.loop.create_task(self.read_Air_Humidity())
        self.loop.create_task(self.network_Status_Daemon())
        self.loop.create_task(self.memory_Garbage_Collector_Daemon())

        self.loop.create_task(self.write_to_influx())

        self.loop.run_forever()

        # self.mything.expose(server=server, broker=broker, ssid=ssid, ssid_password=ssid_password, port=1883)


    ###### UTILS ######

    async def network_Status_Daemon(self):
        config = configuration()
        wlan = WLAN(mode=WLAN.STA)

        while True:
            if wlan.isconnected():
                self.logger.info("Still connected to {}".format(config.WIFI_SSID))
                self.rssi = self.signal_percentage(wlan.joined_ap_info().rssi)
                await asyncio.sleep_ms(60000)
            else:
                try:
                    self.logger.warning("Reconnecting to {}".format(config.WIFI_SSID))
                    connect(config.WIFI_SSID, config.WIFI_PASSWORD)
                except:
                    pass

                await asyncio.sleep_ms(SLEEP_INTERVAL)


    async def memory_Garbage_Collector_Daemon(self):
        while True:
            F = gc.mem_free()/1024
            A = gc.mem_alloc()/1024
            T = F+A
            P = F/T*100

            self.logger.info('Total:{}KB | Free:{}KB ({:.2f}%)| Used:{}KB ({:.2f}%)'.format(T,F,P,A,100-P))

            gc.collect()
            self.watchdog.feed()
            await asyncio.sleep_ms(int(WATCHDOG_TIMEOUT/2))


    async def DS18b20_Read(self, sensor):
        sleep_time = 750
        temp = []
        try:
            for i in range(10):
                sensor.start_conversion()
                await asyncio.sleep_ms(sleep_time)
                temp.append(sensor.read_temp_async())

            res = self.median(temp)
            return res

        except Exception as ex:
            self.logger.error("Fallo al leer el sesor de temperatura: {}".format(ex))

    def median(self, list):
        l=list
        l.sort()
        n = len(l)
        median = 0
        if n % 2 == 0:
            median = (l[int(n/2)-1]+ l[int(n/2)] )/2
        else:
            median =l[int(n/2)]

        return median


    def signal_percentage(self, dbi):
        min = 30
        max = 100
        rng = max - min

        percent = 100 - ((abs(dbi) - min) * 100) / rng

        return percent


    ###### AIR TEMPERATURE AND HUMIDITY SENSORS ######
    async def read_Air_Probe(self):
        try:
            while True:
                self.Temperature_Air = await self.DS18b20_Read(sensor=self.Air_Probe)
                self.logger.info("Probe temperature: {}".format(self.Temperature_Air))
                await asyncio.sleep_ms(500)
        except Exception as ex:
            self.logger.error(ex)


    async def write_to_influx(self):

        import urequests as requests

        url="https://wotinflux.test.ctic.es/api/v2/write?org=wot&bucket=default-bucket&precision=ns"
        token="Token influx"
        parsed_data = "temperature,device=PycomGPy01 value={}"

        while self.Temperature_Air==None:
            await asyncio.sleep_ms(1000)

        while True:
            try:
                gc.collect()
                response = requests.request("POST", url, headers={"Authorization": token}, data=parsed_data.format(self.Temperature_Air))

                if response.status_code is not 204:
                    self.logger.error("Influx write failed with status code: {}".format(response.status_code))

            except Exception as ex:
                self.logger.error("Failed to write to Influx DB with error: {}".format(ex))

            await asyncio.sleep_ms(2000)


if __name__ == "__main__":

    config = configuration()
    logger = ulogging.getLogger(__name__)

    try:
        connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        storage = Storage()
        code = storage.get_Value("IP").split(".")[-1]

        my_main = main(logger=logger,)

    except Exception as ex:
        sys.print_exception(ex)
        f = open("error.log", "w")
        sys.print_exception(ex, f)
        time.sleep(5)
        f.close()
        wlan = network.WLAN()
        station = network.WLAN(mode=network.WLAN.STA)
        if not station.isconnected():
            machine.reset()
        else:
            time.sleep(30)
            machine.reset()

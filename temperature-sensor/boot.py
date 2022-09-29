import os, network, pycom, time, machine
from uStorage import Storage
from conf import configuration

pycom.heartbeat_on_boot(True)

DEVICE = os.uname().sysname
print(DEVICE)

storage = Storage()
config = configuration()

def signal_percentage(dbi):
    min = 30
    max = 100
    rng = max - min

    percent = 100 - ((abs(dbi) - min) * 100) / rng

    return percent

if "Py" in DEVICE:
    def connect(ssid, password, dns=None):
        print("Pycom connecting to {}...".format(ssid))

        wlan = network.WLAN()
        station = network.WLAN(mode=network.WLAN.STA)

        try:
            if station.isconnected():
                conf = station.ifconfig()
                storage.add_Update_Key(key="gateway", value=conf[2])
                storage.add_Update_Key(key="IP", value=conf[0])
                print ("already connected to {}".format(ssid))

            else:
                ssid_is_here = False
                best_network = None
                times=0

                while not ssid_is_here or times < 1:
                    for item in wlan.scan():
                        if item.ssid == ssid:
                            print(item)
                            ssid_is_here = True

                            if best_network is None:
                                best_network=item
                                print("Best found! {}".format(item.ssid))
                            elif signal_percentage(item.rssi) > signal_percentage(best_network.rssi):
                                best_network = item
                                print("Best found! {}".format(item.ssid))

                    time.sleep(2)
                    times += 1


                print("AP found, connecting...")

                station.connect(ssid=best_network.ssid, bssid=best_network.bssid, auth=(network.WLAN.WPA2, password))
                timer = time.time()

                while not station.isconnected():
                    if (time.time() - timer) < 20:
                        machine.idle()
                    else:
                        print("Could not connect, rebooting...")
                        machine.reset()

                time.sleep(2)

                if dns is not None:
                    conf = station.ifconfig()
                    newconf = (conf[0], conf[1], conf[2], dns)
                    station.ifconfig(newconf)

        except:
            pass

        conf = station.ifconfig()
        storage.add_Update_Key(key="gateway", value=conf[2])
        storage.add_Update_Key(key="IP", value=conf[0])
        print(conf)
        wlan.hostname(config.name.rsplit("-", 1)[0].format(config.location, config.family, config.number))
        return 0

elif "esp32" in DEVICE:
    import esp
    esp.osdebug(None)

    def connect(ssid, password, dns=None):
        print("ESP32 connecting to {}...".format(ssid))

        wlan = network.WLAN()
        station = network.WLAN(network.STA_IF)

        try:
            if station.isconnected():
                conf = station.ifconfig()
                storage.add_Update_Key(key="gateway", value=conf[2])
                storage.add_Update_Key(key="IP", value=conf[0])
                print ("already connected to {}".format(ssid))
                return 0
        except:
            pass

        station.active(True)

        ssid_is_here = False
        for item in wlan.scan():
            if ssid in str(item[0]):
                ssid_is_here = True
                break

        if not ssid_is_here:
            raise Exception("No AP found...")

        station.connect(ssid, password)

        while not station.isconnected(): pass

        if dns is not None:
            conf = station.ifconfig()
            newconf = (conf[0], conf[1], conf[2], dns)
            station.ifconfig(newconf)

        conf = station.ifconfig()
        storage.add_Update_Key(key="gateway", value=conf[2])
        storage.add_Update_Key(key="IP", value=conf[0])
        print(conf)
        return 0

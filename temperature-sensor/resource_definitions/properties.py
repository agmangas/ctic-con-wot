def property_declaration(exposed_thing):
    exposed_thing.add_property(
        name="air-temperature",
        description="A DS18b20 Temperature sensor, returns the current temperature of the air in Celsius.",
        type="number",
        unit="DEG_C")
    exposed_thing.add_property(
        name="air-hr",
        description="Pysense Humidity sensor, returns the current temperature of the air in %.",
        type="number",
        unit="PERCENT")
    exposed_thing.add_property(
        name="wifi-rssi",
        description="Indicates the signal strength of the connected WiFi",
        type="number",
        unit="PERCENT")

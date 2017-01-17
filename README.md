# honewell_thermostat
This library builds on the initial work by Brad Goodman.
It provides a clean python-ish API to the Honeywell Thermostat portal for controlling and monitoring their thermostats.
The HonewellThermostat class consists of several exposted methods as follows below

### __init__(username, password, device_id)
##### username
Honeywell username
##### password
Honeywell password
##### device_id
The device id of the honeywell thermostat
To obtain the device_id, visit the URL that you would normally use to access the thermostat.  It looks simething like:
https://mytotalconnectcomfort.com/portal/Device/Control/123456?page=1
The device id for this thermostat would be "123456"

### get_status()
Returns a json structure containing status of the thermostat

### set_cool(value, hold_time)
##### value
the value to change the cool point to.
##### hold_time
The amount of time (minutes) to hold this new temperature
(default is 15 minutes)

This method will put the thermostat into cooling mode and set the target temperature

### set_heat(value, hold_time)
##### value
the value to change the heat point to.
##### hold_time
the amount of time (minutes) to hold this new temperature
(default is 15 minutes)

This method will put the thermostat into heating mode and set the target temperature

### cancel_hold()
This method will return the system to the point before a hold was initiated

### cooler(value, hold_time)
##### value
The amount (in fahrenhThe amount (in fahrenheit) to lower the current temperature by
(default is 1 degree F.)
##### hold_time
The amount of time (minutes) to hold this new temperature
(default is 15 minutes)

This method will check the current room temperature and decrease it by the specified amount.
If the system is off, it will turn it to cool.
If it is already on, it will leave the thermostat in cool and merely lower the target temperature.

### warmer(value, hold_time)
##### value
The amount (in fahrenhThe amount (in fahrenheit) to raise the current temperature by
(default is 1 degree F.)
##### hold_time
The amount of time (minutes) to hold this new temperature
(default is 15 minutes)

This method will check the current room temperature and increase it by the specified amount.
If the system is off, it will turn it to heat.
If it is already on, it will leave the thermostat in heat and merely raise the target temperature.

### system_fan_on()
This method will turn the system fan on

### system_fan_auto()
This method will turn the system fan to auto

### system_off()
This method will turn the system off

### system_heat()
This method will turn the system to heat

### system_cool()
This method will turn the system to cool

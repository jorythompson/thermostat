# honewell_thermostat
This library builds on the initial work by Brad Goodman.
It provides a clean python-ish API to the Honeywell Thermostat portal for controlling and monitoring their thermostats.
The HonewellThermostat class consists of several exposted methods as follows below

### __init__(username, password, device_id)
##### username
honeywell username
##### password
honeywell password
##### device_id
the device id of the honeywell thermostat
To obtain the device_id, visit the URL that you would normally use to access the thermostat.  It looks simething like:
https://mytotalconnectcomfort.com/portal/Device/Control/123456?page=1
the device id for this thermostat would be "123456"

### get_status()
returns a json structure containing status of the thermostat

### set_cool(value, hold_time)
##### value
the value to change the cool point to.
##### hold_time
default is 15 minutes
the amount of time (minutes) to hold this new temperature

This method will turn on the thermostat (if necessary) and set the target temperature

### set_heat(value, hold_time)
##### value
the value to change the heat point to.
##### hold_time
default is 15 minutes
the amount of time (minutes) to hold this new temperature

This method will turn on the thermostat (if necessary) and set the target temperature

### cancel_hold()
This method will return the system to the point before a hold was initiated

### cooler(value, hold_time)
##### value
default is 1 degree F.
##### hold_time
default is 15 minutes
the amount of time (minutes) to hold this new temperature

This method will check the current room temperature and decrease it by the specified amount.
If the system is off, it will turn it to cool.
If it is already on, it will leave the status (heating or cooling) alone and merely lower the target temperature.

### warmer(value, hold_time)
##### value
default is 1 degree F.
##### hold_time
default is 15 minutes
the amount of time (minutes) to hold this new temperature

This method will check the current room temperature and increase it by the specified amount.
If the system is off, it will turn it to heat.
If it is already on, it will leave the status (heating or cooling) alone and merely lower the target temperature.

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

### system_auto()
This method will turn the system to auto

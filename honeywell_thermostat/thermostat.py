# Originally by Brad Goodman
# http://www.bradgoodman.com/
# brad@bradgoodman.com

import urllib
import json
import datetime
import re
import time
import httplib
import logging.config
import inspect
import os
import ConfigParser
import pprint


def get_logger_name():
    stack = inspect.stack()
    file_name = os.path.basename(__file__).replace(".py", "")
    the_function = stack[1][3]
    try:
        if len(stack[1][0].f_locals) > 0:
            the_class = str(stack[1][0].f_locals["self"].__class__.__name__) + "."
        else:
            the_class = ""
    except:
        the_class = ""
    return file_name + "." + the_class + the_function


class SystemState:
    def __init__(self):
        pass

    heat = 1
    off = 2
    cool = 3
    auto = 4
    unknown = 5

    @staticmethod
    def is_valid(val):
        if val in range(SystemState.heat, SystemState.auto):
            return True
        return False

    @staticmethod
    def str_value(val):
        if val == SystemState.heat:
            return "heat"
        elif val == SystemState.off:
            return "off"
        elif val == SystemState.cool:
            return "cool"
        elif val == SystemState.auto:
            return "auto"
        else:
            return str(val) + " is unknown"

    @staticmethod
    def on_off(val):
        if val == 0:
            return "off"
        elif val == 1:
            return "on"
        else:
            raise RuntimeError(str(val) + " is not a valid on/off value")


class Honeywell:
    COOKIE = re.compile('\s*([^=]+)\s*=\s*([^;]*)\s*')

    def __init__(self, username, password, device_id):
        self.username = username
        self.password = password
        self.device_id = device_id
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Encoding": "sdch",
                   "Host": "mytotalconnectcomfort.com",
                   "DNT": "1",
                   "Origin": "https://mytotalconnectcomfort.com/portal",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"
                   }
        conn = httplib.HTTPSConnection("mytotalconnectcomfort.com")
        conn.request("GET", "/portal/", None, headers)
        r0 = conn.getresponse()
        cookie_jar = Honeywell._client_cookies(r0.getheader("set-cookie"))
        params = urllib.urlencode({"timeOffset": "240",
                                   "UserName": self.username,
                                   "Password": self.password,
                                   "RememberMe": "false"})
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Encoding": "sdch",
                   "Host": "mytotalconnectcomfort.com",
                   "DNT": "1",
                   "Origin": "https://mytotalconnectcomfort.com/portal/",
                   "Cookie": Honeywell._export_cookie_jar(cookie_jar),
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36"
                   }
        conn = httplib.HTTPSConnection("mytotalconnectcomfort.com")
        conn.request("POST", "/portal/", params, headers)
        r1 = conn.getresponse()
        cookie_jar = Honeywell._client_cookies(r1.getheader("set-cookie"))
        self.cookie = Honeywell._export_cookie_jar(cookie_jar)
        location = r1.getheader("Location")

        if location is None or r1.status != 302:
            raise RuntimeError("ErrorNever got redirect on initial login  status={0} {1}".format(r1.status, r1.reason))

    @staticmethod
    def _export_cookie_jar(jar):
        s = ""
        for x in jar:
            s += '%s=%s;' % (x, jar[x])
        return s

    @staticmethod
    def _client_cookies(cookie_str):
        container = {}
        tokens = re.split(';|,', cookie_str)
        for t in tokens:
            k = None
            v = None
            m = Honeywell.COOKIE.search(t)
            if m:
                k = m.group(1)
                v = m.group(2)
                if k in ['path', 'Path', 'HttpOnly']:
                    k = None
                    v = None
            if k:
                container[k] = v
        return container

    def _send_payload(self, payload_in):
        logger = logging.getLogger(get_logger_name())
        headers = {
            "Accept": 'application/json; q=0.01',
            "DNT": "1",
            "Accept-Encoding": "gzip,deflate,sdch",
            'Content-Type': 'application/json; charset=UTF-8',
            "Cache-Control": "max-age=0",
            "Accept-Language": "en-US,en,q=0.8",
            "Connection": "keep-alive",
            "Host": "mytotalconnectcomfort.com",
            "Referer": "https://mytotalconnectcomfort.com/portal/",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36",
            'Referer': "/TotalConnectComfort/Device/CheckDataSession/" + str(self.device_id),
            "Cookie": self.cookie
        }
        payload = {
            "CoolNextPeriod": None,
            "HeatNextPeriod": None,
            "CoolSetpoint": None,
            "HeatSetpoint": None,
            "StatusCool": 0,
            "StatusHeat": 0,
            "DeviceID": self.device_id,
            "FanMode": None,
            "SystemSwitch": None
        }
        payload.update(payload_in)
        location = "/portal/Device/SubmitControlScreenChanges"
        raw_jason = json.dumps(payload)
        conn = httplib.HTTPSConnection("mytotalconnectcomfort.com")
        conn.request("POST", location, raw_jason, headers)
        r4 = conn.getresponse()
        if r4.status != 200:
            raise RuntimeError("Error Didn't get 200 status on R4 status={0} {1}".format(r4.status, r4.reason))
        else:
            logger.debug("Success in configuring thermostat!")

    @staticmethod
    def _hold_time(hold_time):
        return hold_time / 15

    def _set_system(self, value):
        if SystemState.is_valid(value):
            self._send_payload({
                "SystemSwitch": value})

    def get_status(self):
        logger = logging.getLogger(get_logger_name())
        code = str(self.device_id)
        t = datetime.datetime.now()
        utc_seconds = (time.mktime(t.timetuple()))
        utc_seconds = int(utc_seconds * 1000)
        location = "/portal/Device/CheckDataSession/" + code + "?_=" + str(utc_seconds)
        headers = {
            "Accept": "*/*",
            "DNT": "1",
            "Accept-Encoding": "plain",
            "Cache-Control": "max-age=0",
            "Accept-Language": "en-US,en,q=0.8",
            "Connection": "keep-alive",
            "Host": "mytotalconnectcomfort.com",
            "Referer": "https://mytotalconnectcomfort.com/portal/",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36",
            "Cookie": self.cookie
        }
        conn = httplib.HTTPSConnection("mytotalconnectcomfort.com")
        conn.request("GET", location, None, headers)
        r3 = conn.getresponse()
        if r3.status != 200:
            raise RuntimeError("Error Didn't get 200 status on R3 status={0} {1}".format(r3.status, r3.reason))
        j = json.loads(r3.read())
        logger.debug("Indoor Temperature:%3.2f", j['latestData']['uiData']["DispTemperature"])
        logger.debug("Indoor Humidity:%3.2f", j['latestData']['uiData']["IndoorHumidity"])
        logger.debug("Cool Setpoint:%3.2f", j['latestData']['uiData']["CoolSetpoint"])
        logger.debug("Heat Setpoint:%3.2f", j['latestData']['uiData']["HeatSetpoint"])
        logger.debug("Hold Until:%d", j['latestData']['uiData']["TemporaryHoldUntilTime"])
        logger.debug("Status Cool:%s", SystemState.on_off(j['latestData']['uiData']["StatusCool"]))
        logger.debug("Status Heat:%s", SystemState.on_off(j['latestData']['uiData']["StatusHeat"]))
        logger.debug("System Status:%s", SystemState.str_value(j['latestData']['uiData']["SystemSwitchPosition"]))
        logger.debug("Status Fan:%s", SystemState.on_off(j['latestData']['fanData']["fanMode"]))
        return j

    def set_cool(self, value, hold_time, switch_position=None):
        # statusCool and statusHeat 1 for hold, 0 for regular
        hold = 1
        if switch_position is None:
            status = self.get_status()
            switch_position = status['latestData']['uiData']["SystemSwitchPosition"]
        if switch_position is not SystemState.cool:
            self.system_cool()
        hold_time = Honeywell._hold_time(hold_time)
        self._send_payload({
            "CoolNextPeriod": hold_time,
            "CoolSetpoint": value,
            "HeatNextPeriod": hold_time,
            "StatusCool": hold,
            "StatusHeat": hold})

    def set_heat(self, value, hold_time, switch_position=None):
        # statusCool and statusHeat 1 for hold, 0 for regular
        hold = 1
        if switch_position is None:
            status = self.get_status()
            switch_position = status['latestData']['uiData']["SystemSwitchPosition"]
        if switch_position is not SystemState.heat:
            self.system_heat()
        hold_time = Honeywell._hold_time(hold_time)
        self._send_payload({
            "CoolNextPeriod": hold_time,
            "HeatSetpoint": value,
            "HeatNextPeriod": hold_time,
            "StatusCool": hold,
            "StatusHeat": hold})

    def cancel_hold(self):
        self._send_payload({})

    def cooler(self, value=1, hold_time=15):
        logger = logging.getLogger(get_logger_name())
        status = self.get_status()
        switch_position = status['latestData']['uiData']["SystemSwitchPosition"]
        current_temp = status['latestData']['uiData']["DispTemperature"]
        target_temp = current_temp - value
        logger.debug("changing the temperature from %3.2f to %3.2f", current_temp, target_temp)
        if switch_position != SystemState.cool and switch_position != SystemState.heat:
            self.system_cool()
            switch_position = SystemState.cool
        if switch_position == SystemState.cool:
            self.set_cool(target_temp, hold_time, switch_position)
        else:
            self.set_heat(target_temp, hold_time, switch_position)

    def warmer(self, value=1, hold_time=15):
        logger = logging.getLogger(get_logger_name())
        status = self.get_status()
        switch_position = status['latestData']['uiData']["SystemSwitchPosition"]
        current_temp = status['latestData']['uiData']["DispTemperature"]
        target_temp = current_temp + value
        logger.debug("changing the temperature from %3.2f to %3.2f", current_temp, target_temp)
        if switch_position != SystemState.cool and switch_position != SystemState.heat:
            self.system_heat()
            switch_position = SystemState.heat
        if switch_position == SystemState.cool:
            self.set_cool(target_temp, hold_time, switch_position)
        else:
            self.set_heat(target_temp, hold_time, switch_position)

    def system_fan_on(self):
        self._send_payload({"FanMode": 1})

    def system_fan_auto(self):
        self._send_payload({"FanMode": 0})

    def system_off(self):
        logger = logging.getLogger(get_logger_name())
        logger.debug("turning system off")
        self._set_system(SystemState.off)

    def system_heat(self):
        logger = logging.getLogger(get_logger_name())
        logger.debug("turning system to heat")
        self._set_system(SystemState.heat)

    def system_cool(self):
        logger = logging.getLogger(get_logger_name())
        logger.debug("turning system to cool")
        self._set_system(SystemState.cool)

    def system_auto(self):
        hold = 1
        logger = logging.getLogger(get_logger_name())
        logger.debug("turning system to auto")
        self._send_payload({
            "StatusCool": hold,
            "StatusHeat": hold,
            "SystemSwitch": SystemState.auto})


def main():
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger(get_logger_name())
    config = ConfigParser.ConfigParser()
    config.read("thermostats.cfg")
    username = config.get("honeywell", "username")
    password = config.get("honeywell", "password")
    thermostats = eval(config.get("system", "thermostats"))
    honeywell = Honeywell(username, password, thermostats["living room"])
    honeywell.system_off()
    # honeywell.cooler(5, 30)
    # honeywell.warmer(5, 30)
    # honeywell.cooler(5, 30)
    # honeywell.set_cool(85, 30)
    # honeywell.set_heat(80, 30)
    # honeywell.system_auto()
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(honeywell.get_status())
    logger.info("Done!")

if __name__ == '__main__':
    main()

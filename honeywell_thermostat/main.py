from thermostat import get_logger_name, Honeywell
import argparse
import logging.config
import pprint

'''
curl -i -k -H "Content-Type: application/json" -X POST -d '{"thermostat":"living room"}' https://localhost:5000/thermostat/off
curl -i -H "Content-Type: application/json" -X POST -d '{"thermostat":"living oom"}' http://localhost:5000/thermostat/on
'''


def main():
    parser = argparse.ArgumentParser(description="test stub for thermostat.Honeywell",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--username",
                        required=True,
                        help="username required by Honeywell web site")
    parser.add_argument("--password",
                        required=True,
                        help="password required by Honeywell web site")
    parser.add_argument("--unit-id",
                        required=True,
                        type=int,
                        help="the unit id from the Honeywell web site")
    subparsers = parser.add_subparsers(help='additional parameters for target-temp')
    cool_parser = subparsers.add_parser("set-cool",
                                        help="set the cool target temperature")
    cool_parser.add_argument("--hold-time",
                             type=int,
                             required=True,
                             help="the hold time for this command")
    cool_parser.add_argument("--target-temp",
                             type=int,
                             required=True,
                             help="the requested temperature")
    cool_parser.set_defaults(action="set-cool")
    heat_parser = subparsers.add_parser("set-heat",
                                        help="set the heat target temperature")
    heat_parser.add_argument("--hold-time",
                             type=int,
                             required=True,
                             help="the hold time for this command")
    heat_parser.add_argument("--target-temp",
                             type=int,
                             required=True,
                             help="the requested temperature")
    heat_parser.set_defaults(action="set-heat")
    cooler_parser = subparsers.add_parser("cooler",
                                          help="reduce the temperature by a specified amount")
    cooler_parser.add_argument("--amount",
                               type=int,
                               required=True,
                               help="amount of temperature to drop")
    cooler_parser.add_argument("--hold-time",
                               type=int,
                               required=True,
                               help="the hold time for this command")
    cooler_parser.set_defaults(action="cooler")
    warmer_parser = subparsers.add_parser("warmer",
                                          help="increase the temperature by a specified amount")
    warmer_parser.add_argument("--amount",
                               type=int,
                               required=True,
                               help="amount of temperature to raise")
    warmer_parser.add_argument("--hold-time",
                               type=int,
                               required=True,
                               help="the hold time for this command")
    warmer_parser.set_defaults(action="warmer")
    auto_parser = subparsers.add_parser("system-auto",
                                        help="turns the thermostat to auto")
    auto_parser.set_defaults(action="system-auto")
    off_parser = subparsers.add_parser("system-off",
                                       help="turns the thermostat off")
    off_parser.set_defaults(action="system-off")
    status_parser = subparsers.add_parser("status",
                                          help="gets the status of the thermostat")
    status_parser.set_defaults(action="status")
    args = parser.parse_args()
    logger = logging.getLogger(get_logger_name())
    logger.debug("starting the test")
    honeywell = Honeywell(args.username, args.password, args.unit_id)
    pp = pprint.PrettyPrinter(indent=2)

    if args.action == "cooler":
        honeywell.cooler(args.amount, args.hold_time)
        pp.pprint(honeywell.get_status())
    elif args.action == "warmer":
        honeywell.warmer(args.amount, args.hold_time)
        pp.pprint(honeywell.get_status())
    elif args.action == "system-auto":
        honeywell.system_auto()
        pp.pprint(honeywell.get_status())
    elif args.action == "system-off":
        honeywell.system_off()
        pp.pprint(honeywell.get_status())
    elif args.action == "status":
        pp.pprint(honeywell.get_status())
    elif args.action == "set-cool":
        pass
    elif args.action == "set-heat":
        pass


if __name__ == "__main__":
    main()

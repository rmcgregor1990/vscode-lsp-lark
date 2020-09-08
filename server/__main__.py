"""Main entry point for starting the server"""

import argparse
import logging

from .server import json_server

# setup python logging to pygls.log
logging.basicConfig(filename="pygls.log", level=logging.DEBUG, filemode="w")


def main():
    parser = argparse.ArgumentParser(description="lark json server example")

    parser.add_argument(
        "--tcp", action="store_true",
        help="Use TCP server instead of stdio"
    )
    parser.add_argument(
        "--host", default="127.0.0.1",
        help="Bind to this address"
    )
    parser.add_argument(
        "--port", type=int, default=2087,
        help="Bind to this port"
    )
    args = parser.parse_args()

    if args.tcp:
        json_server.start_tcp(args.host, args.port)
    else:
        json_server.start_io()


if __name__ == '__main__':
    main()

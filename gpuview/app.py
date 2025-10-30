#!/usr/bin/env python

"""
Web API of gpuview.

@author Fitsum Gaim
@url https://github.com/fgaim
"""

import json
import os
from datetime import datetime
from typing import Any

from bottle import TEMPLATE_PATH, Bottle, response, template

from . import core, demo
from . import service as service_manager
from . import utils

app = Bottle()
abs_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_path, "views")
TEMPLATE_PATH.insert(0, abs_views_path)

EXCLUDE_SELF = False  # Do not report to `/gpustat` calls.
DEMO_MODE = False  # Run with fake data.


@app.route("/")
def index() -> str:
    if DEMO_MODE:
        gpustats = demo.get_demo_gpustats()
    else:
        gpustats = core.all_gpustats()
    now = datetime.now().strftime("Updated at %Y-%m-%d %H-%M-%S")
    return template("index", gpustats=gpustats, update_time=now)


@app.route("/gpustat", methods=["GET"])  # deprecated alias
@app.route("/api/gpustat/self", methods=["GET"])
def report_gpustat() -> str:
    """
    Returns the gpustat of this host.
        See `exclude-self` option of `gpuview run`.
        Available at both /gpustat (legacy) and /api/gpustat/self (RESTful).
    """

    def _date_handler(obj: Any) -> str:
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        else:
            raise TypeError(type(obj))

    response.content_type = "application/json"
    if DEMO_MODE:
        resp = demo.get_demo_local_gpustat()
    elif EXCLUDE_SELF:
        resp = {"error": "Excluded self!"}
    else:
        resp = core.my_gpustat()
    return json.dumps(resp, default=_date_handler)


@app.route("/api/gpustat/all", methods=["GET"])
def api_gpustat_all() -> str:
    """
    Returns aggregated gpustats for all hosts (same data as index page).
    Used by frontend for live updates.
    """

    def _date_handler(obj: Any) -> str:
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        else:
            raise TypeError(type(obj))

    response.content_type = "application/json"
    if DEMO_MODE:
        resp = demo.get_demo_gpustats()
    else:
        resp = core.all_gpustats()
    return json.dumps(resp, default=_date_handler)


def main() -> None:
    parser = utils.arg_parser()
    args = parser.parse_args()

    if "run" == args.action:
        core.safe_zone(args.safe_zone)
        global EXCLUDE_SELF, DEMO_MODE
        EXCLUDE_SELF = args.exclude_self
        DEMO_MODE = args.demo
        app.run(host=args.host, port=args.port, debug=args.debug)

    elif "service" == args.action:
        service_command = args.service_command or "start"
        if service_command == "start":
            service_manager.start(args)
        elif service_command == "status":
            service_manager.status(args)
        elif service_command == "stop":
            service_manager.stop(args)
        elif service_command == "logs":
            service_manager.logs(args)
        elif service_command == "delete":
            service_manager.delete(args)

    elif "add" == args.action:
        core.add_host(args.url, args.name)
    elif "remove" == args.action:
        core.remove_host(args.url)
    elif "hosts" == args.action:
        core.print_hosts()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

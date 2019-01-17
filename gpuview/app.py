#!/usr/bin/env python

"""
Web API of gpuview.

@author Fitsum Gaim
@url https://github.com/fgaim
"""

import os
import json
from datetime import datetime

from bottle import Bottle, TEMPLATE_PATH, template, response

from .utils import cmd_args_parser
from .core import my_gpustat, all_gpustats, add_host, remove_host, safe_zone, print_hosts


app = Bottle()
abs_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_path, 'views')
TEMPLATE_PATH.insert(0, abs_views_path)

EXCLUDE_SELF = False  # Do not report to `/gpustat` calls.


@app.route('/')
def index():
    gpustats = all_gpustats()
    now = datetime.now().strftime('Updated at %Y-%m-%d %H-%M-%S')
    return template('index', gpustats=gpustats, update_time=now)


@app.route('/gpustat', methods=['GET'])
def report_gpustat():
    """
    Returns the gpustat of this host.
        See `exclude-self` option of `gpuview start`.
    """

    def _date_handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError(type(obj))

    response.content_type = 'application/json'
    if EXCLUDE_SELF:
        resp = {'error': 'Excluded self!'}
    else:
        resp = my_gpustat()
    return json.dumps(resp, default=_date_handler)


def main():
    parser = cmd_args_parser()
    args = parser.parse_args()

    if 'start' == args.action:
        safe_zone(args.safe_zone)
        global EXCLUDE_SELF
        EXCLUDE_SELF = args.exclude_self
        app.run(host=args.host, port=args.port, debug=args.debug)
    elif 'add' == args.action:
        add_host(args.url, args.name)
    elif 'remove' == args.action:
        remove_host(args.url)
    elif 'hosts' == args.action:
        print_hosts()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

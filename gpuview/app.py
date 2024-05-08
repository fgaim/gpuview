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

from . import utils
from . import core


app = Bottle()
abs_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_path, 'views')
TEMPLATE_PATH.insert(0, abs_views_path)

EXCLUDE_SELF = False  # Do not report to `/gpustat` calls.

REFRESH_TIME = 5

@app.route('/')
def index():
    return template('index', update_time=REFRESH_TIME)

@app.route('/update', method='GET')
def update():
    gpustats = core.all_gpustats(REFRESH_TIME)
    now = datetime.now().strftime('Updated at %Y-%m-%d %H-%M-%S')
    return template('body', gpustats=gpustats, refresh_time=now)

@app.route('/gpustat', method='GET')
def report_gpustat():
    """
    Returns the gpustat of this host.
        See `exclude-self` option of `gpuview run`.
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
        resp = core.my_gpustat()
    return json.dumps(resp, default=_date_handler)


def main():
    parser = utils.arg_parser()
    args = parser.parse_args()

    if 'run' == args.action:
        core.safe_zone(args.safe_zone)
        global EXCLUDE_SELF, REFRESH_TIME
        EXCLUDE_SELF = args.exclude_self
        REFRESH_TIME = args.refresh_time
        app.run(host=args.host, port=args.port, debug=args.debug)
    elif 'service' == args.action:
        core.install_service(host=args.host,
                             port=args.port,
                             safe_zone=args.safe_zone,
                             exclude_self=args.exclude_self,
                             refresh_time=args.refresh_time)
    elif 'add' == args.action:
        core.add_host(args.url, args.name)
    elif 'remove' == args.action:
        core.remove_host(args.url)
    elif 'hosts' == args.action:
        core.print_hosts()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

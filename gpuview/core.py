"""
Core functions of gpuview.

@author Fitsum Gaim
@url https://github.com/fgaim
"""

import os
import json
import subprocess
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


ABS_PATH = os.path.dirname(os.path.realpath(__file__))
HOSTS_DB = os.path.join(ABS_PATH, 'gpuhosts.db')
SAFE_ZONE = False  # Safe to report all details.


def safe_zone(safe=False):
    global SAFE_ZONE
    SAFE_ZONE = safe


def my_gpustat():
    """
    Returns a [safe] version of gpustat for this host.
        # See `--safe-zone` option of `gpuview start`.
        # Omit sensitive details, eg. uuid, username, and processes.
        # Set color flag based on gpu temperature:
            # bg-warning, bg-danger, bg-success, bg-primary

    Returns:
        dict: gpustat
    """

    try:
        from gpustat import GPUStatCollection
        stat = GPUStatCollection.new_query().jsonify()
        delete_list = []
        for gpu_id, gpu in enumerate(stat['gpus']):
            if type(gpu['processes']) is str:
                delete_list.append(gpu_id)
                continue
            gpu['memory'] = round(float(gpu['memory.used']) /
                                  float(gpu['memory.total']) * 100)
            if SAFE_ZONE:
                gpu['users'] = len(set([p['username']
                                        for p in gpu['processes']]))
                user_process = [
                    '%s(%s,%sM)' % (p['username'],
                                    p['command'], p['gpu_memory_usage'])
                    for p in gpu['processes']
                ]
                gpu['user_processes'] = ' '.join(user_process)
            else:
                gpu['users'] = len(set([p['username']
                                        for p in gpu['processes']]))
                processes = len(gpu['processes'])
                gpu['user_processes'] = '%s/%s' % (gpu['users'], processes)
                gpu.pop('processes', None)
                gpu.pop("uuid", None)
                gpu.pop("query_time", None)

            gpu['flag'] = 'bg-primary'
            if gpu['temperature.gpu'] > 75:
                gpu['flag'] = 'bg-danger'
            elif gpu['temperature.gpu'] > 50:
                gpu['flag'] = 'bg-warning'
            elif gpu['temperature.gpu'] > 25:
                gpu['flag'] = 'bg-success'

        if delete_list:
            for gpu_id in delete_list:
                stat['gpus'].pop(gpu_id)

        return stat
    except Exception as e:
        return {'error': '%s!' % getattr(e, 'message', str(e))}


def all_gpustats():
    """
    Aggregates the gpustats of all registered hosts and this host.

    Returns:
        list: pustats of hosts
    """

    gpustats = []
    mystat = my_gpustat()
    if 'gpus' in mystat:
        gpustats.append(mystat)

    hosts = load_hosts()
    for url in hosts:
        try:
            raw_resp = urlopen(url + '/gpustat')
            gpustat = json.loads(raw_resp.read())
            raw_resp.close()
            if not gpustat or 'gpus' not in gpustat:
                continue
            if hosts[url] != url:
                gpustat['hostname'] = hosts[url]
            gpustats.append(gpustat)
        except Exception as e:
            print('Error: %s getting gpustat from %s' %
                  (getattr(e, 'message', str(e)), url))

    try:
        sorted_gpustats = sorted(gpustats, key=lambda g: g['hostname'])
        if sorted_gpustats is not None:
            return sorted_gpustats
    except Exception as e:
        print("Error: %s" % getattr(e, 'message', str(e)))
    return gpustats


def load_hosts():
    """
    Loads the list of registered gpu nodes from file.

    Returns:
        dict: {url: name, ... }
    """

    hosts = {}
    if not os.path.exists(HOSTS_DB):
        print("There are no registered hosts! Use `gpuview add` first.")
        return hosts

    for line in open(HOSTS_DB, 'r'):
        try:
            name, url = line.strip().split('\t')
            hosts[url] = name
        except Exception as e:
            print('Error: %s loading host: %s!' %
                  (getattr(e, 'message', str(e)), line))
    return hosts


def save_hosts(hosts):
    with open(HOSTS_DB, 'w') as f:
        for url in hosts:
            f.write('%s\t%s\n' % (hosts[url], url))


def add_host(url, name=None):
    url = url.strip().strip('/')
    if name is None:
        name = url
    hosts = load_hosts()
    hosts[url] = name
    save_hosts(hosts)
    print('Successfully added host!')


def remove_host(url):
    hosts = load_hosts()
    if hosts.pop(url, None):
        save_hosts(hosts)
        print("Removed host: %s!" % url)
    else:
        print("Couldn't find host: %s!" % url)


def print_hosts():
    hosts = load_hosts()
    if len(hosts):
        hosts = sorted(hosts.items(), key=lambda g: g[1])
        print('#   Name\tURL')
        for idx, host in enumerate(hosts):
            print('%02d. %s\t%s' % (idx+1, host[1], host[0]))


def install_service(host=None, port=None,
                    safe_zone=False, exclude_self=False):
    arg = ''
    if host is not None:
        arg += '--host %s ' % host
    if port is not None:
        arg += '--port %s ' % port
    if safe_zone:
        arg += '--safe-zone '
    if exclude_self:
        arg += '--exclude-self '
    script = os.path.join(ABS_PATH, 'service.sh')
    subprocess.call('{} "{}"'.format(script, arg.strip()), shell=True)

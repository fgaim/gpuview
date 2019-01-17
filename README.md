gpuview
=======

[![LICENSE](https://img.shields.io/github/license/fgaim/gpuview.svg)](https://github.com/fgaim/gpuview/blob/master/LICENSE)
![GitHub issues](https://img.shields.io/github/issues/fgaim/gpuview.svg)
[![PyPI](https://img.shields.io/pypi/v/gpuview.svg)](https://pypi.org/project/gpuview/)
[![CircleCI](https://circleci.com/gh/fgaim/gpuview.svg?style=shield)](https://circleci.com/gh/fgaim/gpuview)


GPU is an expensive resource, and deep learning practitioners have to monitor the
health and usage of their GPUs, such as the temperature, memory, utilization, and the users. 
This can be done with tools like `nvidia-smi` and `gpustat` from the terminal or command-line.
Often times, however, it is not convenient to `ssh` into servers to just check the GPU status. 
`gpuview` is meant to mitigate this by running a lightweight web dashboard on top of 
[`gpustat`][repo_gpustat].  

With `gpuview` one can monitor GPUs on the go, though a web browser. Moreover, **multiple GPU servers** 
can be registered into one `gpuview` dashboard and all stats are aggregated and accessible from one place.


Thumbnail view of GPUs across multiple servers.  

![Screenshot of gpuview](https://github.com/fgaim/gpuview/blob/master/imgs/dash-1.png)


Setup
-----

Python is required,`gpuview` has been tested with both 2.7 and 3 versions.

Install from [PyPI][pypi_gpuview]:

```
$ pip install gpuview
```

[or] Install directly from repo:

```
$ pip install git+https://github.com/fgaim/gpuview.git@master
```

> `gpuview` installs the latest version of `gpustat` from `pypi`, therefore, its commands are available 
from the terminal.



Usage
-----

Once `gpuview` is installed, it can be started as follows:
```
$ gpuview start --safe-zone
```
This will start the dasboard at `http://0.0.0.0:9988`.


By default, `gpuview` listens to IP `0.0.0.0` and port `9988`, but these can be changed using `--host` and `--port`. The `safe-zone` option implies reporting all detials including user names, but it can be turned off for security reasons.


Execute `gpuview -h` to see runtime options.

* `start`              : Start dashboard server
  * `--host`           : Name or IP address of host (default: 0.0.0.0)
  * `--port`           : Port number to listen to (default: 9988)
  * `--safe-zone`      : Safe to report all details including user names
  * `--exclude-self`   : Don't report to others but to self dashboard
  * `-d`, `--debug`    : Run server in debug mode (for developers)
* `add`                : Add a GPU host to dashboard
  * `--url`            : URL of host [IP:Port], eg. X.X.X.X:9988
  * `--name`           : Optional readable name for the host, eg. Node101
* `remove`             : Remove a registered host from dashboard
  * `--url`            : URL of host to remove, eg. X.X.X.X:9988
* `-v`, `--version`    : Print versions of `gpuview` and `gpustat`
* `-h`, `--help`       : Print help for command-line options


### Run as Service

To permanently run `gpuview` it needs to be started as a background service. This can be done using `nohup` and `&` as follows:

```
$ sudo nohup gpuview start --safe-zone &
```

A better way of handling this will be implemented in future, see [todo](todo).


### Monitoring multiple hosts

To aggregate the stats of multiple machines, they can be registered to one dashboard using their address and the port number running `gpustat`.

Add a host as follows:
```
gpuview add --url <ip:port> --name <name>
```

Remove a registered host as follows:
```
gpuview remove --url <ip:port> --name <name>
```

> Note: `gpuview` service should be started in all hosts that need to be monitored.

> Tip: `gpuview` can be setup on a none GPU machine (for example, a laptop) to monitor remote servers. 


etc
---

Helpful tips related to the underlying performance are available at the [`gpustat`][repo_gpustat] repo.


For the sake of simplicity, `gpuview` does not have a user authentication in place. As a security measure,
it does not report sensitive details such as user names by default. This can be changed if the service is 
running in a trusted network, using the `--safe-zone` option to report all details. 


The `--exclude-self` option of the start command can be used to prevent other dashboards from getting stats of the current machine. This way the stats are shown only on the host's own dashboard.


Detailed view of GPUs across multiple servers.  

![Screenshot of gpuview](https://github.com/fgaim/gpuview/blob/master/imgs/dash-1.png)


License
-------

[MIT License](LICENSE)



[repo_gpustat]: https://github.com/wookayin/gpustat
[pypi_gpuview]: https://pypi.python.org/pypi/gpuview

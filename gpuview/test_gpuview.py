"""
Unit and integration tests for gpuview
"""


def test_my_gpustat():
    from .core import my_gpustat
    stat = my_gpustat()
    assert stat is not None
    assert isinstance(stat, dict)


def test_all_gpustats():
    from .core import all_gpustats
    stats = all_gpustats()
    assert stats is not None
    assert isinstance(stats, list)


def test_hosts_db():
    from .core import load_hosts, add_host, remove_host

    dummy_host = 'dummy.host'
    add_host(dummy_host)

    hosts = load_hosts()
    assert dummy_host in hosts

    remove_host(dummy_host)
    hosts = load_hosts()
    assert dummy_host not in hosts


def test_arg_parser():
    from .utils import arg_parser

    parser = arg_parser()
    assert parser is not None
    # import pytest
    # with pytest.raises(Exception):
    #    parser.parse_args()

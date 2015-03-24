import inspect
import sys

from common.ssh import run_ssh_cmd as _run_ssh_cmd
from common.config import CONFIG
from common.validate import verify


def check_fuel_cpu(con_info):
    '''Checks CPU configuration on host.'''

    cmd = 'lscpu | grep "^CPU(s):"'
    stdout, stderr = _run_ssh_cmd(cmd, con_info)

    if stderr != '':
        raise IOError('Error while checking CPU: %s' % stderr)

    cores = int(stdout.split()[-1].strip())

    verify(cores <= CONFIG['hw_fuel_cpu_core_number'],
           'CPU has more cores (%d) than recommended.' % (cores,)
           )


def _get_size_mb(size, units):
    '''Returns size in MB.

    Parameters:
        - size: size in units
        - units: unit of measurement
    '''

    units = units.lower()

    if units == 'kb':
        div_coef = 1024
    elif units == 'mb':
        div_coef = 1
    elif units == 'gb':
        div_coef = 1.0/1024
    elif units == 'b':
        div_coef = 1024000

    return float(size) / div_coef


def check_fuel_ram(con_info):
    '''Checks RAM size on host.'''

    cmd = 'grep MemTotal /proc/meminfo'
    stdout, stderr = _run_ssh_cmd(cmd, con_info)

    sz = stdout.split()[-2:]

    mem_size = _get_size_mb(sz[0], sz[1])

    verify(mem_size <= CONFIG['hw_fuel_ram_size_mb'],
           'RAM size (%s %s) is larger than recommended value.'
           % (sz[0], sz[1])
           )


def check_fuel_capacity(con_info):
    '''Checks capacity of network card.'''

    cmd = 'ethtool eth0 | grep %dbaseT' % CONFIG['hw_fuel_network_capacity']

    stdout, stderr = _run_ssh_cmd(cmd, con_info)

    verify(stdout != '',
           'Network card does not provide recommended capacity (%d baseT).'
           % (CONFIG['hw_default_network_capacity'],))


def check_fuel_ipmi_access(con_info):
    '''Checks IPMI access on host.'''

    cmd = 'ipmitool sel list'
    err_match = 'Could not open device'

    stdout, stderr = _run_ssh_cmd(cmd, con_info)

    verify(err_match not in stderr,
           'IPMI is not configured on host %s' % con_info["host"])

CHECKS = [check[1] for check in inspect.getmembers(sys.modules[__name__],
                                                   inspect.isfunction)
          if check[0].startswith('check')
          ]

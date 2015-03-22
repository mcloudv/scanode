# Common functions for SSH

from paramiko import SSHClient
from paramiko import AutoAddPolicy


def run_ssh_cmd(cmd, con_info):
    '''Invokes a command through SSH on host.

    Parameters:

        con_info - dictionary with connection info:

           - host: hostname or IP of destination host
           - user: username for SSH connection
           - password: password for SSH connection

    Returns a tuple of content blocks read from stdout and stderr provided
    by SSH connection.'''

    if 'host' not in con_info.keys():
        raise KeyError('No host IP specified.')

    if 'user' not in con_info.keys():
        raise KeyError('No username specified.')

    if 'password' not in con_info:
        raise KeyError('No password (even an empty one) specified.')

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(hostname=con_info['host'],
                   username=con_info['user'],
                   password=con_info['password']
                   )

    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read()
    err = stderr.read()

    client.close()

    return [out, err]

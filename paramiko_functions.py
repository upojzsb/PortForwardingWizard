import os
import paramiko
import sshtunnel


def check_host_availability(username, host):
    pkey = paramiko.RSAKey.from_private_key_file(os.path.expanduser('~/.ssh/id_rsa'))

    client = paramiko.SSHClient()

    # Allow hosts that not in known_hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(host, pkey=pkey, username=username)
    client.close()


def check_target_host_availability(username, jump, host, local_port):
    with sshtunnel.open_tunnel(
            (jump, 22),
            ssh_username=username,
            ssh_pkey=os.path.expanduser('~/.ssh/id_rsa'),
            ssh_private_key_password='',
            remote_bind_address=(host, 22),
            local_bind_address=('0.0.0.0', local_port)
    ) as _:
        pkey = paramiko.RSAKey.from_private_key_file(os.path.expanduser('~/.ssh/id_rsa'))
        client = paramiko.SSHClient()
        # Allow hosts that not in known_hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('localhost', pkey=pkey, username=username, port=local_port)
        client.close()


def forwarding_through_jump_server(username, jump, host, local_port, host_port):
    tunnel = sshtunnel.open_tunnel(
        (jump, 22),
        ssh_username=username,
        ssh_pkey=os.path.expanduser('~/.ssh/id_rsa'),
        ssh_private_key_password='',
        remote_bind_address=(host, host_port),
        local_bind_address=('0.0.0.0', local_port)
    )
    tunnel.start()

    # pkey = paramiko.RSAKey.from_private_key_file(os.path.expanduser('~/.ssh/id_rsa'))
    # client = paramiko.SSHClient()
    # # Allow hosts that not in known_hosts
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect('localhost', pkey=pkey, username=username, port=local_port)
    # client.close()

    return tunnel


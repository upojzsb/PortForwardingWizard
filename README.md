# Port Forwarding Wizard

A simple utility that can forward a remote port onto localhost via a jump server.

# Usage

*Only tested on forwarding ssh and Jupyter, and the OS of the localhost should be Windows*

Before using, make sure that key authentication is set correctly between localhost and jump server and jump server and target host. And the username of the jump server and target host should be the same.

For example, if you want to forward SSH service, the following commands should be run properly without input password:
```shell
# Connect jump server from localhost
localuser@localhost$ ssh remote_user@jump_server -p 22
# Connect target host from jump server
remote_user@jump_server$ ssh remote_user@target_host -p 22
# And the username in the jump server and target host should be the same
remote_user@target_host
```

## SSH

In this scenario, the target host can only be connected via a jump server. 

Suppose that the IP of the jump server is `1.1.1.1`, 
the username of the jump server and the target host is the same, which is `username`, 
the hostname of the target is `cu01`, which could be accessed on the jump server, 
and the port of SSH on the target host is `22`, and you want to map it as `10022` on localhost.

Just fill in the blanks as follows:

| Key          | Value    |
|--------------|----------|
| Username:    | username |
| Jump Server: | 1.1.1.1  |
| Target Host: | cu01     |
| Target Port: | 22       |
| Local Port:  | 10022    |


And then, click the **Connect** button, and wait until the status becomes `Connected`, you can connect to the `cu01` via `ssh`:

```shell
localuser@localhost$ ssh username@localhost -p 10022
username@cu01$ 
```

If you connect to different target hosts, `ssh` may warn you like this:

```shell
localuser@localhost$ ssh username@localhost -p 10022
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Please contact your system administrator.
Add correct host key in C:\\Users\\localuser/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in C:\\Users\\localuser/.ssh/known_hosts:1
ECDSA host key for [localhost]:10022 has changed and you have requested strict checking.
Host key verification failed.
```

You need to remove the line below in file `~/.ssh/known_hosts`

```
[localhost]:10022 xxx xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Jupyter
Suppose that the IP of the jump server is `1.1.1.1`, 
the username of the jump server and the target host is the same, which is `username`, 
the hostname of the target is `gpu02`, which could be accessed on the jump server, 
the port of Jupyter would occur when running it, and you want to map it as `10022` on localhost.

First, make a configure file for Jupyter on your target host:

```shell
jupyter notebook --generate-config
```

And edit `~/.jupyter/jupyter_notebook_config.py`, make sure Jupyter would accept remote access:

```python
c.NotebookApp.ip='0.0.0.0'
```

Then, run `jupyter notebook` on the target host (suppose it is gpu02):
```shell
(base) [username@gpu02 ~]$ jupyter notebook
[W 2023-07-03 16:59:22.216 LabApp] 'ip' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[W 2023-07-03 16:59:22.216 LabApp] 'ip' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[W 2023-07-03 16:59:22.216 LabApp] 'ip' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[I 2023-07-03 16:59:22.225 LabApp] JupyterLab extension loaded from /home/username/anaconda3/lib/python3.9/site-packages/jupyterlab
[I 2023-07-03 16:59:22.225 LabApp] JupyterLab application directory is /home/username/anaconda3/share/jupyter/lab
[I 16:59:22.231 NotebookApp] Serving notebooks from local directory: /home/username
[I 16:59:22.231 NotebookApp] Jupyter Notebook 6.4.12 is running at:
[I 16:59:22.231 NotebookApp] http://gpu02:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[I 16:59:22.231 NotebookApp]  or http://127.0.0.1:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[I 16:59:22.231 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 16:59:22.239 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/username/.local/share/jupyter/runtime/nbserver-xxxxx-open.html
    Or copy and paste one of these URLs:
        http://gpu02:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
     or http://127.0.0.1:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Remember the port (`8888` in this case, or you can just set it in the `~/.jupyter/jupyter_notebook_config.py` file), and fill in the blanks as follows:

| Key          | Value    |
|--------------|----------|
| Username:    | username |
| Jump Server: | 1.1.1.1  |
| Target Host: | gpu02    |
| Target Port: | 8888     |
| Local Port:  | 10022    |

And then, click the **Connect** button,  and wait until the status becomes `Connected`, you can browse the Jupyter on your localhost by visiting:

```
http://localhost:10022/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

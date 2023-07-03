import os
import json

import tkinter as tk
from tkinter import messagebox

import traceback

from paramiko_functions import *

# TODO: Rewrite this file into a Class

# Constant
CONNECTED = 0
DISCONNECTED = 1
INVALID = 2

CONNECTED_TEXT = 'Connected'
DISCONNECTED_TEXT = 'Disconnected'
INVALID_TEXT = 'Invalid'

# Global variables
# Tk related
root_window = tk.Tk()
window_name = ''
version = ''
variable_dict = dict()

# Network related
forwarding_tunnel = None

# Status related
connect_status = DISCONNECTED


def root_window_init(window_info):
    """
    Initialize root window

    :param window_info: Window infos
    :type window_info: dict
    :return: root_window
    :rtype: tk.Tk
    """
    global root_window, window_name, version, variable_dict
    global connect_status

    version = window_info['version']

    window_name = window_info['window_name']

    # Window's properties
    root_window.title(window_name)

    root_window.geometry('450x300')
    root_window.resizable(False, False)

    # TODO: Design an icon
    # root_window.iconbitmap('icon.ico')

    # Fixed Labels
    for k, v in window_info['Labels'].items():
        tk.Label(root_window, text=k).place(x=v[0], y=v[1])

    # Fixed Buttons
    for k, v in window_info['Buttons'].items():
        tk.Button(root_window, text=k, width=10, height=2, command=v[2]).place(x=v[0], y=v[1])

    # Variable Labels
    variable_dict['status'] = tk.Label(root_window, text='*')

    variable_dict['status'].place(x=120, y=240)

    # Variable Entries
    variable_dict['username'] = tk.Entry(root_window, width=40)
    variable_dict['jump server'] = tk.Entry(root_window, width=40)
    variable_dict['target host'] = tk.Entry(root_window, width=40)
    variable_dict['target port'] = tk.Entry(root_window, width=40)
    variable_dict['local port'] = tk.Entry(root_window, width=10)

    variable_dict['username'].place(x=120, y=20)
    variable_dict['jump server'].place(x=120, y=60)
    variable_dict['target host'].place(x=120, y=100)
    variable_dict['target port'].place(x=120, y=140)
    variable_dict['local port'].place(x=120, y=200)

    # Callback functions
    root_window.protocol('WM_DELETE_WINDOW', quit_confirm_message_callback)

    # Init TK items
    variable_dict['local port'].insert(0, '10022')
    variable_dict['status'].config(text=DISCONNECTED_TEXT)

    connect_status = DISCONNECTED

    # Use saved config
    if os.path.exists('config.json'):
        with open('config.json', 'r') as fp:
            config_json = json.load(fp)

        if {'username', 'jump server', 'target host', 'target port', 'local port'}.issubset(set(config_json.keys())):
            variable_dict['username'].insert(0, config_json['username'])
            variable_dict['jump server'].insert(0, config_json['jump server'])
            variable_dict['target host'].insert(0, config_json['target host'])
            variable_dict['target port'].insert(0, config_json['target port'])
            variable_dict['local port'].delete(0, len(variable_dict['local port'].get()))
            variable_dict['local port'].insert(0, config_json['local port'])
        else:  # Config file invalid
            os.remove('config.json')

    return root_window


# Callback functions
def quit_confirm_message_callback():
    if connect_status == CONNECTED:
        messagebox.showerror(window_name, 'Disconnect current tunnel before quitting!')
        return

    if messagebox.askyesno(window_name, 'Do you want to quit?'):
        # Save the configs
        config_dict = {
            'username': variable_dict['username'].get(),
            'jump server': variable_dict['jump server'].get(),
            'target host': variable_dict['target host'].get(),
            'target port': variable_dict['target port'].get(),
            'local port': variable_dict['local port'].get()
        }

        with open('config.json', 'w') as fp:
            json.dump(config_dict, fp)

        root_window.destroy()


def connect_callback():
    global forwarding_tunnel, connect_status

    if connect_status == CONNECTED:
        messagebox.showwarning(
            window_name,
            'Disconnect current tunnel before start a new connection.'
        )
        return

    # Get contents of entries
    username = variable_dict['username'].get()
    jump_server = variable_dict['jump server'].get()
    target_host = variable_dict['target host'].get()
    target_port = int(variable_dict['target port'].get())
    local_port = int(variable_dict['local port'].get())

    # Check connectivity of the jump server
    try:
        check_host_availability(username, jump_server)
    except Exception as e:
        messagebox.showerror(
            window_name,
            'Check connectivity of the jump server FAILED.\n'
            'Error message:\n' + e.__repr__()
        )
        return

    # Check connectivity of the target host
    try:
        check_target_host_availability(username, jump_server, target_host, local_port)
    except Exception as e:
        messagebox.showerror(
            window_name,
            'Check connectivity of the target host FAILED.\n'
            'Error message:\n' + e.__repr__()
        )
        return

    forwarding_tunnel = forwarding_through_jump_server(username, jump_server, target_host, local_port, target_port)
    connect_status = CONNECTED
    refresh_labels(variable_dict['status'], CONNECTED_TEXT)


def disconnect_callback():
    global forwarding_tunnel, connect_status
    forwarding_tunnel.close()
    connect_status = DISCONNECTED
    refresh_labels(variable_dict['status'], DISCONNECTED_TEXT)


def about_callback():
    messagebox.showinfo(
        window_name,
        'Author: UPO-JZSB.\nVersion: ' + version + '.\nReleased under GPL-V2 License.'
    )


def refresh_labels(label, text):
    label.config(text=text)

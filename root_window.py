import json

import tkinter as tk
from tkinter import messagebox

from paramiko_functions import *


class RootWindow(tk.Frame):
    # Project Informations
    version = '1.10'
    window_name = 'Port Forwarding Wizard'

    # Constants
    CONNECTED = 0
    DISCONNECTED = 1
    INVALID = 2

    CONNECTED_TEXT = 'Connected'
    DISCONNECTED_TEXT = 'Disconnected'
    INVALID_TEXT = 'Invalid'

    # Global variables
    # # Tk related
    variable_dict = dict()

    # # Network related
    forwarding_tunnel = None

    # # Status related
    connect_status = DISCONNECTED

    def __init__(self):
        """
        Initialize root window

        :return: None
        """
        super().__init__()

        # Window's properties
        self.master.title(self.window_name)
        self.master.geometry('450x300')
        self.master.resizable(False, False)

        # TODO: Design an icon
        # root_window.iconbitmap('icon.ico')

        self._create_init_widgets_()

        # Callback functions
        self.master.protocol('WM_DELETE_WINDOW', self.quit_confirm_message_callback)



    def _create_init_widgets_(self):
        """
        Create and init Widgets for RootWindow
        :return: None
        """
        # Tk
        tk_labels = {
            # Text: [x, y]
            'Username: ': [40, 20],
            'Jump Server:': [40, 60],
            'Target Host:': [40, 100],
            'Target Port:': [40, 140],
            'Local Port:': [40, 200],
            # variable
            'Status:': [40, 240],
        }

        tk_buttons = {
            # Text: [x, y, callback]
            'Connect': [250, 200, self.connect_callback],
            'Disconnect': [250, 250, self.disconnect_callback],

            # TODO: Add some advanced settings, including:
            # 1. Add a selection to disable pre-connection test
            # 2. Add a config to select the ssh key file path and file name
            # 3. Add a config to input the password of the ssh key file
            # 4. Allow different key file in connecting jump server and the target server
            # 5. Allow different user in connecting jump server and the target server
            'Advanced\nSettings': [350, 200, self.advanced_settings_callback],
            'About': [350, 250, self.about_callback],
        }

        # Fixed Labels
        for k, v in tk_labels.items():
            tk.Label(self.master, text=k).place(x=v[0], y=v[1])

        # Fixed Buttons
        for k, v in tk_buttons.items():
            tk.Button(self.master, text=k, width=10, height=2, command=v[2]).place(x=v[0], y=v[1])

        # Variable Labels
        self.variable_dict['status'] = tk.Label(self.master, text='')

        self.variable_dict['status'].place(x=120, y=240)

        # Variable Entries
        self.variable_dict['username'] = tk.Entry(self.master, width=40)
        self.variable_dict['jump server'] = tk.Entry(self.master, width=40)
        self.variable_dict['target host'] = tk.Entry(self.master, width=40)
        self.variable_dict['target port'] = tk.Entry(self.master, width=40)
        self.variable_dict['local port'] = tk.Entry(self.master, width=10)

        self.variable_dict['username'].place(x=120, y=20)
        self.variable_dict['jump server'].place(x=120, y=60)
        self.variable_dict['target host'].place(x=120, y=100)
        self.variable_dict['target port'].place(x=120, y=140)
        self.variable_dict['local port'].place(x=120, y=200)

        # Init TK items
        self.variable_dict['local port'].insert(0, '10022')
        self.variable_dict['status'].config(text=self.DISCONNECTED_TEXT)

        self.connect_status = self.DISCONNECTED

        # Use saved config
        if os.path.exists('config.json'):
            with open('config.json', 'r') as fp:
                config_json = json.load(fp)

            if {'username', 'jump server', 'target host', 'target port', 'local port'}.issubset(
                    set(config_json.keys())):
                self.variable_dict['username'].insert(0, config_json['username'])
                self.variable_dict['jump server'].insert(0, config_json['jump server'])
                self.variable_dict['target host'].insert(0, config_json['target host'])
                self.variable_dict['target port'].insert(0, config_json['target port'])
                self.variable_dict['local port'].delete(0, len(self.variable_dict['local port'].get()))
                self.variable_dict['local port'].insert(0, config_json['local port'])
            else:  # Config file invalid
                os.remove('config.json')

    # Callback functions
    def quit_confirm_message_callback(self):
        if self.connect_status == self.CONNECTED:
            messagebox.showerror(self.window_name, 'Disconnect current tunnel before quitting!')
            return

        if messagebox.askyesno(self.window_name, 'Do you want to quit?'):
            # Save the configs
            config_dict = {
                'username': self.variable_dict['username'].get(),
                'jump server': self.variable_dict['jump server'].get(),
                'target host': self.variable_dict['target host'].get(),
                'target port': self.variable_dict['target port'].get(),
                'local port': self.variable_dict['local port'].get()
            }

            with open('config.json', 'w') as fp:
                json.dump(config_dict, fp)

            self.master.destroy()

    def connect_callback(self):
        if self.connect_status == self.CONNECTED:
            messagebox.showwarning(
                self.window_name,
                'Disconnect current tunnel before start a new connection.'
            )
            return

        # Get contents of entries
        username = self.variable_dict['username'].get()
        jump_server = self.variable_dict['jump server'].get()
        target_host = self.variable_dict['target host'].get()
        target_port = int(self.variable_dict['target port'].get())
        local_port = int(self.variable_dict['local port'].get())

        # Check connectivity of the jump server
        try:
            check_host_availability(username, jump_server)
        except Exception as e:
            messagebox.showerror(
                self.window_name,
                'Check connectivity of the jump server FAILED.\n'
                'Error message:\n' + e.__repr__()
            )
            return

        # Check connectivity of the target host
        try:
            check_target_host_availability(username, jump_server, target_host, local_port)
        except Exception as e:
            messagebox.showerror(
                self.window_name,
                'Check connectivity of the target host FAILED.\n'
                'Error message:\n' + e.__repr__()
            )
            return

        self.forwarding_tunnel = forwarding_through_jump_server(
            username,
            jump_server,
            target_host,
            local_port,
            target_port
        )
        self.connect_status = self.CONNECTED
        self.refresh_labels(self.variable_dict['status'], self.CONNECTED_TEXT)

    def disconnect_callback(self):
        self.forwarding_tunnel.close()
        self.connect_status = self.DISCONNECTED
        self.refresh_labels(self.variable_dict['status'], self.DISCONNECTED_TEXT)

    def about_callback(self):
        messagebox.showinfo(
            self.window_name,
            'Author: UPO-JZSB.\nVersion: ' + self.version + '.\nReleased under GPL-V2 License.'
        )

    def advanced_settings_callback(self):
        messagebox.showinfo(
            self.window_name,
            'Not yet implemented'
        )

    # Static methods
    @staticmethod
    def refresh_labels(label, text):
        label.config(text=text)

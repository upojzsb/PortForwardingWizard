import json

import tkinter as tk
from tkinter import messagebox

from paramiko_functions import *

from advanced_settings_window import AdvancedSettingsWindow


class RootWindow(tk.Frame):
    # Project Information
    version = '2.10'
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
    tk_variable_dict = dict()

    # # Network related
    forwarding_tunnel = None

    # # Status related
    connect_status = DISCONNECTED

    # # Flags
    check_connectivity_flag = 0

    # # Path
    ssh_key_file = ''

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

        # Load all settings
        self.load_settings()
        self.load_advanced_settings()

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
            # MISC

            # SSH KEY SETTING
            # 3. Add a config to input the password of the ssh key file
            # 4. Allow different key file in connecting jump server and the target server

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
        self.tk_variable_dict['status'] = tk.Label(self.master, text='')

        self.tk_variable_dict['status'].place(x=120, y=240)

        # Variable Entries
        self.tk_variable_dict['username'] = tk.Entry(self.master, width=40)
        self.tk_variable_dict['jump server'] = tk.Entry(self.master, width=40)
        self.tk_variable_dict['target host'] = tk.Entry(self.master, width=40)
        self.tk_variable_dict['target port'] = tk.Entry(self.master, width=40)
        self.tk_variable_dict['local port'] = tk.Entry(self.master, width=10)

        self.tk_variable_dict['username'].place(x=120, y=20)
        self.tk_variable_dict['jump server'].place(x=120, y=60)
        self.tk_variable_dict['target host'].place(x=120, y=100)
        self.tk_variable_dict['target port'].place(x=120, y=140)
        self.tk_variable_dict['local port'].place(x=120, y=200)

        # Init TK items
        self.tk_variable_dict['local port'].insert(0, '10022')
        self.tk_variable_dict['status'].config(text=self.DISCONNECTED_TEXT)

        self.connect_status = self.DISCONNECTED

    def load_settings(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as fp:
                config_json = json.load(fp)

            if {'username', 'jump server', 'target host', 'target port', 'local port'}.issubset(
                    set(config_json.keys())):
                self.tk_variable_dict['username'].insert(0, config_json['username'])
                self.tk_variable_dict['jump server'].insert(0, config_json['jump server'])
                self.tk_variable_dict['target host'].insert(0, config_json['target host'])
                self.tk_variable_dict['target port'].insert(0, config_json['target port'])
                self.tk_variable_dict['local port'].delete(0, 'end')
                self.tk_variable_dict['local port'].insert(0, config_json['local port'])
            else:  # Config file invalid
                os.remove('config.json')

    def save_settings(self):
        # Save the configs
        config_dict = {
            'username': self.tk_variable_dict['username'].get(),
            'jump server': self.tk_variable_dict['jump server'].get(),
            'target host': self.tk_variable_dict['target host'].get(),
            'target port': self.tk_variable_dict['target port'].get(),
            'local port': self.tk_variable_dict['local port'].get()
        }

        with open('config.json', 'w') as fp:
            json.dump(config_dict, fp)

    def load_advanced_settings(self):
        if os.path.exists('config_advanced.json'):
            with open('config_advanced.json', 'r') as fp:
                config_json = json.load(fp)

            if {'miscConnectivityCheck', 'sshkeyPath', }.issubset(set(config_json.keys())):
                self.check_connectivity_flag = config_json['miscConnectivityCheck']
                self.ssh_key_file = config_json['sshkeyPath']

                # All ok
                return

        # Something wrong
        # Create the config_advanced.json as the default value
        self.check_connectivity_flag = 1
        self.ssh_key_file = os.path.expanduser('~/.ssh/id_rsa')
        config_dict = {
            'miscConnectivityCheck': self.check_connectivity_flag,
            'sshkeyPath': self.ssh_key_file,
        }

        with open('config_advanced.json', 'w') as fp:
            json.dump(config_dict, fp)

    # Callback functions
    def quit_confirm_message_callback(self):
        if self.connect_status == self.CONNECTED:
            messagebox.showerror(self.window_name, 'Disconnect current tunnel before quitting!')
            return

        if messagebox.askyesno(self.window_name, 'Do you want to quit?'):
            self.save_settings()
            self.master.destroy()

    def connect_callback(self):
        if self.connect_status == self.CONNECTED:
            messagebox.showwarning(
                self.window_name,
                'Disconnect current tunnel before start a new connection.'
            )
            return

        # Get contents of entries
        username = self.tk_variable_dict['username'].get()
        jump_server = self.tk_variable_dict['jump server'].get()
        target_host = self.tk_variable_dict['target host'].get()
        target_port = int(self.tk_variable_dict['target port'].get())
        local_port = int(self.tk_variable_dict['local port'].get())

        if local_port < 1 or local_port > 65535 or target_port < 1 or target_port > 65535:
            messagebox.showerror(
                self.window_name,
                'All ports should be set between 1 and 65535.'
            )
            return

        # Check connectivity of the jump server
        if self.check_connectivity_flag:
            try:
                check_host_availability(
                    username=username,
                    host=jump_server,
                    ssh_key_path=self.ssh_key_file
                )
            except Exception as e:
                messagebox.showerror(
                    self.window_name,
                    'Check connectivity of the jump server FAILED.\n'
                    'Error message:\n' + e.__repr__()
                )
                return

            # Check connectivity of the target host
            try:
                check_target_host_availability(
                    username=username,
                    jump=jump_server,
                    host=target_host,
                    local_port=local_port,
                    ssh_key_path=self.ssh_key_file
                )
            except Exception as e:
                messagebox.showerror(
                    self.window_name,
                    'Check connectivity of the target host FAILED.\n'
                    'Error message:\n' + e.__repr__()
                )
                return

        self.forwarding_tunnel = forwarding_through_jump_server(
            username=username,
            jump=jump_server,
            host=target_host,
            local_port=local_port,
            host_port=target_port,
            ssh_key_path=self.ssh_key_file
        )
        self.connect_status = self.CONNECTED
        self.refresh_labels(self.tk_variable_dict['status'], self.CONNECTED_TEXT)

        self.set_widget_with_connect_status()

    def disconnect_callback(self):
        self.forwarding_tunnel.close()
        self.connect_status = self.DISCONNECTED
        self.refresh_labels(self.tk_variable_dict['status'], self.DISCONNECTED_TEXT)

        self.set_widget_with_connect_status()

    def about_callback(self):
        messagebox.showinfo(
            self.window_name,
            'Author: UPO-JZSB.\nVersion: ' + self.version + '.\nReleased under GPL-V2 License.'
        )

    def advanced_settings_callback(self):
        advanced_window = AdvancedSettingsWindow(self)
        advanced_window.grab_set()  # This will make the AdvancedSettingsWindow modal
        self.wait_window(advanced_window)  # Wait for AdvancedSettingsWindow to be closed before resuming

        self.load_advanced_settings()

    def set_widget_with_connect_status(self):
        if self.connect_status == self.CONNECTED:
            self.tk_variable_dict['username'].config(state='disabled')
            self.tk_variable_dict['jump server'].config(state='disabled')
            self.tk_variable_dict['target host'].config(state='disabled')
            self.tk_variable_dict['target port'].config(state='disabled')
            self.tk_variable_dict['local port'].config(state='disabled')
        else:
            self.tk_variable_dict['username'].config(state='normal')
            self.tk_variable_dict['jump server'].config(state='normal')
            self.tk_variable_dict['target host'].config(state='normal')
            self.tk_variable_dict['target port'].config(state='normal')
            self.tk_variable_dict['local port'].config(state='normal')

    # Static methods
    @staticmethod
    def refresh_labels(label, text):
        label.config(text=text)

import os
import json

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from paramiko_functions import *


class AdvancedSettingsWindow(tk.Toplevel):

    # Constants
    window_name = 'Port Forwarding Wizard - Advanced Settings'

    # Global variables
    # # Tk related
    variable_dict = dict()

    def __init__(self, parent):
        """
        Initialize advanced settings window

        :return: None
        """
        super().__init__(parent)

        self.parent = parent

        # Window's properties
        self.title(self.window_name)
        self.geometry('450x300')
        self.resizable(False, False)

        # root_window.iconbitmap('icon.ico')

        self._create_init_widgets_()

        # Callback functions
        # self.master.protocol('WM_DELETE_WINDOW', self.quit_confirm_message_callback)

        self.load_advanced_settings()

    def _create_init_widgets_(self):
        """
        Create and init Widgets for RootWindow
        :return: None
        """

        # LabelFrames
        # Declare before labels & buttons declaration to provide master for them
        frame_ssh_key_settings = tk.LabelFrame(self, height=150, width=450, text='SSH Key Settings')
        frame_ssh_key_settings.place(x=0, y=0)

        frame_misc = tk.LabelFrame(self, height=100, width=450, text='Miscellaneous')
        frame_misc.place(x=0, y=150)

        # Tk
        tk_labels = {
            # Text: [x, y, master]
            'SSH Key Path:': [0, 0, frame_ssh_key_settings]
        }

        tk_buttons = {
            # Text: [x, y, callback, master]
            'Apply': [150, 250, self.apply_callback, self],
            'Cancel': [250, 250, self.cancel_callback, self],
            'Default': [350, 250, self.default_callback, self],
            # ssh key settings frame
            'Pick\nPrivate Key': [350, -10, self.pick_key_callback, frame_ssh_key_settings],
        }

        tk_checkbuttons = {
            # variable name: [x, y, master, text]
            'miscConnectivityCheck': [0, 0, frame_misc, 'Check the connectivity before set up tunnel']
        }

        tk_entry = {
            # variable name: [x, y, master]
            'sshkeyPath': [100, 0, frame_ssh_key_settings]
        }

        # Fixed Labels
        for k, v in tk_labels.items():
            tk.Label(v[2], text=k).place(x=v[0], y=v[1])

        # Fixed Buttons
        for k, v in tk_buttons.items():
            tk.Button(v[3], text=k, width=10, height=2, command=v[2]).place(x=v[0], y=v[1])

        # Fixed check buttons
        for k, v, in tk_checkbuttons.items():
            checkbutton = tk.Checkbutton(v[2], text=v[3], onvalue=1, offvalue=0)
            checkbutton.place(x=v[0], y=v[1])

            self.variable_dict[k] = tk.IntVar()
            checkbutton['variable'] = self.variable_dict[k]

        # Fixed entry
        for k, v in tk_entry.items():
            self.variable_dict[k] = tk.StringVar()

            entry = tk.Entry(v[2], width=40, textvariable=self.variable_dict[k])
            entry.place(x=v[0], y=v[1])

    def load_advanced_settings(self):
        if os.path.exists('config_advanced.json'):
            with open('config_advanced.json', 'r') as fp:
                config_json = json.load(fp)

            if {'miscConnectivityCheck', 'sshkeyPath', }.issubset(set(config_json.keys())):
                self.variable_dict['miscConnectivityCheck'].set(config_json['miscConnectivityCheck'])
                self.variable_dict['sshkeyPath'].set(config_json['sshkeyPath'])
                # File exist and valid
                return
        # Neither the file does not exist nor its invalid
        self.default_callback()

    def save_advanced_settings(self):
        config_dict = {
            'miscConnectivityCheck': self.variable_dict['miscConnectivityCheck'].get(),
            'sshkeyPath': self.variable_dict['sshkeyPath'].get(),
        }

        with open('config_advanced.json', 'w') as fp:
            json.dump(config_dict, fp)

    def pick_key_callback(self):
        # Initial dir
        original_text = self.variable_dict['sshkeyPath'].get()
        if os.path.exists(os.path.dirname(original_text)):
            initialdir = os.path.dirname(original_text)
        elif os.path.exists(os.path.expanduser('~/.ssh/')):
            initialdir = os.path.expanduser('~/.ssh/')
        else:
            initialdir = os.path.expanduser('~/')

        filename = filedialog.askopenfilename(
            title='Select SSH Key File',
            initialdir=initialdir
        )

        # Nothing selected
        if not filename:
            return

        if filename.endswith('pub'):
            messagebox.showerror(
                self.window_name,
                'Pick the private key file instead of the public key file.'
            )
            # Do not set the entry
            return

        with open(filename, mode='r') as fp:
            first_line = fp.readline()

        if 'private' not in first_line.lower() or 'key' not in first_line.lower():
            messagebox.showerror(
                self.window_name,
                'This is not a valid private key file.'
            )
            # Do not set the entry
            return

        self.variable_dict['sshkeyPath'].set(filename)

    def apply_callback(self):
        if messagebox.askyesno(self.window_name, 'Do you want to apply?'):
            self.save_advanced_settings()
            self.destroy()

    def cancel_callback(self):
        self.destroy()

    def default_callback(self):
        self.variable_dict['miscConnectivityCheck'].set(1)
        self.variable_dict['sshkeyPath'].set(os.path.expanduser('~/.ssh/id_rsa'))

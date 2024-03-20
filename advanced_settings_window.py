import os
import json

import tkinter as tk
from tkinter import messagebox

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
        }

        tk_buttons = {
            # Text: [x, y, callback, master]
            'Apply': [250, 250, self.apply_callback, self],
            'Cancel': [350, 250, self.cancel_callback, self],
        }

        tk_checkbuttons = {
            # variable name: [x, y, master, text]
            'miscConnectivityCheck': [0, 0, frame_misc, 'Check the connectivity before set up tunnel']
        }

        # Fixed Labels
        for k, v in tk_labels.items():
            tk.Label(v[3], text=k).place(x=v[0], y=v[1])

        # Fixed Buttons
        for k, v in tk_buttons.items():
            tk.Button(v[3], text=k, width=10, height=2, command=v[2]).place(x=v[0], y=v[1])

        # Fixed check buttons
        for k, v, in tk_checkbuttons.items():
            checkbutton = tk.Checkbutton(v[2], text=v[3], onvalue=1, offvalue=0)
            checkbutton.place(x=v[0], y=v[1])

            self.variable_dict[k] = tk.IntVar()
            checkbutton['variable'] = self.variable_dict[k]

    def load_advanced_settings(self):
        # Use saved config
        if os.path.exists('config_advanced.json'):
            with open('config_advanced.json', 'r') as fp:
                config_json = json.load(fp)

            if {'miscConnectivityCheck', }.issubset(set(config_json.keys())):
                self.variable_dict['miscConnectivityCheck'].set(config_json['miscConnectivityCheck'])

    def save_advanced_settings(self):
        config_dict = {
            'miscConnectivityCheck': self.variable_dict['miscConnectivityCheck'].get(),
        }

        with open('config_advanced.json', 'w') as fp:
            json.dump(config_dict, fp)

    def apply_callback(self):
        if messagebox.askyesno(self.window_name, 'Do you want to apply?'):
            self.save_advanced_settings()
            self.destroy()

    def cancel_callback(self):
        if messagebox.askyesno(self.window_name, 'Do you want to cancel?'):
            self.destroy()

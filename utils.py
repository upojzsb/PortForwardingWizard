from tk_functions import about_callback, connect_callback, disconnect_callback


def get_window_info():
    return {
        'version': '1.0',

        'window_name': 'Port Forwarding Wizard',

        'Labels': {
            # Text: [x, y]
            'Username: ': [40, 20],
            'Jump Server:': [40, 60],
            'Target Host:': [40, 100],
            'Target Port:': [40, 140],
            'Local Port:': [40, 200],
            # variable
            'Status:': [40, 240],
        },

        'Buttons': {
            # Text: [x, y, callback]
            'Connect': [250, 200, connect_callback],
            'Disconnect': [250, 250, disconnect_callback],
            'About': [350, 250, about_callback],
        }
    }

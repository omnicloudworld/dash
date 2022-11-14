#!/usr/bin/env python3.10

from skyant.ui.app import Bootstrapped

app = Bootstrapped(
    'NaMe',
    default_theme=Bootstrapped.theme.SUPERHERO
)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8008)

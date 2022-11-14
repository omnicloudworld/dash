#!/usr/bin/env python3.10
'''
'''

from dash import html

from skyant.ui.app import Bootstrapped, Servers

class My(Servers, Bootstrapped):
    pass


app = My(name='sdsds')

app.layout = html.Div(
    'sds'
)

server = app.asgi_server
if __name__ == '__main__':
    app.debug_server()

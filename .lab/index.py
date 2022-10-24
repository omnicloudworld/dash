#!/usr/bin/env python3.10
'''
'''

from dash import html
from skyant.web.platform import BootstrappedDash, SkyAntServers

class My(SkyAntServers, BootstrappedDash):

    def __init__(self, name='sdsd', **kw):
        super().__init__(name=name, **kw)

app = My(name='sdsds')


app.layout = html.Div(
    'sds'
)



if __name__ == '__main__':
    app.debug_server()

---
hide:
    - navigation
---

#

The Dash provides a features for running an application, serve CSS & JS files.

The skyant.ui.app.Servers provides a feature for serving any files and features for running
    the Dash with HTTP/2 web-server.

Host name & port should to define during initialization a class.

```py linenums='1' title='index.py'
#!/usr/bin/env python3.10

from skyant.ui.app import Servers

app = Servers(
    'Name',
    host='0.0.0.0',
    port=8008
)

if __name__ == '__main__':
    app.debug_server()
```

## Serve files

For serving any files from application put they in the directory "static" near the application
    file.

All files from this directory will be served on the path "static".


## Debug server

For fast run debug_server call the method ```debug_server()```.


## Asgi & Async server

The skyant.ui.app.Servers provides two properties with middleware that needed for running
    HTTP/2 server.

- asgi_server
    _contains asgiref.wsgi.WsgiToAsgi object_

- async_server
    _contains hypercorn.middleware.AsyncioWSGIMiddleware_

```bash linenums='1' title='run production server'
hypercorn -w 1 --bind 0.0.0.0:8008 index:asgi_server
```

!!!bug

    async_server don't support file uploading 


#

The package includes next classes:

- Bootstrapped - preloaded Bootstrap theme, Google Fonts, Awesome & material icons

- CoLab - class for running inside Jupyter notebook

- PyScript - preloaded [PyScript](https://pyscript.net)

- Servers - preconfigured development & production servers with serving static files


An inheritance from skyant.ui.app.* will be as from single class well as with polymorphism from 
any classes.

## Single

```python3
#!/usr/bin/env python3.10

from skyant.ui.app import Bootstrapped

app = Bootstrapped('Name')

if __main__ == '__name__':
    app.run_server(host='0.0.0.0', port=8008)
```

## Polymorph

```python3
#!/usr/bin/env python3.10

from skyant.ui.app import Bootstrapped, Servers

class MyDash(Bootstrapped, Servers):
    pass

app = MyDash('Name')

if __main__ == '__name__':
    app.debug_server()
```
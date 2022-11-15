---
hide:
    - navigation
---

#

## Base layout

Classes Servers, PyScript & CoLab provide nothing predefined layouts.

The class Bootstrapped provides some frequently uses elements and a section tag for deploying
    an application's contents.

Predefined layouts contains:

- [Dash core component __Location__](https://dash.plotly.com/dash-core-components/location){:target=_blank}
    with id='__url__'

    _This element provide to your python code current url value & features to modify it._

- [Dash html component __Section__](https://dash.plotly.com/dash-html-components/section){:target=_blank}
    with id='__page__'
    
    _It's a place for deploying the application's content._

- _(optional)_ up to three [Dash core component __Store__](https://dash.plotly.com/dash-core-components/store){:target=_blank}
    with id: __store-local__, __store-session__, __store-memory__

    _Each of they elements provide features to save session data._

```py linenums='1' title='full dash layout'
from dash import html, dcc

layout = html.Div(
    [
        html.Div(
            [
                dcc.Location(id='url'),
                dcc.Store(id='store-local', storage_type='local'),
                dcc.Store(id='store-session', storage_type='session'),
                dcc.Store(id='store-memory', storage_type='memory')
            ],
            id='skyant',
            style={'display': 'none'}
        ),
        html.Section(id='page'),
        
    ],
    id='root'
)
```

You should to set the relevant class initial argument to True if you want to get a store object.

```py linenums='1' title='local store initialisation'
from skyant.ui.app import Bootstrapped

app = Bootstrapped(
    'Name',
    store_local=True
)
```


## Send layout

Of course you can set the layout attribute up in the class. But if you need to avoid a limitation
    on only one callback per html element, you can use the method skyant.ui.app.Bootstrapped.layouter().

```py linenums='1' title='layouter method'
from dash import html
from skyant.ui.app import Bootstrapped

app = Bootstrapped(
    'Name',
)

app.layouter(
    html.Div('content')
)
```


## URL routing



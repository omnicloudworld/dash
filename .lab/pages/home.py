from dash import register_page, html

register_page(
    __name__,
    path='/',
    path_template='pp/<p>',
    relative_path='zx/',
    title='TTTTitle',
    description='''
    q3ior 9438u5 t98u34 9pt8u34pw8ty 498tu 5pt
    12436789
    '''
)


def layout(a: str = None, **kw):

    qstring = html.H2(f"Q: {kw.get('q', 'EMPTY')}")
    pstring = html.H2(f"P: {kw.get('p', 'EMPTY')}")
    astring = html.H2(f"A: {kw.get('a', a) or 'EMPTY'}")

    return html.Div(
        [
            qstring,
            pstring,
            astring
        ],
        className='px-5 py-3'
    )

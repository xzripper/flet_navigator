<h1 align="center">FletNavigator V2.2.5</h1>
<p align="center"><img src="example2.gif" width=600><br><i>FletNavigator & <a href="https://github.com/xzripper/flet_restyle">FletReStyle</a>.</i></p>
<p align="center">Simple and fast navigator (router) for Flet (Python) that allows you to create multi-page applications! [<code>pip install flet_navigator</code>].<br><b>[<a href="https://github.com/xzripper/flet_navigator/blob/main/flet-navigator-docs.md">DOCUMENTATION</a>].</b></p>
<p align="center">Using Example:

```python
from flet import app, Page

from flet_navigator import VirtualFletNavigator, PageData, ROUTE_404


def main_page(pg: PageData) -> None:
    ... # Main page content.

def second_page(pg: PageData) -> None:
    ... # Second page content.

def route_404(pg: PageData) -> None:
    ... # 404 Page Content.

def main(page: Page) -> None:
    # Initialize navigator.
    flet_navigator = VirtualFletNavigator(
        {
            '/': main_page, # Main page route.
            'second_page': second_page, # Second page route.
            ROUTE_404: route_404 # 404 page route.
        }, lambda route: print(f'Route changed!: {route}') # Route change handler (optional).
    )

    flet_navigator.render(page) # Render current page.

app(target=main)
```

</p>

<p align="center"><img src="example.gif" width=500></p> <p align="center"><i>(Deprecated Example GIF).</i></p>

See the difference between ```VirtualFletNavigator``` and ```FletNavigator```, and more <a href="https://github.com/xzripper/flet_navigator/blob/main/flet-navigator-docs.md">here</a> (<- documentation).

<hr>
<p align="center">FletNavigator v2.2.5.</p></i>

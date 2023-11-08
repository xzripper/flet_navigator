<h1 align="center">FletNavigator v2.1.1 Documentation.</h1>

<h4 align="center">Menu:</h4>

- [Getting Started.](#getting-started)
- [General.](#general)
- [`VirtualFletNavigator`](#virtualfletnavigator)
- [`FletNavigator`](#fletnavigator)
- [`define_page`](#define_page)
- [Summary.](#summary)

<hr>

<h3 align="center">Getting Started.</h3>
FletNavigator - Simple and fast navigator (router) for Flet (Python) that allows you to create multi-page applications!<br>It allows you to define own routes, provides built-in URL parameters support, animations (in-future), virtual routing, and more...<br><br>

Installation is quite easy: ```pip install flet_navigator```

> [!WARNING]  
> FletNavigator is in active development phase + only one developers works on this project. Please, be patient and report all bugs.

**FletNavigator Features**:
  - **✨ Simple installation and very simple using.**
  - **✨ Fast.**
  - **✨ Cookies-like mechanism.**
  - **✨ Animations between page change. (FUTURE).**
  - **✨ Built-in smart URL parameters parser.**
  - **✨ Multiple routing modes.**
  - **✨ And more! And even more coming in future!**

**FletNavigator TODO**:
  - **Animations between page change.**
  - ~**Implement URL parameters for `navigate`.**~
  - **Fix bugs.**

**FletNavigator Known Bugs**:
  - ~**Double redirect when using `navigate` (class `FletNavigator`).**~
  - **Unable to trace previous page when manually updating URL in browser (`_nav_route_change_handler`). (Seems like fixed).**
  - **Non-tested in real projects.**

<hr>

<h3 align="center">General.</h3>

- **What's the difference between virtual navigator (`VirtualFletNavigator`) and non virtual navigator (`FletNavigator`)?**<br>
Virtual navigator uses its own virtual route for navigating. `VirtualFletNavigator` depends on `VirtualFletNavigator.route`, while `FletNavigator` uses page route (`page.route`).<br><br>
While you're using virtual navigator you can't have route in your URL, because route is virtual (created in navigator class and used in navigator class). Also you can't use URL parameters. Basically this mode is useful for desktop applications, because you don't need URL's in desktop application, URL parameters even more so. You can share your data between pages using `arguments` (keep reading for explanation).<br><br>
What's about non virtual navigator? Non-virtual navigator uses actual page route, so navigator renders page depending on page route. So you can have route in your URL (<code>`http://127.0.0.1:53863/` `second_page`</code>), URL parameters (`http://127.0.0.1:53863/second_page?id=123&etc=true`), etc. This mode should be used in web applications (optional).<br><br>

- **"Cookies-like mechanism"?**

FletNavigator has its own cookies like mechanism for each route (page). The main difference from cookies that that data contained on server, in navigator class, not on user computer. Example:

```python
navigator.set_route_data('my_page', data)

# Somewhere on other page....
navigator.get_route_data('my_page') # => data
```

<br>

- **URL Parameters.**

URL Parameters (`http://127.0.0.1:53863/second_page?id=123&etc=true`) will be returned as dictionary (`{'id': 123, 'etc': True}`) (parameters parser can cast types).

<br>

- **Route naming.**

Route should have latin alphabet (no cyrillic), route can have underscores and digits. Route can't have special characters, cyrillic alphabet & spaces. Wrong route will be removed from registered routes.

```flet_navigator::constructor:51: Warning: Wrong route name: "$my_route1У H". Allowed only digits and underscores.```

<hr>

<h3 align="center"><code>VirtualFletNavigator</code></h3>

- `VirtualFletNavigator` - Virtual Flet Navigator Class.
  - `route: str = '/'` - Current route.
  - `routes: dict[str, Callable[[PageData], None]] = {}` - Registered routes.
  - `routes_data: dict[str, Any] = {}` - Routes data.
  - `route_changed_handler: Callable[[str], None] = None` - Route changed handler.<br><br>

  - `__init__(routes: dict[str, Callable[[Page, 'VirtualFletNavigator', tuple[Any], str], None]], route_changed_handler: Callable[[str], None]=None) -> None` - Initialize Virtual Flet Navigator.
  - `navigate(route: str, page: Page, args: tuple[Any]=None) -> None` - Navigate to specific route. Specify `args` to transfer arguments to other page.
  - `render(page: Page, args: tuple[Any]=None) -> None` - Render current route. If there is no route like that throw ROUTE-404 (if specified). Should be called only one time.
  - `set_route_data(self, route: str, data: Any) -> int` - Set route data (cookies-like mechanism). Returns success/fail.
  - `get_route_data(self, route: str) -> Any` - Get route data.

Using example:

```python
from flet import app, Page

from flet_navigator import VirtualFletNavigator, PageData, Any, ROUTE_404

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

<hr>

<h3 align="center"><code>FletNavigator</code></h3>

- `FletNavigator` - Flet Navigator Class.
  - `page: Page = None` - Page.
  - `route: str = '/'` - Current route.
  - `routes: dict[str, Callable[[PageData], None]] = {}` - Registered routes.
  - `routes_data: dict[str, Any] = {}` - Routes data.
  - `route_changed_handler: Callable[[str], None] = None` - Route changed handler.<br><br>

  - `__init__(page: Page, routes: dict[str, Callable[[Page, 'VirtualFletNavigator', tuple[Any], str], None]], route_changed_handler: Callable[[str], None]=None) -> None` - Initialize Flet Navigator.
  - `navigate(route: str, page: Page, args: tuple[Any]=None) -> None` - Navigate to specific route. Specify `args` to transfer arguments to other page.
  - `render(page: Page, args: tuple[Any]=None, route_parameters: dict[str, Any]={}) -> None` - Render current route. If there is no route like that throw ROUTE-404 (if specified). Should be called only one time.
  - `set_route_data(self, route: str, data: Any) -> int` - Set route data (cookies-like mechanism). Returns success/fail.
  - `get_route_data(self, route: str) -> Any` - Get route data.

Using example:

```python
from flet import app, Page, WEB_BROWSER

from flet_navigator import FletNavigator, Any, ROUTE_404


def main_page(pg: PageData) -> None:
    ... # Main page content.

def second_page(pg: PageData) -> None:
    ... # Second page content.

def route_404(pg: PageData) -> None:
    ... # 404 page content.

def main(page: Page) -> None:
    # Initialize navigator.
    flet_navigator = FletNavigator(page, # Specify page.
        {
            '/': main_page, # Main page route,
            'second_page': second_page, # Second page route,
            ROUTE_404: route_404 # 404 page route
        }, lambda route: print(f'Route changed!: {route}') # Route change handler (optional).
    )

    # Render current page.
    flet_navigator.render(page)

app(target=main, view=WEB_BROWSER) # Non-Virtual Navigator recommended in web.
```

<hr>

<h3 align="center"><code>define_page</code></h3>

```define_page(path: str, name: str=None) -> Callable[[PageData], None]```

Used to import page from other file. Example:<br><br>

`second_page.py`

```python
# from flet import 

from flet_navigator import PageData


def second_page(pg: PageData) -> None:
    ... # Second page content.
```

<br>

`main.py`

```python
from flet_navigator import FletNavigator

def main(page: Page) -> None:
    flet_navigator = FletNavigator(page,
        {
            '/': main_page,
            'second_page': define_page('second_page'),
            ROUTE_404: route_404
        }, lambda route: print(f'Route changed!: {route}')
    )

    flet_navigator.render(page)

app(target=main, view=WEB_BROWSER) # Non-Virtual Navigator recommended in web.
```

<br>

If `name` is None, `path` is used as page name.

```python
define_page('second_page') # => second_page
define_page('path\\to\\page\\second_page') # => second_page
define_page('path/to/page/second_page') # => second_page
define_page('second_page', 'my_second_page_name') # => my_second_page_name
```

<hr>

<h3 align="center">Summary.</h3>
Summary! Now you know difference between virtual and non-virtual navigator, how to use navigator, etc! Good luck, have fun! But remember that project isn't finished!<br><br>

*Developer Note*: It would be great support for me if you'd added credits for FletNavigator! Optional!

<hr>

<p align="center"><b><i>FletNavigator V2.1.1</i></b></p>

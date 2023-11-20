<h1 align="center">FletNavigator v2.4.5 Documentation.</h1>

<h4 align="center">Menu:</h4>

- [Getting Started.](#getting-started)
- [General.](#general)
- [`VirtualFletNavigator`](#virtualfletnavigator)
- [`FletNavigator`](#fletnavigator)
- [`PageData`](#pagedata)
- [`NavigatorAnimation`](#navigatoranimation)
- [`route`](#route)
- [`define_page`](#define_page)
- [`template`](#template)
- [Summary.](#summary)

<hr>

<h3 align="center">Getting Started.</h3>
FletNavigator - Simple and fast navigator (router) for Flet (Python) that allows you to create multi-page applications!<br>It allows you to define own routes, provides built-in URL parameters support, animations, virtual routing, and more...<br><br>

Installation is quite easy: ```pip install flet_navigator```

> [!WARNING]  
> FletNavigator is in active development phase + only one developers works on this project. Please, be patient and report all bugs.

**FletNavigator Features**:
  - **✨ Simple installation and very simple using.**
  - **✨ Fast.**
  - **✨ Cookies-like mechanism.**
  - **✨ Animations between page change.**
  - **✨ Built-in smart URL parameters parser.**
  - **✨ Multiple routing modes.**
  - **✨ Templates.**
  - **✨ MVC Support.**
  - **✨ And more! And even more coming in future!**

**FletNavigator TODO**:
  - **NO TODO...**

**FletNavigator Known Bugs**:
  - **No known bugs...**

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

<br>

- **Homepages.**

Homepage is main page, that you can set with `set_homepage`, and navigate with `navigate_homepage`.

<br>

- **Typehints.**

- `Arguments = tuple[Any]` - Arguments type.
- `PageDefinition = Callable[[PageData], None]` - Page definition type.
- `TemplateDefinition = Callable[[PageData, Arguments], None]` - Template definition type.
- `RouteChangedHandler = Callable[[str], None]` - Route changed handler type.
- `Routes = dict[str, PageDefinition]` - Routes type.

<hr>

<h3 align="center"><code>VirtualFletNavigator</code></h3>

- `VirtualFletNavigator` - Virtual Flet Navigator Class.
  - `route: str = '/'` - Current route.
  - `routes: Routes = {}` - Registered routes.
  - `routes_data: dict[str, Any] = {}` - Routes data.
  - `homepage: str = '/'` - Homepage (main page).
  - `navigator_animation: NavigatorAnimation = NavigatorAnimation()` - Page switch animation.
  - `appbars: dict[int, Control] = {}` - Dictionary of appbars for each page (ID).
  - `route_changed_handler: RouteChangedHandler = None` - Route changed handler.<br><br>

  - `__init__(routes: dict[str, Callable[[Page, 'VirtualFletNavigator', tuple[Any], str], None]], route_changed_handler: Callable[[str], None]=None, navigator_animation: NavigatorAnimation=NavigatorAnimation()) -> None` - Initialize Virtual Flet Navigator.
  - `navigate(route: str, page: Page, args: tuple[Any]=None) -> None` - Navigate to specific route. Specify `args` to transfer arguments to other page.
  - `navigate_homepage(page: Page, args: tuple[Any]=None) -> None` - Navigate to homepage.
  - `render(page: Page, args: tuple[Any]=None) -> None` - Render current route. If there is no route like that throw ROUTE-404 (if specified). Should be called only one time.
  - `set_route_data(self, route: str, data: Any) -> int` - Set route data (cookies-like mechanism). Returns success/fail. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.
  - `get_route_data(self, route: str) -> Any` - Get route data. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.
  - `set_homepage(self, homepage: str) -> None` - Set homepage (main page). More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.

Using example:

```python
from flet import app, Page, Text

from flet_navigator import VirtualFletNavigator, PageData, ROUTE_404


def main_page(pg: PageData) -> None:
    pg.page.add(Text('Main page!'))

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
  - `routes: Routes = {}` - Registered routes.
  - `routes_data: dict[str, Any] = {}` - Routes data.
  - `homepage: str = '/'` - Homepage (main page).
  - `navigator_animation: NavigatorAnimation = NavigatorAnimation()` - Page switch animation.
  - `appbars: dict[int, Control] = {}` - Dictionary of appbars for each page (ID).
  - `route_changed_handler: RouteChangedHandler = None` - Route changed handler.<br><br>

  - `__init__(page: Page, routes: dict[str, Callable[[Page, 'VirtualFletNavigator', tuple[Any], str], None]], route_changed_handler: Callable[[str], None]=None, navigator_animation: NavigatorAnimation=NavigatorAnimation()) -> None` - Initialize Flet Navigator.
  - `navigate(route: str, page: Page, args: tuple[Any]=None) -> None` - Navigate to specific route. Specify `args` to transfer arguments to other page.
  - `navigate_homepage(page: Page, args: tuple[Any]=None) -> None` - Navigate to homepage (main page).
  - `render(page: Page, args: tuple[Any]=None, route_parameters: dict[str, Any]={}) -> None` - Render current route. If there is no route like that throw ROUTE-404 (if specified). Should be called only one time.
  - `set_route_data(route: str, data: Any) -> int` - Set route data (cookies-like mechanism). Returns success/fail. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.
  - `get_route_data(route: str) -> Any` - Get route data. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.
  - `set_homepage(homepage: str) -> None` - Set homepage (main page). More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.

Using example:

```python
from flet import app, Page, Text, WEB_BROWSER

from flet_navigator import FletNavigator ROUTE_404


def main_page(pg: PageData) -> None:
    pg.page.add(Text('Main page!'))

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

<h3 align="center"><code>PageData</code></h3>

- `PageData` - Used for transfering data between pages.
  - `page: Page = None` - Current page.
  - `navigator: Union['FletNavigator', 'VirtualFletNavigator'] = None` - Navigator.
  - `arguments: Arguments = None` - Arguments sent from previous page.
  - `previous_page: str = None` - Previous page.
  - `parameters: dict[str, Any] = None` - URL parameters. (Always `None` if `VirtualFletNavigator` used).
  - `page_id: int = None` - Page ID.<br><br>

  - `set_appbar(appbar: Control) -> None` - Set appbar for current page. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.

<hr>

<h3 align="center"><code>NavigatorAnimation</code></h3>

Class added in `V2.4.5` for implementing animation between page change. Example:

```python
from flet_navigator import NavigatorAnimation

def main(page: Page) -> None:
    navigator = FletNavigator({}, navigator_animation=NavigatorAnimation(NavigatorAnimation.SCALE))
```

<br>

- `NavigatorAnimation` - Class for implementing animations between page change.
  - `__init__(animation: int=FADE, smoothness: list[float]=SMOOTHNESS_9, delay: float=0.01, optimized_delay: float=0.001, optimization_threshold: int=5) -> None` - Initialize navigator animation.<br><br>

  - `NONE: int = 0` - None animation.
  - `FADE: int = 1` - Fade animation.
  - `SCALE: int = 2` - Scale animation.
  - `ROTATE: int = 3` - Rotate animation.
  - `SMOOTHNESS_1: list[float] = [0.9, 0.0]` - Smoothness level 1.
  - `SMOOTHNESS_2: list[float] = [0.9, 0.8, 0.0]` - Smoothness level 2.
  - `SMOOTHNESS_3: list[float] = [0.9, 0.8, 0.7, 0.0]` - Smoothness level 3.
  - `SMOOTHNESS_4: list[float] = [0.9, 0.8, 0.7, 0.6, 0.0]` - Smoothness level 4.
  - `SMOOTHNESS_5: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.0]` - Smoothness level 5.
  - `SMOOTHNESS_6: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.0]` - Smoothness level 6.
  - `SMOOTHNESS_7: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.0]` - Smoothness level 7.
  - `SMOOTHNESS_8: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.0]` - Smoothness level 8.
  - `SMOOTHNESS_9: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]` - Smoothness level 9.
  - `SMOOTHNESS_10: list[float] = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]` - Smoothness level 10.
  - `animation: int = FADE` - Selected animation.
  - `smoothness: list[float] = SMOOTHNESS_9` - Animation smoothness.
  - `delay: float = 0.01` - Animation delay.
  - `optimized_delay: float = 0.001` - Animation optimized delay (when a lot of controls on the page).
  - `optimization_threshold: int = 5` - Optimization threshold (maximal amount of controls that force optimized delay using instead of simple delay).<br><br>

  - `animate_out(page: Page, page_widgets: list[Control]) -> None` - Play out animation. Basically shouldn't be called by user.

<hr>

<h3 align="center"><code>route</code></h3>

`route` added in `V2.4.5` and used to specify routes using decorator. Example:
```
@route('/')
def main_page(pg: PageData) -> None:
    ...

def main(page: Page) -> None:
    navigator = FletNavigator({}) # Routes = {'/': main_page} / Supported for VirtualFletNavigator.
```

<hr>

<h3 align="center"><code>define_page</code></h3>

```define_page(path: str, name: str=None) -> PageDefinition```

Used to import page from other file. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>. Example:<br><br>

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

<h3 align="center"><code>template</code></h3>

```template(template_definition: TemplateDefinition, page_data: PageData, arguments: Arguments=None) -> Union[Control, None]```

Used to render template. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>. Example:<br>

```python
def go_to_button(pg: PageData, args: Arguments) -> None:
    pg.page.add(FilledButton(args[0], on_click=lambda _: pg.navigator.navigate(args[1], pg.page, args[2]))) # Or return FilledButton so we can do things with button later.

def main(pg: PageData) -> None:
    pg.page.add(Text('Hello World!'))

    template(go_to_button, pg, ('Go to second page.', 'second_page', None)) # Out is FilledButton with text 'Go to second page.', and on click redirect to `second_page` happens.
```

<hr>

<h3 align="center">Summary.</h3>
Summary! Now you know difference between virtual and non-virtual navigator, how to use navigator, etc! Good luck, have fun! But remember that project isn't finished!<br><br>

*Developer Note*: It would be great support for me if you'd added credits for FletNavigator! Optional!

<hr>

<p align="center"><b><i>FletNavigator V2.4.5</i></b></p>

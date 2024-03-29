<h1 align="center">FletNavigator v2.7.5 Documentation.</h1>

<h4 align="center">Menu:</h4>

- [Getting Started.](#getting-started)
- [General.](#general)
- [`VirtualFletNavigator`](#virtualfletnavigator)
- [`FletNavigator`](#fletnavigator)
- [`PageData`](#pagedata)
- [`NavigatorAnimation`](#navigatoranimation)
- [`route`](#route)
- [`define_page`](#define_page)
- [`parameters`](#parameters)
- [`template`](#template)
- [`global_template`](#global_template)
- [`render`](#render)
- [`anon`](#anon)
- [Summary.](#summary)

<hr>

<h3 align="center">Getting Started.</h3>
FletNavigator - Simple and fast navigator (router) for Flet (Python) that allows you to create multi-page applications!<br>It allows you to define own routes, provides built-in URL parameters support, animations, virtual routing, and more...<br><br>

Installation is quite easy: ```pip install flet_navigator```

> [!WARNING]  
> ~FletNavigator is in active development phase + only one developer works on this project. Please, be patient and report all bugs.~

> [!NOTE]
> Starting from `v2.7.5` FletNavigator is production-stable and almost completely ready to use. Any bug reports are very appreciated.

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
  - **No flexible support for widgets like `AppBar` and others.**

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

```flet_navigator::constructor:302: Warning: Wrong route name: "$my_route1У H". Allowed only digits and underscores.```

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

  - `__init__(routes: Routes={}, route_changed_handler: RouteChangedHandler=None, navigator_animation: NavigatorAnimation=NavigatorAnimation()) -> None` - Initialize Virtual Flet Navigator.
  - `navigate(route: str, page: Page, args: Arguments=None) -> None` - Navigate to specific route. Specify `args` to transfer arguments to other page.
  - `navigate_homepage(page: Page, args: Arguments=None) -> None` - Navigate to homepage.
  - `render(page: Page, args: Arguments=None) -> None` - Render current route. If there is no route like that throw ROUTE-404 (if specified). Should be called once.
  - `set_route_data(route: str, data: Any) -> int` - Set route data (cookies-like mechanism). Returns success/fail. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.
  - `get_route_data(route: str) -> Any` - Get route data. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.
  - `set_homepage(self, homepage: str) -> None` - Set homepage (main page). More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.

  - `@property virtual() -> bool[True]` - Is navigator virtual? Used in `PageData`. 

Using example:

```python
from flet import app, Text

from flet_navigator import PageData, render, anon, route


@route('/')
def main_page(pg: PageData) -> None:
  pg.add(Text('Main Page!')) # or `pg.page.add`.

@route('second_page')
def second_page(pg: PageData) -> None:
  ... # Second page content.

app(anon(render, virtual=True))
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

  - `__init__(page: Page, routes: Routes={}, route_changed_handler: RouteChangedHandler=None, navigator_animation: NavigatorAnimation=NavigatorAnimation()) -> None` - Initialize Flet Navigator.
  - `navigate(route: str, page: Page, args: Arguments=None, parameters: dict[str, Any]=None) -> None` - Navigate to specific route. Specify `args` to transfer arguments to other page. Specify `parameters` to add URL parameters.
  - `navigate_homepage(page: Page, args: Arguments=None, parameters: dict[str, Any]=None) -> None` - Navigate to homepage (main page).
  - `render(page: Page, args: tuple[Any]=None, route_parameters: dict[str, Any]={}) -> None` - Render current route. If there is no route like that throw ROUTE-404 (if specified). Should be called only one time.
  - `set_route_data(route: str, data: Any) -> int` - Set route data (cookies-like mechanism). Returns success/fail. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.
  - `get_route_data(route: str) -> Any` - Get route data. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.
  - `set_homepage(homepage: str) -> None` - Set homepage (main page). More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.

  - `@property virtual() -> bool[False]` - Is navigator virtual? Used in `PageData`. 

Using example:

```python
from flet import app, Text

from flet_navigator import PageData, render, anon, route


@route('/')
def main_page(pg: PageData) -> None:
    pg.add(Text('Main Page!')) # or `pg.page.add`.

@route('second_page')
def second_page(pg: PageData) -> None:
    ... # Second page content.

app(anon(render))
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
  - `add(*controls: Control) -> None` - Append control(s) to page. Works as same as `Page.add`.
  - `navigate(route: str, args: Arguments=None, parameters: dict[str, Any]=None) -> None` - Navigate to specific route. Parameters aren't used if navigator is virtual. Works as same as `PageData.navigator.navigate`.
  - `navigate_homepage(args: Arguments=None, parameters: dict[str, Any]=None) -> None` - Navigate to homepage. Parameters aren't used if navigator is virtual. Works as same as `PageData.navigator.navigate_homepage`.

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
  - `SHRINK: int = 3` - Shrink animation.
  - `ROTATE: int = 4` - Rotate animation.
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
```python
@route('/')
def main_page(pg: PageData) -> None:
    ...

def main(page: Page) -> None:
    navigator = FletNavigator() # Routes = {'/': main_page} / Supported for VirtualFletNavigator.
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

<h3 align="center"><code>parameters</code></h3>

```parameters(route: str, **_parameters: dict) -> str```

<code>parameters</code> function added in <code>v2.7.5</code> and used to append route with parameters.<br><br>

```python
parameters('route', param=1, param2=2, param3=3) # Returns 'route?param=1&param2=2&param3=3'.
```

<hr>

<h3 align="center"><code>template</code></h3>

```template(template_definition: Union[str, TemplateDefinition], page_data: PageData, arguments: Arguments=None) -> Union[Control, None]```

Used to render template. More <a href="https://github.com/xzripper/flet_navigator/issues/4#issuecomment-1817908000">detailed</a>.<br>

In `v2.7.5` template features are extended: added global templates. Now you can use `@global_template` to register template and call template just by it's name.

Example:<br>

```python
def local_template(pd: PageData, args: Arguments) -> Union[Control, None]:
    ... # Template content...

@global_template # or use @global_template(%TEMPLATE_NAME%) for custom name. So now template with name `my_global_template` is registered in global templates.
def my_global_template(pd: PageData, args: Arguments) -> Union[Control, None]:
    ... # Template content...

@route('/')
def index(pd: PageData) -> None:
    template(local_template) # Local template.

    template('my_global_template') # Global template.
```

<hr>

<h3 align="center">global_template.</h3>

```@global_template(template_name: str=None) -> Any```

Decorator used to register global templates.

```python
def local_template(pd: PageData, args: Arguments) -> Union[Control, None]:
    ... # Template content...

@global_template # or use @global_template(%TEMPLATE_NAME%) for custom name. So now template with name `my_global_template` is registered in global templates.
def my_global_template(pd: PageData, args: Arguments) -> Union[Control, None]:
    ... # Template content...
```

<hr>

<h3 align="center">render</h3>

```render(page: Page=None, routes: Routes={}, args: Arguments=None, parameters: dict[str, Any]=None, route_changed_handler: RouteChangedHandler=None, navigator_animation: NavigatorAnimation=NavigatorAnimation(), virtual: bool=False) -> None```

Shortcut for rendering page at start (`Nav(page?).render(page)`). Better use it with `anon`.

```python
@route('/')
def index(pd: PageData) -> None:
    ... # Index content...

app(lambda page: render(page))
```

<hr>

<h3 align="center">anon</h3>

```anon(function: Callable, args: Arguments=(), **kwargs: dict) -> Callable```

Function used to create anonymous functions. Anonymous function has one argument required - `page`.

```python
app(anon(render)) # instead of app(lambda page: render(page))
```

<hr>

<h3 align="center">Summary.</h3>
Summary! Now you know difference between virtual and non-virtual navigator, how to use navigator, etc! Good luck, have fun! But remember that project isn't finished!<br><br>

*Developer Note*: It would be great support for me if you'd added credits for FletNavigator! Optional!

<hr>

<p align="center"><b><i>FletNavigator V2.7.5</i></b></p>

<h1 align="center">FletNavigator V3.8.6</h1>
<p align="center">FletNavigator is a minimalistic, powerful, and extremely fast navigation management library designed for Flet applications. It simplifies the handling of routes and page transitions while delivering optimal performance. With its lightweight architecture, FletNavigator supports both virtual and public routing, enabling seamless navigation with or without public URLs. It allows dynamic page rendering, efficient management of URL parameters and arguments, and customizable route change callbacks. FletNavigator supports nested and parameterized routes, and provides built-in mechanisms for handling 404 errors. Its intuitive design and focus on speed make it an ideal choice for building responsive and robust Flet-based applications.</p>

## Table of Contents
- [Installation](#installation)
- [Classes](#classes)
  - [PageData](#pagedata)
  - [VirtualFletNavigator](#virtualfletnavigator)
  - [PublicFletNavigator](#publicfletnavigator)
- [Core Features](#core-features)
- [Aliases](#aliases)
- [Disabling FletNavigator logger](#disabling-fletnavigator-logger)

# Installation
To install FletNavigator use this command line: `pip install flet_navigator`. That's it!

# Classes
FletNavigator classes: `PageData`, `VirtualFletNavigator`, `PublicFletNavigator`.

## PageData
Represents data associated with a specific page in a navigation system.

This class holds information about the current page, its associated navigator, 
arguments and parameters passed from the previous page, and the page ID.
It provides methods to navigate between routes, manage the navigation bar, 
and more.

- **Attributes**:
    - `page: Page`    
        The current page instance.
    - `navigator: PublicFletNavigator | VirtualFletNavigator`    
        The navigator.
    - `arguments: Arguments`    
        Arguments passed from the previous page for context.
    - `parameters: RouteParameters`    
        URL parameters associated with the current route.
    - `page_id: int`    
        The unique identifier for this page.

- **Methods**:
    - `__init__(page: Page, navigator: PublicFletNavigator | VirtualFletNavigator, arguments: Arguments, parameters: RouteParameters, page_id: int) -> None`    
        Initialize a PageData instance.
    - `current_route() -> str`    
        Get the current route from the navigator.
    - `add(*controls: Control) -> None`    
        Add one or more controls to the current page.
    - `navigate(route: str, args: Arguments=(), parameters: RouteParameters={}) -> None`    
        Navigate to a specific route. If the navigator is virtual, parameters are not used.
    - `navigate_homepage(args: Arguments=(), parameters: RouteParameters={}) -> None`    
        Navigate to the homepage. If the navigator is virtual, parameters are not used.
    - `set_navbar(navbar: Control) -> None`    
        Set the navigation bar for the current page.
    - `del_navbar() -> None`    
        Remove the navigation bar for the current page.
    - `__repr__() -> str`    
        Represent the PageData instance as a string for debugging purposes.

## VirtualFletNavigator
Virtual navigator class.

Manages routing and navigation in a Flet application. It allows navigation between routes,
setting a homepage, and rendering pages based on the current route. This class provides virtual navigation,
where the route and page content are managed without public URL address.

- **Attributes**:
    - `route: str`    
        The current active route.
    - `routes: Routes`    
        A map of all supported routes in the application.
    - `homepage: str`    
        The route that acts as the homepage.
    - `navbars: dict[int, Control]`    
        A dictionary mapping page IDs to their corresponding navigation bars.
    - `route_change_callback: RouteChangeCallback`    
        A callback function that is triggered when the route changes.

- **Methods**:
    - `__init__(routes: Routes={}, route_change_callback: RouteChangeCallback=None) -> None`    
        Initialize the virtual navigator.
    - `navigate(route: str, page: Page, args: Arguments=()) -> None`    
        Navigate to a specific route in the application.
    - `navigate_homepage(page: Page, args: Arguments=()) -> None`    
        Navigate to the homepage route.
    - `set_homepage(homepage: str) -> None`    
        Set a new homepage route.
    - `render(page: Page, args: Arguments=()) -> None`    
        Render the current route on the provided page. If the route is not found, a 404 error page is shown.
    - `is_virtual() -> None`    
        Check if the navigator is virtual or public.

```python
from flet import app, Page, Text, TextButton

from flet_navigator import VirtualFletNavigator, PageData, route


@route('/')
def main(pg: PageData) -> None:
    pg.add(Text('Hello World!'))

    pg.add(TextButton('Navigate to the second page!', on_click=lambda _: pg.navigate('second')))

@route
def second(pg: PageData) -> None:
    pg.add(Text('I am the second page!'))

    pg.add(TextButton('Return to the homepage!', on_click=lambda _: pg.navigate_homepage()))

app(lambda page: VirtualFletNavigator().render(page))
```

## PublicFletNavigator
Public navigator class.

This class handles routing and navigation in a Flet application, managing routes, 
page rendering, and navigation between different pages. It supports navigating to 
specific routes, setting a homepage, and handling route changes. Works with the public URL addresses.

- **Attributes**:
    - `page: Page`    
        Page object representing the current page.
    - `route: str`    
        The current active route.
    - `routes: Routes`    
        A map of all supported routes in the application.
    - `homepage: str`    
        The homepage route.
    - `navbars: dict[int, Control]`    
        A dictionary mapping page IDs to their corresponding navigation bars.
    - `route_change_callback: RouteChangeCallback`    
        A callback function that is triggered when the route changes.

- **Methods**:
    - `__init__(page: Page, routes: Routes={}, route_change_callback: RouteChangeCallback=None) -> None`    
        Initialize the public navigator.
    - `navigate(route: str, page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None`    
        Navigate to a specific route in the application.
    - `navigate_homepage(page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None`    
        Navigate to the homepage route.
    - `render(page: Page, args: Arguments=(), route_parameters: RouteParameters={}) -> None`    
        Render the current route on the provided page. If the route is not found, a 404 error page is shown.
    - `set_homepage(homepage: str) -> None`    
        Set a new homepage route.
    - `is_virtual() -> None`    
        Check if the navigator is virtual or public.
    - `_nav_route_changed_callback(_) -> None`    
        Internal callback triggered when the route changes.

```python
from flet import app, Text, TextButton

from flet_navigator import PublicFletNavigator, PageData, route, ROUTE_404


@route('/')
def main(pg: PageData) -> None:
    pg.add(Text('Hello World!'))

    pg.add(TextButton('Navigate to the second page!', on_click=lambda _: pg.navigate('second', ('Hi!', ), {'msg':'Hello second page!'})))

@route
def second(pg: PageData) -> None:
    pg.add(Text(f'I am the second page! URL parameters: {str(pg.parameters)}, arguments: {str(pg.arguments)}'))

    pg.add(TextButton('Return to the homepage!', on_click=lambda _: pg.navigate_homepage()))

@route(ROUTE_404)
def route404(pg: PageData) -> None:
    pg.add(Text('Are you sure this page exists?'))

    pg.add(TextButton('Return to the homepage!', on_click=lambda _: pg.navigate_homepage()))

app(lambda page: PublicFletNavigator(page).render(page))
```

# Core Features

- `route(route: str | PageDefinition) -> Any`
    Link a route to the last initialized navigator. Associates a route with a page definition or adds a page definition as a decorator for a specified route.

```python
@route
def my_route(pg: PageData) -> None: # Now this route is available as 'my_route'.
    ...

@route('my_route_2')
def func(pg: PageData) -> None: # Now this route is available as 'my_route_2'.
    ...
```

- `load_page(path: str, name: str=None) -> PageDefinition`
    Load a page definition from a specified module. Dynamically imports a module and retrieves a page definition.

```python
PublicFletNavigator(page, {'loaded_route': load_page('my_page')}).render(page)
```

`my_page.py`
```python
from flet_navigator import PageData

def my_page(pg: PageData) -> None:
    ...
```

- `template(template_definition: str | TemplateDefinition, page_data: PageData, *arguments: Arguments) -> Control?`
    Render a template for the given page data and arguments. Supports retrieving a global template by name or using a callable template function.

```python
def my_local_template(pg: PageData, *args) -> None: # Also its possible to return the controls.
    ...

# Fetch/render a local template within your page.
template(my_local_template, page_data)
```

- `global_template(template_name: str=None) -> Any`
    Register a global template to the last initialized navigator. Associates a callable template with a name or uses the template function's name as the key.

```python
@global_template
def my_template(pg: PageData, *args) -> None: # Template is registered as 'my_template'.
    ...

@global_template('my_template_2')
def func(pg: PageData, *args) -> None: # Template is registered as 'my_template_2'.
    ...

# Fetch/render a local template within your page.
template('my_template', page_data)
template('my_template_2', page_data)
```

# Aliases

- **Arguments**    
    Alias for page-transferring arguments: `tuple[Any, ...]`.

- **PageDefinition**    
    Alias for page definition: `Callable[[PageData], None]`.

- **TemplateDefinition**    
    Alias for template definition: `Callable[[PageData, Arguments], Optional[Control]]`.

- **RouteChangeCallback**    
    Alias for route change callback: `Callable[[str], None]`.

- **Routes**    
    Alias for routes map: `dict[str, PageDefinition]`.

- **RouteParameters**    
    Alias for route parameters map: `dict[str, Union[str, int, bool, None]]`.

# Disabling FletNavigator logger
You can disable FletNavigator logger by setting `FN`'s logger `propagate` property to `False`.

```python
from logging import getLogger

# Append this line after the navigator has been initialized.
getLogger('FN').propagate = False
```

<hr><p align="center"><b>FletNavigator V3.8.6</b></p>

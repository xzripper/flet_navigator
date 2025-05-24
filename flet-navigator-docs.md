<h1 align="center">FletNavigator V3.9.7 Documentation</h1>
Minimalistic FletNavigator documentation. Yeah, just like the module itself.<br><br>

<a href="#ultimate-showcase">Ultimate showcase.</a>

<h4>Features I'd like to see in FletNavigator</h4>

- Routes' guards & evolved `RouteChangeCallback`'s.

<h2>Public Generic Globals</h2>

- `FLET_NAVIGATOR_VERSION` (`str`, `'3.9.7'`) - FN Version.
- `_DEFAULT_PAGE_404` (`PageDefinition`) - A page definition of 404 route. It's public but I don't really think you'll need this.
- `ROUTE_404` (`str`, `ROUTE-404`) - A constant string representing the 404 route type. It's akin to a form of identification.

<h2>Public Typehints/Aliases</h2>

- `Arguments` (`Union[Any, tuple[Any, ...]]`) - An alias for a page-transfering arguments.
- `PageDefinition` (`Callable[[PageData], None]`) - An alias for a page definition.
- `TemplateDefinition` (`Callable[[PageData, Arguments], Any]`) - An alias for a template definition.
- `RouteChangeCallback` (`Callable[[str], None]`) - An alias for a route change callback.
- `Routes` (`dict[str, PageDefinition]`) - An alias for a routes map.
- `RouteParameters` (`dict[str, Union[str, int, bool, None]]`) - An alias for a route parameters map.

<h2>Public Classes</h2>

- `PageData` (Just a class that contains page data and some utility functions for navigation):
  - Fields:
  - `page` (`Page`, `None`) - The current page instance.
  - `navigator` (`Union[PublicFletNavigator, VirtualFletNavigator]`, `None`) - The navigator.
  - `arguments` (`Arguments`, `None`) - Arguments passed from the previous page for context.
  - `parameters` (`RouteParameters`, `None`) - URL parameters associated with the current route.
  - `page_id` (`tuple[int, str]`, `None`) - The unique identifier for this page.
  - Methods:
  - `current_route() -> str` - Get the navigator's current route state.
  - `add(*controls: Control) -> None` - Add one or more controls to the current page.
  - `navigate(route: str, args: Arguments=(), parameters: RouteParameters={}) -> None` - Navigate to a specific route. If the navigator is virtual, parameters are not used.
  - `navigate_homepage(args: Arguments=(), parameters: RouteParameters={}) -> None` - Navigate to the homepage. If the navigator is virtual, parameters are not used.
  - `navigate_back(args: Arguments=(), parameters: RouteParameters={}) -> None` - Navigate back to the previous route. If the navigator is virtual, parameters are not used.
  - `set_navbar(navbar: Union[ConstrainedControl, AdaptiveControl]) -> None` - Set the navigation bar for the current page.
  - `delete_navbar() -> None` - Remove the navigation bar for the current page.

- `VirtualFletNavigator` (The Virtual Flet Navigator. It's just like the public one, but without URL parameters and visible routes):
  - Fields:
    - `route` (`str`, `'/'`) - The current active route.
    - `routes` (`Routes`, `{}`) - A map of all registered routes.
    - `previous_routes` (`list[str]`, `[]`) - List of previously visited routes.
    - `homepage` (`str`, `'/'`) - The homepage route.
    - `navbars` (`dict[int, Union[ConstrainedControl, AdaptiveControl]]`, `{}`) - A dictionary mapping page IDs to their corresponding navigation bars.
    - `route_change_callback` (`RouteChangeCallback`, `None`) - Optional callback on route change.
  - Methods:
    - `navigate(route: str, page: Page, args: Arguments = ()) -> None` - Navigate to a specific route.
    - `navigate_homepage(page: Page, args: Arguments = ()) -> None` - Navigate to the homepage.
    - `set_homepage(homepage: str) -> None` - Set the homepage route.
    - `navigate_back(page: Page, args: Arguments = (), parameters: RouteParameters = {}) -> None` - Navigate to the previous route.
    - `render(page: Page, args: Arguments = ()) -> None` - Render the current route on the provided page. Must be called only once in the main function.
    - `is_virtual() -> bool` - Check if the navigator is virtual.

- `PublicFletNavigator` (The Public Flet Navigator. It's just like the virtual one, but with URL parameters and visible routes.):
  - Fields:
    - `page` (`Page`, `None`) - The current page instance.
    - `route` (`str`, `'/'`) - The current active route.
    - `routes` (`Routes`, `{}`) - A map of all registered routes.
    - `previous_routes` (`list[str]`, `[]`) - List of previously visited routes.
    - `homepage` (`str`, `'/'`) - The homepage route.
    - `navbars` (`dict[int, Union[ConstrainedControl, AdaptiveControl]]`, `{}`) - A dictionary mapping page IDs to their corresponding navigation bars.
    - `route_change_callback` (`RouteChangeCallback`, `None`) - Optional callback on route change.
  - Methods:
    - `navigate(route: str, page: Page, args: Arguments = (), parameters: RouteParameters = {}) -> None` - Navigate to a specific route.
    - `navigate_homepage(page: Page, args: Arguments = (), parameters: RouteParameters = {}) -> None` - Navigate to the homepage.
    - `set_homepage(homepage: str) -> None` - Set the homepage route.
    - `navigate_back(page: Page, args: Arguments = (), parameters: RouteParameters = {}) -> None` - Navigate to the previous route.
    - `render(page: Page, args: Arguments = (), route_parameters: RouteParameters = {}) -> None` - Render the current route. Must be called only once in the main function.
    - `is_virtual() -> bool` - Check if the navigator is virtual.

<h2>Utilities</h2>

- `route(route: Union[str, PageDefinition]) -> Any`:

Link a route to the last initialized navigator.

This function registers the route and associates it with a given page definition.
The only difference is the name. You can specify the name in the first argument.
or this function will fetch the given function name automatically.

- `load_page(path: str, name: Optional[str]=None) -> PageDefinition`:

Load a page definition from a specified module.

Let me explain this technically: it replaces all the system path separators with a dot.
After loading the module by its path, it loads the page definition function.
The function name is determined by the path. If a name is specified, then it loads the specified name.
Otherwise, it uses the last name in the path.

Can throw `ModuleNotFoundError` and `AttributeError`.

- `template(template_definition: Union[str, TemplateDefinition], page_data: PageData, arguments: Arguments=()) -> Optional[Any]`:

Render a template for the given page data and arguments.

If `template_definition` is a string, then it's a global template.
The function will try to find the template you defined earlier via `@global_template` in the list of global templates.
If `template_definition` is a callable, then it's a local template.
The template will be rendered by calling the template function.

P.S I question the usefulness of local templates. Are they useful at all?

- `global_template(template_name: Optional[str]=None) -> Any`:

Register a global template to the last initialized navigator.

This function registers the template and associates it with a given template definition.
The only difference is the name. You can specify the name in the first argument.
or this function will fetch the given template function name automatically.

<h2>Ultimate showcase</h2>
Example that shows almost all features FletNavigator has.

Note: All redirects to `/` page with parameters will result in error (non-fatal log message) because index/main route doesn't support parameters.

`main.py`

```python
# Flet
from flet import (
    Text, TextField, FilledButton,
    Icon, IconButton, AppBar,
    Icons, Colors, app, WEB_BROWSER
)

# Flet Navigator
from flet_navigator import (
    PublicFletNavigator, PageData, Arguments, # Main classes & arguments alias
    route, template, global_template, load_page, # Utility functions
    ROUTE_404, FLET_NAVIGATOR_VERSION # Constants
)

# Try-Except evaluation utility function
def evaluate(string: str) -> object:
    try:
        return eval(string)
    except Exception as exc:
        print(exc)

# --- Global Template Definition ---
@global_template
def homepage_setter(pg: PageData, args: Arguments) -> None:
    pg.add(hp := TextField(hint_text=f'New homepage address {args}'))

    pg.add(FilledButton(
        'Submit new homepage',
        on_click=lambda _: pg.navigator.set_homepage(hp.value)
    ))

# --- Local Template Definition ---
def fn_version_local(pg: PageData, args: Arguments) -> None:
    pg.add(Text(f'FletNavigator {FLET_NAVIGATOR_VERSION} ({args})'))

# --- Main Page Definition ---
@route('/')
def main(pg: PageData) -> None:
    # --- Adding Controls ---
    # --- Generic data like arguments, parameters, current_route, etc ---
    pg.add(Text('Main page!', size=30))
    pg.add(Text(f'Arguments from the previous page: {pg.arguments}', size=15))
    pg.add(Text('Parameters from the previous page: not supported on /', size=15))
    pg.add(Text(f'Current route: {pg.current_route()}', size=15))
    pg.add(Text(f'Previous routes: {pg.navigator.previous_routes}', size=15))
    pg.add(Text(f'Homepage: {pg.navigator.homepage}', size=15))

    pg.add(args := TextField(hint_text='Arguments for the next page as a Python code.', value='[set((1, 2, 3)), 4, (5, )]'))
    pg.add(value := TextField(hint_text='Enter a random text/number/whatever', value='Hello World!'))

    # --- Back Navigation ---
    pg.add(
        FilledButton(
            'Go back',
            on_click=lambda _: # 'lambda _:' Flet requires function to spare first argument for event
            pg.navigate_back( # Navigate back
                evaluate(args.value), # Arguments
                {'value': value.value} # Parameters
            )
    ))

    pg.add(
        FilledButton(
            'Go to the second page',
            on_click=lambda _: # 'lambda _:' Flet requires function to spare first argument for event
            pg.navigate( # Navigate to a specific route
                'second', # Route
                evaluate(args.value), # Arguments
                {'value': value.value} # Parameters
            )
    ))

    pg.add(
        FilledButton(
            'Go to the third page',
            # Same as previous navigation operation.
            on_click=lambda _:
            pg.navigate(
                'third',
                evaluate(args.value),
                {'value': value.value}
            )
    ))

    # --- Render Global Template ---
    template(
        'homepage_setter', # Template name
        pg, # Page data reference
        ('main') # Arguments (can be tuple or single argument)
    )

    # --- Render Local Template ---
    template(fn_version_local, pg, ('main'))

    # --- Set navigation bar for this page ---
    pg.set_navbar(AppBar(
        leading=Icon(Icons.HOME),
        bgcolor=Colors.INDIGO_700,
        title=Text('Home'),
        actions=[IconButton(Icons.SUNNY)]
    ))

    # --- Delete/de-register/unhook navbar ---
    # pg.delete_navbar()

# --- Second page definition (function's name as the route name) ---
# No big difference between this function and the first one.
@route
def second(pg: PageData) -> None:
    pg.add(Text('Second page!', size=30))
    pg.add(Text(f'Arguments from the previous page: {pg.arguments}', size=15))
    pg.add(Text(f'Parameters from the previous page: {pg.parameters}', size=15))
    pg.add(Text(f'Current route: {pg.current_route()}', size=15))
    pg.add(Text(f'Previous routes: {pg.navigator.previous_routes}', size=15))
    pg.add(Text(f'Homepage: {pg.navigator.homepage}', size=15))

    pg.add(args := TextField(hint_text='Arguments for the next page as a Python code.', value='lambda x, y: x + y'))
    pg.add(value := TextField(hint_text='Enter a random text/number/whatever', value='Wello Horld!'))

    pg.add(
        FilledButton(
            'Go back',
            on_click=lambda _: pg.navigate_back(evaluate(args.value), {'value': value.value})
    ))

    pg.add(
        FilledButton(
            'Return to the homepage',
            on_click=lambda _: pg.navigate_homepage(evaluate(args.value), {'value': value.value})
    ))

    pg.add(
        FilledButton(
            'Go to the third page',
            on_click=lambda _: pg.navigate('third', evaluate(args.value), {'value': value.value})
    ))

    template('homepage_setter', pg, ('second'))

    template(fn_version_local, pg, ('second'))

    pg.set_navbar(AppBar(
        leading=Icon(Icons.ABC),
        bgcolor=Colors.BLUE_GREY_500,
        title=Text('Second page'),
        actions=[IconButton(Icons.CLOUD)]
    ))

# --- Route 404 Handling ---
# @route(ROUTE_404)
# def invalid_route(pg: PageData) -> None:
#    pg.add(Text("Invalid route..."))
#    pg.add(FilledButton("Go back", on_click=lambda _: pg.navigate_back()))

# Run the application.
app(lambda page: PublicFletNavigator(
    page, # Flet's page
    #        Loads external route from third.py: abc function.
    {'third': load_page('third', 'abc')} # Old way to specify routes; 
                                         # but still required for the external routes
    ).render(page) # Render the page.
, view=WEB_BROWSER)

# Equivalent to:
"""
def main(page: Page) -> None:
    PublicFletNavigator(page, {'third': load_page('third', 'abc')}, view=WEB_BROWSER).render(page)

app(main)
"""
```

`third.py`

```python
from flet import Text, TextField, FilledButton, AppBar, Colors, Icons, Icon, IconButton

from flet_navigator import PageData, template


def evaluate(string: str) -> object:
    try:
        return eval(string)
    except Exception as exc:
        print(exc)

# --- External route ---
# No big difference between other routes.
def abc(pg: PageData) -> None:
    pg.add(Text('Third external page!', size=30))
    pg.add(Text(f'Arguments from the previous page: {pg.arguments}', size=15))
    pg.add(Text(f'Parameters from the previous page: {pg.parameters}', size=15))
    pg.add(Text(f'Current route: {pg.current_route()}', size=15))
    pg.add(Text(f'Previous routes: {pg.navigator.previous_routes}', size=15))
    pg.add(Text(f'Homepage: {pg.navigator.homepage}', size=15))

    pg.add(args := TextField(hint_text='Arguments for the next page as a Python code.', value='"hello".encode("ascii")'))
    pg.add(value := TextField(hint_text='Enter a random text/number/whatever', value='Bello!'))

    pg.add(
        FilledButton(
            'Go back',
            on_click=lambda _:
            pg.navigate_back(
                evaluate(args.value),
                {'value': value.value}
            )
    ))

    pg.add(
        FilledButton(
            'Return to the homepage',
            on_click=lambda _:
            pg.navigate_homepage(
                evaluate(args.value),
                {'value': value.value}
            )
    ))

    pg.add(
        FilledButton(
            'Go to the second page',
            on_click=lambda _:
            pg.navigate(
                'second',
                evaluate(args.value),
                {'value': value.value}
            )
    ))

    template('homepage_setter', pg, ('third'))

    # Can't render template because it's local and was defined only in main.py
    # template(fn_version_local)

    pg.add(Text('Can\'t render fn_version_local: template is local'))

    pg.set_navbar(AppBar(
        leading=Icon(Icons.AC_UNIT),
        bgcolor=Colors.DEEP_PURPLE_900,
        title=Text('Third page'),
        actions=[IconButton(Icons.ACCESS_TIME)]
    ))
```

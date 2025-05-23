<h1 align="center">FletNavigator V3.9.6 Documentation</h1>
Minimalistic FletNavigator documentation. Yeah, just like the module itself.

<h2>Public Generic Globals</h2>

- `FLET_NAVIGATOR_VERSION` (`str`, `'3.9.6'`) - FN Version.
- `_DEFAULT_PAGE_404` (`PageDefinition`) - A page definition of 404 route. It's public but I don't really think you'll need this.
- `ROUTE_404` (`str`, `ROUTE-404`) - A constant string representing the 404 route type. It's akin to a form of identification.

<h2>Public Typehints/Aliases</h2>

- `Arguments` (`tuple[Any, ...]`) - An alias for a page-transfering arguments.
- `PageDefinition` (`Callable[[PageData], None]`) - An alias for a page definition.
- `TemplateDefinition` (`Callable[[PageData, Arguments], Optional[Control]]`) - An alias for a template definition.
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
  - `set_navbar(navbar: Control) -> None` - Set the navigation bar for the current page.
  - `delete_navbar() -> None` - Remove the navigation bar for the current page.

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

"""FletNavigator is a minimalistic, powerful, and extremely fast navigation management library designed for Flet applications. It simplifies the handling of routes and page transitions while delivering optimal performance. With its lightweight architecture, FletNavigator supports both virtual and public routing, enabling seamless navigation with or without public URLs. It allows dynamic page rendering, efficient management of URL parameters and arguments, and customizable route change callbacks. FletNavigator supports nested and parameterized routes, and provides built-in mechanisms for handling 404 errors. Its intuitive design and focus on speed make it an ideal choice for building responsive and robust Flet-based applications."""

from flet import Page, Control, Text, IconButton

from urllib.parse import parse_qs, urlsplit, unquote

from logging import basicConfig, getLogger, ERROR

from re import compile as re_compile

from importlib import import_module

from typing import Union, Optional, Callable, Any


_pre_def_routes: 'Routes' = {}


_global_templates: dict[str, 'TemplateDefinition'] = {}


_url_fn_space_chr: str = '<FN385S>'


FLET_NAVIGATOR_VERSION: str = '3.8.5'
"""The version of the Flet Navigator."""


ROUTE_404: str = 'ROUTE-404'
"""A constant string representing the 404 route type.

Used to specify a custom route for handling 404 errors (Page Not Found) in web applications. 
This can be customized for routing or error handling purposes."""


Arguments = tuple[Any, ...]
"""Alias for page-transfering arguments."""


class PageData:
    """Represents data associated with a specific page in a navigation system.

    This class holds information about the current page, its associated navigator, 
    arguments and parameters passed from the previous page, and the page ID.
    It provides methods to navigate between routes, manage the navigation bar, 
    and more."""

    page: Page = None
    """The current page instance."""

    navigator: Union['PublicFletNavigator', 'VirtualFletNavigator'] = None
    """The navigator."""

    arguments: Arguments = None
    """Arguments passed from the previous page for context."""

    parameters: 'RouteParameters' = None
    """URL parameters associated with the current route."""

    page_id: int = None
    """The unique identifier for this page."""

    def __init__(self, page: Page, navigator: Union['PublicFletNavigator', 'VirtualFletNavigator'], arguments: Arguments, parameters: 'RouteParameters', page_id: int) -> None:
        """Initialize a PageData instance."""
        self.page = page

        self.navigator = navigator

        self.arguments = arguments

        self.parameters = parameters

        self.page_id = page_id

    def current_route(self) -> str:
        """Get the current route from the navigator."""
        return self.navigator.route

    def add(self, *controls: Control) -> None:
        """Add one or more controls to the current page."""
        self.page.add(*controls)

    def navigate(self, route: str, args: Arguments=(), parameters: 'RouteParameters'={}) -> None:
        """Navigate to a specific route. If the navigator is virtual, parameters are not used."""
        if self.navigator.virtual:
            self.navigator.navigate(route, self.page, args)

        else:
            self.navigator.navigate(route, self.page, args, parameters)

    def navigate_homepage(self, args: Arguments=(), parameters: 'RouteParameters'={}) -> None:
        """Navigate to the homepage. If the navigator is virtual, parameters are not used."""
        if self.navigator.virtual:
            self.navigator.navigate_homepage(self.page, args)

        else:
            self.navigator.navigate_homepage(self.page, args, parameters)

    def set_navbar(self, navbar: Control) -> None:
        """Set the navigation bar for the current page."""
        self.page.appbar = navbar

        self.navigator.navbars[self.page_id] = navbar

    def del_navbar(self) -> None:
        """Remove the navigation bar for the current page."""
        self.page.appbar = None

        if self.page_id in self.navigator.navbars:
            self.navigator.navbars.pop(self.page_id)

    def __repr__(self) -> str:
        """Represent the PageData instance as a string for debugging purposes."""
        return f'{self.previous_page} -> {self.navigator.route} [{"NO-ARGUMENTS" if not self.arguments else self.arguments}, {"NO-PARAMETERS" if len(self.parameters) <= 0 else self.parameters}] ({self.page_id}) (NAVIGATOR-OBJECT {self.navigator})'


PageDefinition = Callable[[PageData], None]
"""Alias for page definition."""

TemplateDefinition = Callable[[PageData, Arguments], Optional[Control]]
"""Alias for template definition."""

RouteChangeCallback = Callable[[str], None]
"""Alias for route change callback."""

Routes = dict[str, PageDefinition]
"""Alias for routes map."""

RouteParameters = dict[str, Any]
"""Alias for route parameters map."""


_DEFAULT_PAGE_404: PageDefinition = lambda pg: (
    globals().__setitem__('_FNDP404_PRE_H_A', pg.page.horizontal_alignment),
    globals().__setitem__('_FNDP404_PRE_V_A', pg.page.vertical_alignment),

    globals().__setitem__('_FNDP404_CLOSED', False),

    setattr(pg.page, 'horizontal_alignment', 'center'),
    setattr(pg.page, 'vertical_alignment', 'center'),

    pg.add(Text('Not Found', size=100, tooltip=f'No defined route: "{pg.current_route()}".')),

    pg.add(IconButton(
        'door_back_door_outlined', 'white', 60,

        on_click=lambda _: (
            pg.page.clean(),

            setattr(pg.page, 'horizontal_alignment', globals().get('_FNDP404_PRE_H_A')),
            setattr(pg.page, 'vertical_alignment', globals().get('_FNDP404_PRE_V_A')),

            globals().__setitem__('_FNDP404_CLOSED', True),

            pg.navigate_homepage()
        ), tooltip='Return to the homepage.'
    ))
)
"""Default route-404 handler."""


class AbstractFletNavigator:
    @staticmethod
    def init_nav(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], /, page: Page=None, routes: Routes={}, route_change_callback: RouteChangeCallback=None) -> None:
        basicConfig(format=f'%(name)s %(levelname)s: %(message)s')

        nav._logger = getLogger(f'FN')

        nav._logger.setLevel(ERROR)

        nav._afn_vroute = re_compile(r'^[a-zA-Z_]\w*$')

        if page:
            nav._afn_proute = re_compile(r'^[a-zA-Z_]\w*\?\w+=([\w+~`!@"#№$;%^:*-,.<>\'{}\[\]()-]+)(?:&\w+=([\w+~`!@"#№$;%^:*-,.<>\'{}\[\]()-]+))*$')
            nav._afn_floatstr = re_compile(r'^-?\d+\.\d+$')

            nav.page = page

            nav.virtual = False

        else:
            nav.virtual = True

        nav.routes = routes

        nav.route_change_callback = route_change_callback

        if not nav.is_virtual():
            page.on_route_change = nav._nav_route_changed_callback

        routes_to_delete = []

        for route in nav.routes:
            if route != '/' and route != ROUTE_404:
                if not re_compile(nav._afn_vroute).match(route):
                    routes_to_delete.append(route)

                    nav._logger.error(f'Invalid route name: "{route}". Route names must start with a letter or underscore and contain only alphanumeric characters or underscores).')

        for route_to_delete in routes_to_delete:
            nav.routes.pop(route_to_delete)

        for route in _pre_def_routes:
            nav.routes[route] = _pre_def_routes[route]

    @staticmethod
    def navigate(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], /, route: str, page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None:
        if nav.is_virtual() and '?' in route:
            route = route.split('?')[0]

            nav._logger.error("The VirtualFletNavigator does not support URL parameters. Use page arguments instead, or switch to the PublicFletNavigator for full URL parameters support.")

        nav.route = route

        if not nav.is_virtual():
            nav._nav_temp_args = args

            page.go(AbstractFletNavigator.fparams(route, **parameters))

        else:
            nav.render(page, args)

    @staticmethod
    def render(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], /, page: Page, args: Arguments=(), route_parameters: RouteParameters={}) -> None:
        if nav.route not in nav.routes:
            page.clean()

            if nav.route_change_callback:
                nav.route_change_callback(nav.route)

            if ROUTE_404 in nav.routes:
                page.appbar = nav.navbars.get(ROUTE_404)

                nav.routes[ROUTE_404](PageData(page, nav, args, route_parameters, ROUTE_404))

            else:
                _DEFAULT_PAGE_404(PageData(page, nav, args, route_parameters, ROUTE_404))

            nav._logger.error(f'The route "{nav.route}" does not exist in the defined routes. Unable to render the page.')

        else:
            page.clean()

            page_id = list(nav.routes.keys()).index(nav.route) + 1

            page.appbar = nav.navbars.get(page_id)

            nav.routes[nav.route](PageData(page, nav, args, route_parameters, page_id))

            page.update()

            if nav.route_change_callback:
                nav.route_change_callback(nav.route)

    @staticmethod
    def fparams(route: str, **_parameters: dict) -> str:
        return f'{route}?{"&".join(f"{key}={value}" for key, value in _parameters.items())}' if len(_parameters) > 0 else route


class VirtualFletNavigator:
    """Virtual navigator class.

    Manages routing and navigation in a Flet application. It allows navigation between routes,
    setting a homepage, and rendering pages based on the current route. This class provides virtual navigation,
    where the route and page content are managed without public URL address."""

    route: str = '/'
    """The current active route."""

    routes: Routes = {}
    """A map of all supported routes in the application."""

    homepage: str = '/'
    """The route that acts as the homepage."""

    navbars: dict[int, Control] = {}
    """A dictionary mapping page IDs to their corresponding navigation bars."""

    route_change_callback: RouteChangeCallback = None
    """A callback function that is triggered when the route changes."""

    def __init__(self, routes: Routes={}, route_change_callback: RouteChangeCallback=None) -> None:
        """Initialize the virtual navigator."""
        AbstractFletNavigator.init_nav(self, routes=routes, route_change_callback=route_change_callback)

    def navigate(self, route: str, page: Page, args: Arguments=()) -> None:
        """Navigate to a specific route in the application."""
        AbstractFletNavigator.navigate(self, route, page, args)

    def navigate_homepage(self, page: Page, args: Arguments=()) -> None:
        """Navigate to the homepage route."""
        self.navigate(self.homepage, page, args)

    def set_homepage(self, homepage: str) -> None:
        """Set a new homepage route."""
        self.homepage = homepage

    def render(self, page: Page, args: Arguments=()) -> None:
        """Render the current route on the provided page. If the route is not found, a 404 error page is shown."""
        AbstractFletNavigator.render(self, page, args)

    def is_virtual(self) -> None:
        """Check if the navigator is virtual or public."""
        return getattr(self, 'virtual', None)


class PublicFletNavigator:
    """Public navigator class.

    This class handles routing and navigation in a Flet application, managing routes, 
    page rendering, and navigation between different pages. It supports navigating to 
    specific routes, setting a homepage, and handling route changes. Works with the public URL addresses."""

    page: Page = None
    """Page object representing the current page."""

    route: str = '/'
    """The current active route."""

    routes: Routes = {}
    """A map of all supported routes in the application."""

    homepage: str = '/'
    """The homepage route."""

    navbars: dict[int, Control] = {}
    """A dictionary mapping page IDs to their corresponding navigation bars."""

    route_change_callback: RouteChangeCallback = None
    """A callback function that is triggered when the route changes."""

    _nav_temp_args: Arguments = None

    def __init__(self, page: Page, routes: Routes={}, route_change_callback: RouteChangeCallback=None) -> None:
        """Initialize the public navigator."""
        AbstractFletNavigator.init_nav(self, page, routes, route_change_callback)

    def navigate(self, route: str, page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None:
        """Navigate to a specific route in the application."""
        AbstractFletNavigator.navigate(self, route, page, args, parameters)

    def navigate_homepage(self, page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None:
        """Navigate to the homepage route."""
        self.navigate(self.homepage, page, args, parameters)

    def render(self, page: Page, args: Arguments=(), route_parameters: RouteParameters={}) -> None:
        """Render the current route on the provided page. If the route is not found, a 404 error page is shown."""
        AbstractFletNavigator.render(self, page, args, route_parameters)

    def set_homepage(self, homepage: str) -> None:
        """Set a new homepage route."""
        self.homepage = homepage

    def is_virtual(self) -> None:
        """Check if the navigator is virtual or public."""
        return getattr(self, 'virtual', None)

    def _nav_route_changed_callback(self, _) -> None:
        route: str = self.page.route.replace(' ', _url_fn_space_chr).replace('%20', _url_fn_space_chr).replace('+', _url_fn_space_chr)

        route = route[1:] if route.startswith('/') and len(route) >= 2 else route

        split_url = urlsplit(route)

        broute, qstr = split_url.path, split_url.query

        parameters = {}

        if self._afn_proute.match(route):
            _parsed_params = parse_qs(qstr, True)

            for key, values in _parsed_params.items():
                if not key.isalpha():
                    self._logger.error(f'Invalid key name: "{key}". The key is expected to be a string.')

                    continue

                value = unquote(values[0]) if values else ''

                if value.isdigit(): parameters[key] = int(value)
                elif self._afn_floatstr.match(value): parameters[key] = float(value)
                elif value in ['True', 'False']: parameters[key] = value == 'True'
                elif value == 'None': parameters[key] = None
                else: parameters[key] = value.replace(_url_fn_space_chr, ' ')

        self.route = broute

        if not globals().get('_FNDP404_CLOSED'):
            setattr(self.page, 'horizontal_alignment', globals().get('_FNDP404_PRE_H_A')),
            setattr(self.page, 'vertical_alignment', globals().get('_FNDP404_PRE_V_A')),

        self.render(self.page, self._nav_temp_args, parameters)

        self._nav_temp_args = None


def route(route: Union[str, PageDefinition]) -> Any:
    """Link a route to the last initialized navigator.

    This function either registers a route as a string, associating it with a given 
    page definition or adds a page definition as a decorator for a specified route."""
    if isinstance(route, Callable):
        _pre_def_routes[route.__name__] = route

    else:
        def _route_decorator(page_definition: PageDefinition) -> None:
            _pre_def_routes[route] = page_definition

        return _route_decorator


def load_page(path: str, name: Optional[str]=None) -> PageDefinition:
    """Load a page definition from a specified module.

    This function dynamically imports a module based on the provided `path` and attempts 
    to retrieve a page definition. If a `name` is specified, it looks for the page definition 
    with that name; otherwise, it uses the last part of the `path` as the name.
    
    Raises `ImportError` if the module or the specified page definition cannot be loaded."""
    path = path.replace('\\', '.').replace('/', '.')

    page = None

    try:
        page = getattr(import_module(path), path.split('.')[-1] if not name else name)
    except AttributeError:
        raise ImportError(f'Failed to load page definition: "{path}".')

    return page


def template(template_definition: Union[str, TemplateDefinition], page_data: PageData, arguments: Arguments=()) -> Optional[Control]:
    """Render a template for the given page data and arguments.

    This function checks if the `template_definition` is a string or a callable. 
    If it's a string, it attempts to retrieve a registered global template by that name.
    If the template is not found, it logs an error. If it's a callable (template function),
    it directly calls it with the provided `page_data` and `arguments`."""
    if isinstance(template_definition, str):
        if template_definition in _global_templates:
            return _global_templates[template_definition](page_data, arguments)

        else:
            page_data.navigator._logger.error(f'No template found with the name: "{template_definition}". Ensure the template is registered and its name is correct.')

    else:
        return template_definition(page_data, arguments)


def global_template(template_name: Optional[str]=None) -> Any:
    """Register a global template to the last initialized navigator.

    This function registers a template either by associating a callable template
    with a name or by using a provided template name. If a string `template_name`
    is passed, it registers the template under that name. If no name is provided,
    the template function's name is used as the key."""
    if isinstance(template_name, Callable):
        _global_templates[template_name.__name__] = template_name

    else:
        def _global_template(template: TemplateDefinition) -> None:
            _global_templates[template.__name__ if not template_name or not isinstance(template_name, str) else template_name] = template

        return _global_template

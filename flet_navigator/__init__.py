"""A minimalist module for navigation in Flet that combines speed and simplicity."""

from importlib import import_module

from logging import ERROR, basicConfig, getLogger

from re import compile as re_compile

from urllib.parse import parse_qs, unquote, urlsplit

from typing import Any, Callable, Optional, Union

from flet import Control, Page, Text, IconButton


_pre_def_routes: 'Routes' = {}


_global_templates: dict[str, 'TemplateDefinition'] = {}


_url_fn_space_chr: str = '<FN31011S>'


FLET_NAVIGATOR_VERSION: str = '3.10.11'
"""The version of the Flet Navigator."""


_DEFAULT_PAGE_404: 'PageDefinition' = lambda pg: (
    globals().__setitem__('_FNDP404_PRE_H_A', pg.page.horizontal_alignment),
    globals().__setitem__('_FNDP404_PRE_V_A', pg.page.vertical_alignment),

    globals().__setitem__('_FNDP404_CLOSED', False),

    setattr(pg.page, 'horizontal_alignment', 'center'),
    setattr(pg.page, 'vertical_alignment', 'center'),

    pg.add(Text('Not Found', size=100, tooltip=f'Invalid route: "{pg.current_route()}".')),

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
"""A default Route-404 handler."""


ROUTE_404: str = 'ROUTE-404'
"""A constant string representing the 404 route type.

Used to specify a custom route for handling 404 errors (Page Not Found) in applications. 
This can be customized for routing or error handling purposes."""


Arguments = Union[Any, tuple[Any, ...]]
"""An alias for a page-transferring arguments."""

PageDefinition = Callable[['RouteContext'], None]
"""An alias for a page definition."""

TemplateDefinition = Callable[['RouteContext', Arguments], Any]
"""An alias for a template definition."""

RouteChangeCallback = Callable[['RouteContext'], None]
"""An alias for a route change callback."""

Routes = dict[str, PageDefinition]
"""An alias for a routes map."""

RouteParameters = dict[str, Union[str, int, bool, None]]
"""An alias for a route parameters map."""

RouteProperties = dict[int, dict[str, Any]]
"""An alias for a route properties map."""


class RouteContext:
    """Route context class used for transferring data between routes and providing Navigator shortcuts."""

    page: Page = None
    """The current page instance."""

    navigator: Union['PublicFletNavigator', 'VirtualFletNavigator'] = None
    """The navigator that created this RouteContext instance."""

    arguments: Arguments = None
    """Arguments passed from the previous page for context."""

    parameters: 'RouteParameters' = None
    """URL parameters associated with the current route."""

    route_id: tuple[int, str] = None
    """The unique identifier for this page."""

    def __init__(self, page: Page, navigator: Union['PublicFletNavigator', 'VirtualFletNavigator'], arguments: Arguments, parameters: 'RouteParameters', route_id: tuple[int, str]) -> None:
        """Initialize a RouteContext instance."""
        self.page = page

        self.navigator = navigator

        self.arguments = arguments

        self.parameters = parameters

        self.route_id = route_id

    def add(self, *controls: Control) -> None:
        """Add one or more controls to the current page."""
        self.page.add(*controls)

    def navigate(self, route: str, args: Arguments=(), **parameters: RouteParameters) -> None:
        """Navigate to a specific route. If the navigator is virtual, parameters are not used."""
        if self.navigator.is_virtual():
            self.navigator.navigate(route, self.page, args)

        else:
            self.navigator.navigate(route, self.page, args, parameters)

    def navigate_homepage(self, args: Arguments=(), **parameters: RouteParameters) -> None:
        """Navigate to the homepage. If the navigator is virtual, parameters are not used."""
        if self.navigator.is_virtual():
            self.navigator.navigate_homepage(self.page, args)

        else:
            self.navigator.navigate_homepage(self.page, args, parameters)

    def navigate_back(self, args: Arguments=(), **parameters: RouteParameters) -> None:
        """Navigate back to the previous route. If the navigator is virtual, parameters are not used."""
        if self.navigator.is_virtual():
            self.navigator.navigate_back(self.page, args)

        else:
            self.navigator.navigate_back(self.page, args, parameters)

    def set_homepage(self, homepage: str) -> None:
        """Update navigator's homepage address."""
        self.navigator.set_homepage(homepage)

    def spec_cpage_props(self, **props: dict[str, Any]) -> None:
        """Specify current page properties."""
        self.navigator.props_map[self.route_id] = props

        AbstractFletNavigator.proc_page_props(self.page, props, ())

        self.page.update()

    def current_route(self) -> str:
        """Get the navigator's current route state."""
        return self.navigator.route

    def __repr__(self) -> str:
        """Represent the RouteContext instance as a string for debugging purposes."""
        return f'{self.previous_page} -> {self.navigator.route} [{"NO-ARGUMENTS" if not self.arguments else self.arguments}, {"NO-PARAMETERS" if len(self.parameters) <= 0 else self.parameters}] ({self.route_id}) (NAVIGATOR-OBJECT {self.navigator})'


class AbstractFletNavigator:
    @staticmethod
    def init_nav(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], page: Page=None, routes: Routes={}, route_change_callback: RouteChangeCallback=None) -> None:
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
            page.on_route_change = nav.fn_route_change_handler_

        routes_to_delete = []

        for route in _pre_def_routes:
            nav.routes[route] = _pre_def_routes[route]

        for route in nav.routes:
            if route != '/' and route != ROUTE_404:
                if not nav._afn_vroute.match(route):
                    routes_to_delete.append(route)

                    nav._logger.error(f'Invalid route name: "{route}". Route names must start with a letter or underscore and contain only alphanumeric characters or underscores.')

        for route_to_delete in routes_to_delete:
            nav.routes.pop(route_to_delete)

        nav._returning = False

    @staticmethod
    def navigate(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], route: str, page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None:
        if nav.is_virtual() and '?' in route:
            route = route.split('?')[0]

            nav._logger.error('VirtualFletNavigator does not support URL parameters. Use page arguments instead, or switch to PublicFletNavigator for full URL parameters support.')

        if not nav._returning:
            nav.previous_routes.append(nav.route)

        nav.route = route

        if not nav.is_virtual():
            nav._nav_temp_args = args

            if route == '/' and parameters:
                page.go(route)

                nav._logger.error('Index/Main route does not support parameters; parameters transferring skipped.')

            else:
                page.go(AbstractFletNavigator.fparams(route, **parameters))

        else:
            nav.process(page, args)

    @staticmethod
    def navigate_homepage(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None:
        AbstractFletNavigator.navigate(nav, nav.homepage, page, args, parameters)

    @staticmethod
    def set_homepage(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], homepage: str) -> None:
        if homepage not in nav.routes:
            nav._logger.error('Can\'t update homepage address: invalid route.')

            return

        nav.homepage = homepage

    @staticmethod
    def navigate_back(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None:
        if len(nav.previous_routes) > 0:
            nav._returning = True

            AbstractFletNavigator.navigate(nav, nav.previous_routes[-1], page, args, parameters)

            nav._returning = False

            nav.previous_routes.pop()

    @staticmethod
    def process(nav: Union['VirtualFletNavigator', 'PublicFletNavigator'], page: Page, args: Arguments=(), route_parameters: RouteParameters={}) -> None:
        total_props = AbstractFletNavigator.find_all_specified_props(nav.routes, nav.props_map)

        if nav.route not in nav.routes:
            page.clean()

            r404_rctx_inst = RouteContext(page, nav, args, route_parameters, ROUTE_404)

            if ROUTE_404 in nav.routes:
                AbstractFletNavigator.proc_page_props(page, nav.props_map.get(ROUTE_404), total_props)

                nav.routes[ROUTE_404](r404_rctx_inst)

            else:
                _DEFAULT_PAGE_404(r404_rctx_inst)

            if nav.route_change_callback:
                nav.route_change_callback(r404_rctx_inst)

            nav._logger.error(f'Route "{nav.route}" does not exist in the defined routes. Unable to process the page.')

        else:
            page.clean()

            route_id = hash(nav.route)

            AbstractFletNavigator.proc_page_props(page, nav.props_map.get(route_id), total_props)

            nav.routes[nav.route](nxrctx := RouteContext(page, nav, args, route_parameters, route_id))

            page.update()

            if nav.route_change_callback:
                nav.route_change_callback(nxrctx)

    @staticmethod
    def find_all_specified_props(routes: Routes, props_map: RouteProperties) -> tuple[str]:
        total_props_specified = []

        for route in routes:
            route_id = hash(route)

            if route_id in props_map:
                total_props_specified += list(props_map[route_id].keys())

        return tuple(total_props_specified)

    @staticmethod
    def proc_page_props(page: Page, props: RouteProperties, total_props: tuple[str]) -> None:
        for prop in total_props:
            setattr(page, prop, None)

        if props:
            for prop, prop_value in props.items():
                setattr(page, prop, prop_value)

    @staticmethod
    def fparams(route: str, **_parameters: dict) -> str:
        return f'{route}?{"&".join(f"{key}={value}" for key, value in _parameters.items())}' if len(_parameters) > 0 else route

    @staticmethod
    def is_virtual(nav: Union['VirtualFletNavigator', 'PublicFletNavigator']) -> bool:
        return getattr(nav, 'virtual', None)


class PublicFletNavigator:
    """The Public Flet Navigator. It's just like the virtual one, but with URL parameters and visible routes."""

    page: Page = None
    """Page object representing the current page."""

    route: str = '/'
    """The current active route."""

    routes: Routes = {}
    """A map of all registered routes in the application."""

    previous_routes: list[str] = []
    """A list of all previously visited routes."""

    homepage: str = '/'
    """The homepage route."""

    props_map: RouteProperties = {}
    """A page properties map for each page ID."""

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
        AbstractFletNavigator.navigate_homepage(self, page, args, parameters)

    def set_homepage(self, homepage: str) -> None:
        """Update navigator's homepage address."""
        AbstractFletNavigator.set_homepage(self, homepage)

    def navigate_back(self, page: Page, args: Arguments=(), parameters: RouteParameters={}) -> None:
        """Navigate back to the previous route."""
        AbstractFletNavigator.navigate_back(self, page, args, parameters)

    def process(self, page: Page, args: Arguments=(), route_parameters: RouteParameters={}) -> None:
        """Process the current route on the provided page."""
        AbstractFletNavigator.process(self, page, args, route_parameters)

    def is_virtual(self) -> bool:
        """Check if the navigator is virtual or public."""
        return AbstractFletNavigator.is_virtual(self)

    def fn_route_change_handler_(self, _) -> None:
        route: str = self.page.route.replace(' ', _url_fn_space_chr).replace('%20', _url_fn_space_chr).replace('+', _url_fn_space_chr)

        route = route[1:] if route.startswith('/') and len(route) >= 2 else route

        split_url = urlsplit(route)

        base_route, qstr = split_url.path, split_url.query

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

        self.route = base_route

        if not globals().get('_FNDP404_CLOSED'):
            setattr(self.page, 'horizontal_alignment', globals().get('_FNDP404_PRE_H_A')),
            setattr(self.page, 'vertical_alignment', globals().get('_FNDP404_PRE_V_A')),

        self.process(self.page, self._nav_temp_args, parameters)

        self._nav_temp_args = None


class VirtualFletNavigator:
    """The Virtual Flet Navigator. It's just like the public one, but without URL parameters and visible routes."""

    route: str = '/'
    """The current active route."""

    routes: Routes = {}
    """A map of all registered routes in the application."""

    previous_routes: list[str] = []
    """A list of all previously visited routes."""

    homepage: str = '/'
    """The homepage route."""

    props_map: RouteProperties = {}
    """A page properties map for each page ID."""

    route_change_callback: RouteChangeCallback = None
    """A callback function that is triggered when the route changes."""

    def __init__(self, routes: Routes={}, route_change_callback: RouteChangeCallback=None) -> None:
        """Initialize the virtual navigator."""
        AbstractFletNavigator.init_nav(self, None, routes, route_change_callback)

    def navigate(self, route: str, page: Page, args: Arguments=()) -> None:
        """Navigate to a specific route in the application."""
        AbstractFletNavigator.navigate(self, route, page, args)

    def navigate_homepage(self, page: Page, args: Arguments=()) -> None:
        """Navigate to the homepage route."""
        AbstractFletNavigator.navigate_homepage(self, page, args)

    def set_homepage(self, homepage: str) -> None:
        """Update navigator's homepage address."""
        AbstractFletNavigator.set_homepage(self, homepage)

    def navigate_back(self, page: Page, args: Arguments=()) -> None:
        """Navigate back to the previous route."""
        AbstractFletNavigator.navigate_back(self, page, args)

    def process(self, page: Page, args: Arguments=()) -> None:
        """Process the current route on the provided page."""
        AbstractFletNavigator.process(self, page, args)

    def is_virtual(self) -> bool:
        """Check if the navigator is virtual or public."""
        return AbstractFletNavigator.is_virtual(self)


def route(route: Union[str, PageDefinition]) -> Any:
    """Link a route to the last initialized navigator.

    This function registers the route and associates it with a given page definition.
    The only difference is the name. You can specify the name in the first argument.
    or this function will fetch the given function name automatically."""
    if isinstance(route, Callable):
        _pre_def_routes[route.__name__] = route

    else:
        def _route_decorator(page_definition: PageDefinition) -> None:
            _pre_def_routes[route] = page_definition

        return _route_decorator


def load_page(path: str, name: Optional[str]=None) -> PageDefinition:
    """Load a page definition from a specified module.

    Let me explain this technically: it replaces all the system path separators with a dot.
    After loading the module by its path, it loads the page definition function.
    The function name is determined by the path. If a name is specified, then it loads the specified name.
    Otherwise, it uses the last name in the path.
    
    Can throw `ModuleNotFoundError` and `AttributeError`."""
    path = path.replace('\\', '.').replace('/', '.')

    page = None

    try:
        page = getattr(import_module(path), _pd := path.split('.')[-1] if not name else name)
    except ModuleNotFoundError as module_exc:
        raise TypeError(f'Failed to load page definition module: "{path}".') from module_exc
    except AttributeError as attr_error:
        raise ImportError(f'Failed to load page definition: "{_pd}".') from attr_error

    return page


def template(template_definition: Union[str, TemplateDefinition], route_data: RouteContext, arguments: Arguments=()) -> Optional[Any]:
    """Render a template for the given page data and arguments.
    
    If `template_definition` is a string, then it's a global template.
    The function will try to find the template you defined earlier via `@global_template` in the list of global templates.
    If `template_definition` is a callable, then it's a local template.
    The template will be rendered by calling the template function."""
    if isinstance(template_definition, str):
        if template_definition in _global_templates:
            return _global_templates[template_definition](route_data, arguments)

        else:
            route_data.navigator._logger.error(f'No global template found with the name: "{template_definition}". Ensure the template is registered and its name is correct.')

    else:
        return template_definition(route_data, arguments)


def global_template(template_name: Optional[str]=None) -> Any:
    """Register a global template to the last initialized navigator.

    This function registers the template and associates it with a given template definition.
    The only difference is the name. You can specify the name in the first argument.
    or this function will fetch the given template function name automatically."""
    if isinstance(template_name, Callable):
        _global_templates[template_name.__name__] = template_name

    else:
        def _global_template(template: TemplateDefinition) -> None:
            _global_templates[template.__name__ if not template_name or not isinstance(template_name, str) else template_name] = template

        return _global_template


def fn_process(start: str='/', virtual: bool=False, routes: Routes={}, route_change_callback: RouteChangeCallback=None, startup_args: Arguments=(), public_startup_parameters: RouteParameters={}) -> Callable[[Page], None]:
    """Shortcut to skip main function implementation and just calling `fn_process` in Flet's `app` function.
    
    The best way to explain this function is to show an example:
    ```
    @route('/')
    def main(rd: RouteContext) -> None:
        ...

    app(fn_process()) # Instead of: app(lambda page: PublicFletNavigator(page).process(page))
    ```"""
    return lambda page: (
        fn := PublicFletNavigator(page, routes, route_change_callback),

        setattr(fn, 'route', start),

        fn.process(page, startup_args, public_startup_parameters)) \
     if not virtual else (
        fn := VirtualFletNavigator(routes, route_change_callback),

        setattr(fn, 'route', start),

        fn.process(page, startup_args)
    )

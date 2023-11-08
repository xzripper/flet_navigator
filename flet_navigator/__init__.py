"""Navigator for Flet."""

from flet import Page

from typing import Callable, Any

from warnings import warn_explicit

from re import compile as re_compile

from importlib import import_module

from typing import Union


FLET_NAVIGATOR_VERSION: float = '2.1.3'
"""Flet Navigator Version."""

ROUTE_404: str = 'ROUTE-404'
"""Route 404 Typehint."""

URL_FN_SPACE_CHARACTER: str = '_$urlspace_'
"""FletNavigator URL Space Character."""

class PageData:
    """PageData Class."""

    page: Page = None
    """Current page."""

    navigator: Union['FletNavigator', 'VirtualFletNavigator'] = None
    """Navigator."""

    arguments: tuple[Any] = None
    """Arguments sent from previous page."""

    previous_page: str = None
    """Previous page."""

    parameters: dict[str, Any] = None
    """URL parameters."""

    def __init__(self, page: Page, navigator: Union['FletNavigator', 'VirtualFletNavigator'], arguments: tuple[any], previous_page: str, parameters: dict[str, Any]) -> None:
        """Initialize PageData."""
        self.page = page

        self.navigator = navigator

        self.arguments = arguments

        self.previous_page = previous_page

        self.parameters = parameters

class VirtualFletNavigator:
    """Flet Virtual Navigator Class."""

    route: str = '/'
    """Current route."""

    routes: dict[str, Callable[[PageData], None]] = {}
    """All supported routes."""

    routes_data: dict[str, Any] = {}
    """Routes data (cookies-like, but global)."""

    route_changed_handler: Callable[[str], None] = None
    """On route changed handler."""

    _nav_previous_routes: list[str] = ['/']

    _nav_route_simple_re: str = r'^[a-zA-Z_]\w*$'

    def __init__(self, routes: dict[str, Callable[[PageData], None]], route_changed_handler: Callable[[str], None]=None) -> None:
        """Initialize Virtual Flet Navigator."""
        self.routes = routes

        self.route_changed_handler = route_changed_handler

        routes_to_delete = []

        for route in self.routes:
            if route != '/' and route != ROUTE_404:
                if not re_compile(self._nav_route_simple_re).match(route):
                    warn_explicit(f'Wrong route name: "{route}". Allowed only digits and underscores.', Warning, 'flet_navigator::constructor', 51)

                    routes_to_delete.append(route)

        for route_to_delete in routes_to_delete:
            self.routes.pop(route_to_delete)

        for route in self.routes:
            self.routes_data[route] = None

    def navigate(self, route: str, page: Page, args: tuple[Any]=None) -> None:
        """Navigate to specific route."""
        self._nav_previous_routes.append(self.route)

        self.route = route

        self.render(page, args)

    def render(self, page: Page, args: tuple[Any]=None) -> None:
        """Render current route. If there is no route like that throw ROUTE-404 (if specified)."""
        if self.route not in self.routes:
            if ROUTE_404 in self.routes:
                page.clean()

                self.routes[ROUTE_404](PageData(page, self, args, self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None, {}))

                if self.route_changed_handler:
                    self.route_changed_handler(self.route)

        else:
            for route in self.routes:
                if self.route == route:
                    page.clean()

                    self.routes[route](PageData(page, self, args, self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else '/', {}))

                    page.update()

                    if self.route_changed_handler:
                        self.route_changed_handler(route)

    def set_route_data(self, route: str, data: Any) -> int:
        """Set route data (cookies-like, but global)."""
        if route in self.routes_data:
            self.routes_data[route] = data

            return 0

        else:
            return 1

    def get_route_data(self, route: str) -> Any:
        """Get route data (cookies-like, but global)."""
        if route in self.routes_data:
            return self.routes_data[route]

        else:
            return None

class FletNavigator:
    """Flet Navigator Class."""

    page: Page = None
    """Page."""

    route: str = '/'
    """Current route."""

    routes: dict[str, Callable[[PageData], None]] = {}
    """All supported routes."""

    routes_data: dict[str, Any] = {}
    """Routes data (cookies-like, but global)."""

    route_changed_handler: Callable[[str], None] = None
    """On route changed handler."""

    _nav_previous_routes: list[str] = ['/']

    _nav_temp_args: tuple[Any] = None

    _nav_route_simple_re: str = r'^[a-zA-Z_]\w*$'
    _nav_route_advanced_re: str = r'^[a-zA-Z_]\w*\?\w+=(?:[\w+~`!@"#№$;%^:*-,.|\/\\<>\'{}[\]()-]+)(?:&\w+=(?:[\w+~`!@"#№$;%^:*-,.|\/\\<>\'{}[\]()-]+))*$'

    _nav_is_float_re: str = r'^-?\d+\.\d+$'

    def __init__(self, page: Page, routes: dict[str, Callable[[PageData], None]], route_changed_handler: Callable[[str], None]=None) -> None:
        """Initialize Virtual Flet Navigator."""
        self.page = page

        self.routes = routes

        self.route_changed_handler = route_changed_handler

        routes_to_delete = []

        for route in self.routes:
            if route != '/' and route != ROUTE_404:
                if not re_compile(self._nav_route_simple_re).match(route):
                    warn_explicit(f'Wrong route name: "{route}". Allowed only digits and underscores.', Warning, 'flet_navigator::constructor', 51)

                    routes_to_delete.append(route)

        for route_to_delete in routes_to_delete:
            self.routes.pop(route_to_delete)

        for route in self.routes:
            self.routes_data[route] = None

        self.page.on_route_change = self._nav_route_change_handler

    def navigate(self, route: str, page: Page, args: tuple[Any]=None) -> None:
        """Navigate to specific route."""
        self._nav_previous_routes.append(self.route)

        self._nav_temp_args = args

        self.route = route.replace(' ', URL_FN_SPACE_CHARACTER)

        page.go(self.route)

    def render(self, page: Page, args: tuple[Any]=None, route_parameters: dict[str, Any]={}) -> None:
        """Render current route. If there is no route like that throw ROUTE-404 (if specified)."""
        if self.route not in self.routes:
            if ROUTE_404 in self.routes:
                page.clean()

                self.routes[ROUTE_404](PageData(page, self, args, self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None, route_parameters))

                if self.route_changed_handler:
                    self.route_changed_handler(self.route)

        else:
            for route in self.routes:
                if self.route == route:
                    page.clean()

                    self.routes[route](PageData(page, self, args, self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else '/', route_parameters))

                    page.update()

                    if self.route_changed_handler:
                        self.route_changed_handler(route)

    def set_route_data(self, route: str, data: Any) -> int:
        """Set route data (cookies-like, but global)."""
        if route in self.routes_data:
            self.routes_data[route] = data

            return 0

        else:
            return 1

    def get_route_data(self, route: str) -> Any:
        """Get route data (cookies-like, but global)."""
        if route in self.routes_data:
            return self.routes_data[route]

        else:
            return None

    def _nav_route_change_handler(self, _) -> None:
        route: str = self.page.route.replace(' ', URL_FN_SPACE_CHARACTER).replace('%20', URL_FN_SPACE_CHARACTER).replace('+', URL_FN_SPACE_CHARACTER)

        if route.startswith('/') and len(route) >= 2: route = route[1:]

        parameters = {}

        if re_compile(self._nav_route_advanced_re).match(route):
            _parameters_list = route.split('?')[1]

            if '&' in _parameters_list: _parameters_list = _parameters_list.split('&')
            else: _parameters_list = [_parameters_list]

            for _parameter in _parameters_list:
                _parameter_parsed = _parameter.split('=')

                if _parameter_parsed[0].startswith('?'): _parameter_parsed[0] = _parameter_parsed[0][1:]

                if len(_parameter_parsed) <= 1:
                    warn_explicit(f'Unable to parse route parameters ({_parameters_list.index(_parameter)}).', Warning, 'flet_navigator::RouteChangeHandler', 261)

                    continue

                if _parameter_parsed[0].isdigit():
                    warn_explicit(f'Unable to parse route parameters ({_parameters_list.index(_parameter)}): key should be string.', Warning, 'flet_navigator::RouteChangeHandler', 266)

                    continue

                if _parameter_parsed[1].isdigit(): parameters[_parameter_parsed[0]] = int(_parameter_parsed[1])
                elif re_compile(self._nav_is_float_re).match(_parameter_parsed[1]): parameters[_parameter_parsed[0]] = float(_parameter_parsed[1])
                elif _parameter_parsed[1] in ['true', 'false']: parameters[_parameter_parsed[0]] = bool(_parameter_parsed[1])
                else: parameters[_parameter_parsed[0]] = _parameter_parsed[1].replace(URL_FN_SPACE_CHARACTER, ' ')

                self.route = route.split('?')[0]

        else:
            self.route = route.split('?')[0] # In case user did a syntax error. 

        self.render(self.page, self._nav_temp_args, parameters)

        self._nav_temp_args = None

def define_page(path: str, name: str=None) -> Callable[[PageData], None]:
    """Get page from module."""
    path = path.replace('\\', '.').replace('/', '.')

    page = None

    try:
        page = getattr(import_module(path), path.split('.')[-1] if not name else name)
    except AttributeError:
        warn_explicit(f'Unable to define page: "{path}".', Warning, 'flet_navigator::define_page', 291)

    return page

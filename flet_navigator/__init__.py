"""Navigator for Flet."""

from flet import Page, Control

from typing import Callable, Any

from warnings import warn_explicit

from re import compile as re_compile


FLET_NAVIGATOR_VERSION: float = '2.0.1'
"""Flet Navigator Version."""

ROUTE_404: str = 'ROUTE-404'
"""Route 404 Typehint."""

def get_page_widgets(page: Page) -> list[Control]:
    """Get page widgets."""
    return page._get_children()[0]._get_children()

class VirtualFletNavigator:
    """Flet Virtual Navigator Class."""

    route: str = '/'
    """Current route."""

    routes: dict[str, Callable[[Page, 'VirtualFletNavigator', tuple[Any], str], None]] = {}
    """All supported routes."""

    routes_data: dict[str, Any] = {}
    """Routes data (cookies-like, but global)."""

    route_changed_handler: Callable[[str], None] = None
    """On route changed handler."""

    _nav_previous_routes: list[str] = ['/']

    _nav_route_simple_re: str = r'^[a-zA-Z_]\w*$'

    def __init__(self, routes: dict[str, Callable[[Page, 'VirtualFletNavigator', tuple[Any], str], None]], route_changed_handler: Callable[[str], None]=None) -> None:
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

    def navigate(self, route: str, page: Page, args: tuple[Any]=None, route_parameters: dict[str, Any]={}) -> None:
        """Navigate to specific route."""
        self._nav_previous_routes.append(self.route)

        self.route = route

        self.render(page, args, route_parameters)

    def render(self, page: Page, args: tuple[Any]=None, route_parameters: dict[str, Any]={}) -> None:
        """Render current route. If there is no route like that throw ROUTE-404 (if specified)."""
        if self.route not in self.routes:
            if ROUTE_404 in self.routes:
                page.clean()

                self.routes[ROUTE_404](page, self, args, self._nav_previous_routes[-2] if len(self._nav_previous_routes) >= 2 else None, route_parameters)

        else:
            for route in self.routes:
                if self.route == route:
                    page.clean()

                    self.routes[route](page, self, args, self._nav_previous_routes[-2] if len(self._nav_previous_routes) >= 2 else '/', route_parameters)

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

    routes: dict[str, Callable[[Page, 'FletNavigator', tuple[Any], str], None]] = {}
    """All supported routes."""

    routes_data: dict[str, Any] = {}
    """Routes data (cookies-like, but global)."""

    route_changed_handler: Callable[[str], None] = None
    """On route changed handler."""

    _nav_previous_routes: list[str] = ['/']

    _nav_route_simple_re: str = r'^[a-zA-Z_]\w*$'
    _nav_route_advanced_re: str = r'^[a-zA-Z_]\w*\?\w+=\w+(?:&\w+=\w+)*$'

    _nav_is_float_re: str = r'^-?\d+\.\d+$'

    def __init__(self, page: Page, routes: dict[str, Callable[[Page, 'FletNavigator', tuple[Any], str], None]], route_changed_handler: Callable[[str], None]=None) -> None:
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

    def navigate(self, route: str, page: Page, args: tuple[Any]=None, route_parameters: dict[str, Any]={}) -> None:
        """Navigate to specific route."""
        self._nav_previous_routes.append(self.route)

        self.route = route

        page.go(self.route) # [Here happens double redirect].

        self.render(page, args, route_parameters)

    def render(self, page: Page, args: tuple[Any]=None, route_parameters: dict[str, Any]={}) -> None:
        """Render current route. If there is no route like that throw ROUTE-404 (if specified)."""
        if self.route not in self.routes:
            if ROUTE_404 in self.routes:
                page.clean()

                self.routes[ROUTE_404](page, self, args, self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None, route_parameters)

        else:
            for route in self.routes:
                if self.route == route:
                    page.clean()

                    self.routes[route](page, self, args, self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else '/', route_parameters)

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
        route: str = self.page.route

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
                    warn_explicit(f'Unable to parse route parameters ({_parameters_list.index(_parameter)}).', Warning, 'flet_navigator::merge_routes', 92)

                    continue

                if _parameter_parsed[0].isdigit():
                    warn_explicit(f'Unable to parse route parameters ({_parameters_list.index(_parameter)}): key should be string.', Warning, 'flet_navigator::merge_routes', 99)

                    continue

                if _parameter_parsed[1].isdigit(): parameters[_parameter_parsed[0]] = int(_parameter_parsed[1])
                elif re_compile(self._nav_is_float_re).match(_parameter_parsed[1]): parameters[_parameter_parsed[0]] = float(_parameter_parsed[1])
                elif _parameter_parsed[1] in ['true', 'false']: parameters[_parameter_parsed[0]] = bool(_parameter_parsed[1])
                else: parameters[_parameter_parsed[0]] = _parameter_parsed[1]

                self.route = route.split('?')[0]

        else:
            self.route = route

        self.render(self.page, None, parameters)

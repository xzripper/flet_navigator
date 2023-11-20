"""Navigator for Flet."""

from flet import Page, Control

from time import sleep

from warnings import warn_explicit

from re import compile as re_compile

from importlib import import_module

from typing import Union, Callable, Any


_pre_def_routes: 'Routes' = {}

FLET_NAVIGATOR_VERSION: str = '2.4.5'
"""Flet Navigator Version."""

ROUTE_404: str = 'ROUTE-404'
"""Route 404 Typehint."""

URL_FN_SPACE_CHARACTER: str = '_$urlspace_'
"""FletNavigator URL Space Character."""


def get_page_widgets(page: Page) -> list[Control]:
    """Get page widgets."""
    return page._get_children()[0]._get_children()


class NavigatorAnimation:
    NONE: int = 0
    """None animation."""

    FADE: int = 1
    """Fade out animation."""

    SCALE: int = 2
    """Scale out animation."""

    ROTATE: int = 3
    """Rotate out animation."""

    SMOOTHNESS_1: list[float] = [0.9, 0.0]
    """Smoothness level 1."""

    SMOOTHNESS_2: list[float] = [0.9, 0.8, 0.0]
    """Smoothness level 2."""

    SMOOTHNESS_3: list[float] = [0.9, 0.8, 0.7, 0.0]
    """Smoothness level 3."""

    SMOOTHNESS_4: list[float] = [0.9, 0.8, 0.7, 0.6, 0.0]
    """Smoothness level 4."""

    SMOOTHNESS_5: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.0]
    """Smoothness level 5."""

    SMOOTHNESS_6: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.0]
    """Smoothness level 6."""

    SMOOTHNESS_7: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.0]
    """Smoothness level 7."""

    SMOOTHNESS_8: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.0]
    """Smoothness level 8."""

    SMOOTHNESS_9: list[float] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    """Smoothness level 9."""

    SMOOTHNESS_10: list[float] = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    """Smoothness level 10."""

    animation: int = FADE
    """Selected animation."""

    smoothness: list[float] = SMOOTHNESS_9
    """Animation smoothness."""

    delay: float = 0.01
    """Animation delay."""

    optimized_delay: float = 0.001
    """Animation optimized delay (when too much controls on the page)."""

    optimization_threshold: int = 5
    """Optimization threshold (maximal amount of controls that force optimized delay using instead of simple delay)."""

    def __init__(self, animation: int=FADE, smoothness: list[float]=SMOOTHNESS_9, delay: float=0.01, optimized_delay: float=0.001, optimization_threshold: int=5) -> None:
        """Initialize navigator animation."""
        self.animation = animation
        self.smoothness = smoothness

        self.delay = delay
        self.optimized_delay = optimized_delay

        self.optimization_threshold = optimization_threshold

    def animate_out(self, page: Page, page_widgets: list[Control]) -> None:
        """Play out animation."""
        delay = self.delay

        if len(page_widgets) > self.optimization_threshold:
            delay = self.optimized_delay

        if self.animation == self.FADE:
            for control in page_widgets:
                for opacity in self.smoothness:
                    control.opacity = opacity

                    page.update()

                    sleep(delay)

            page.clean()

        elif self.animation == self.SCALE:
            for control in page_widgets:
                for scale in self.smoothness:
                    control.scale = scale

                    page.update()

                    sleep(delay)

            page.clean()

        elif self.animation == self.ROTATE:
            for control in page_widgets:
                rotation_smoothness = (len(self.SMOOTHNESS_10) - len(self.smoothness)) + 1

                rotation_smoothness = rotation_smoothness // 2 if rotation_smoothness >= 2 else rotation_smoothness

                for angle, scale in zip(range(0, 90, rotation_smoothness), self.smoothness):
                    if scale <= 0.0:
                        break

                    control.rotate = angle

                    control.scale = scale - 0.1

                    page.update()

                    sleep(delay)

            page.clean()

        else:
            page.clean()


Arguments = tuple[Any]
"""Arguments type."""


class PageData:
    """PageData Class."""

    page: Page = None
    """Current page."""

    navigator: Union['FletNavigator', 'VirtualFletNavigator'] = None
    """Navigator."""

    arguments: Arguments = None
    """Arguments sent from previous page."""

    previous_page: str = None
    """Previous page."""

    parameters: dict[str, Any] = None
    """URL parameters."""

    page_id: int = None
    """Page ID."""

    def __init__(self, page: Page, navigator: Union['FletNavigator', 'VirtualFletNavigator'], arguments: Arguments, previous_page: str, parameters: dict[str, Any], page_id: int) -> None:
        """Initialize PageData."""
        self.page = page

        self.navigator = navigator

        self.arguments = arguments

        self.previous_page = previous_page

        self.parameters = parameters

        self.page_id = page_id

    def set_appbar(self, appbar: Control) -> None:
        """Set appbar for this page (ID)."""
        self.page.appbar = appbar

        self.navigator.appbars[self.page_id] = appbar


PageDefinition = Callable[[PageData], None]
"""Page Definition Type."""

TemplateDefinition = Callable[[PageData, Arguments], Union[Control, None]]
"""Template Definition Type(hint)."""

RouteChangedHandler = Callable[[str], None]
"""Route Changed Handler Type."""

Routes = dict[str, PageDefinition]
"""Routes Type."""


class VirtualFletNavigator:
    """Flet Virtual Navigator Class."""

    route: str = '/'
    """Current route."""

    routes: Routes = {}
    """All supported routes."""

    routes_data: dict[str, Any] = {}
    """Routes data (cookies-like, but global)."""

    homepage: str = '/'
    """Homepage route."""

    navigator_animation: NavigatorAnimation = NavigatorAnimation()
    """Page switch animation."""

    appbars: dict[int, Control] = {}
    """Dictionary of appbars for each page ID."""

    route_changed_handler: RouteChangedHandler = None
    """On route changed handler."""

    _nav_previous_routes: list[str] = ['/']

    _nav_route_simple_re: str = r'^[a-zA-Z_]\w*$'

    def __init__(self, routes: Routes, route_changed_handler: RouteChangedHandler=None, navigator_animation: NavigatorAnimation=NavigatorAnimation()) -> None:
        """Initialize Virtual Flet Navigator."""
        self.routes = routes

        self.route_changed_handler = route_changed_handler

        routes_to_delete = []

        for route in self.routes:
            if route != '/' and route != ROUTE_404:
                if not re_compile(self._nav_route_simple_re).match(route):
                    warn_explicit(
                        f'Wrong route name: "{route}". Allowed only digits and underscores.', Warning,
                        'flet_navigator::constructor', 51
                    )

                    routes_to_delete.append(route)

        for route_to_delete in routes_to_delete:
            self.routes.pop(route_to_delete)

        for route in self.routes:
            self.routes_data[route] = None

        self.navigator_animation = navigator_animation

        for route in _pre_def_routes:
            self.routes[route] = _pre_def_routes[route]

    def navigate(self, route: str, page: Page, args: Arguments=None) -> None:
        """Navigate to specific route."""
        if '?' in route:
            warn_explicit(
                'VirtualFletNavigator doesn\'t have URL parameters support. Consider using page arguments or FletNavigator.', Warning,
                'flet_navigator::navigate', 98
            )

            route = route.split('?')[0]

        self._nav_previous_routes.append(self.route)

        self.route = route

        self.render(page, args)

    def navigate_homepage(self, page: Page, args: Arguments=None) -> None:
        """Navigate homepage."""
        self.navigate(self.homepage, page, args)

    def render(self, page: Page, args: Arguments=None) -> None:
        """Render current route. If there is no route like that throw ROUTE-404 (if specified)."""
        if self.route not in self.routes:
            if ROUTE_404 in self.routes:
                page.clean()

                if 404 in self.appbars:
                    page.appbar = self.appbars[404]

                else:
                    page.appbar = None

                self.routes[ROUTE_404](
                    PageData(
                        page, self, args,

                        self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None,

                        {}, 404
                    )
                )

                if self.route_changed_handler:
                    self.route_changed_handler(self.route)

        else:
            for route in self.routes:
                if self.route == route:
                    self.navigator_animation.animate_out(page, get_page_widgets(page))

                    page_id = list(self.routes.keys()).index(route) + 1

                    if page_id in self.appbars:
                        page.appbar = self.appbars[page_id]

                    else:
                        page.appbar = None

                    self.routes[route](
                        PageData(
                            page, self, args,

                            self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else '/',

                            {}, page_id
                        )
                    )

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

    def set_homepage(self, homepage: str) -> None:
        """Set homepage."""
        self.homepage = homepage

class FletNavigator:
    """Flet Navigator Class."""

    page: Page = None
    """Page."""

    route: str = '/'
    """Current route."""

    routes: Routes = {}
    """All supported routes."""

    routes_data: dict[str, Any] = {}
    """Routes data (cookies-like, but global)."""

    homepage: str = '/'
    """Homepage route."""

    navigator_animation: NavigatorAnimation = NavigatorAnimation()
    """Page switch animation."""

    appbars: dict[int, Control] = {}
    """Dictionary of appbars for each page ID."""

    route_changed_handler: RouteChangedHandler = None
    """On route changed handler."""

    _nav_previous_routes: list[str] = ['/']

    _nav_temp_args: Arguments = None

    _nav_route_simple_re: str = r'^[a-zA-Z_]\w*$'
    _nav_route_advanced_re: str = r'^[a-zA-Z_]\w*\?\w+=(?:[\w+~`!@"#№$;%^:*-,.|\/\\<>\'{}[\]()-]+)(?:&\w+=(?:[\w+~`!@"#№$;%^:*-,.|\/\\<>\'{}[\]()-]+))*$'

    _nav_is_float_re: str = r'^-?\d+\.\d+$'

    def __init__(self, page: Page, routes: Routes, route_changed_handler: RouteChangedHandler=None, navigator_animation: NavigatorAnimation=NavigatorAnimation()) -> None:
        """Initialize Virtual Flet Navigator."""
        self.page = page

        self.routes = routes

        self.route_changed_handler = route_changed_handler

        routes_to_delete = []

        for route in self.routes:
            if route != '/' and route != ROUTE_404:
                if not re_compile(self._nav_route_simple_re).match(route):
                    warn_explicit(
                        f'Wrong route name: "{route}". Allowed only digits and underscores.', Warning,
                        'flet_navigator::constructor', 51
                    )

                    routes_to_delete.append(route)

        for route_to_delete in routes_to_delete:
            self.routes.pop(route_to_delete)

        for route in self.routes:
            self.routes_data[route] = None

        self.page.on_route_change = self._nav_route_change_handler

        self.navigator_animation = navigator_animation

        for route in _pre_def_routes:
            self.routes[route] = _pre_def_routes[route]

    def navigate(self, route: str, page: Page, args: Arguments=None) -> None:
        """Navigate to specific route."""
        self._nav_previous_routes.append(self.route)

        self._nav_temp_args = args

        self.route = route

        page.go(self.route)

    def navigate_homepage(self, page: Page, args: Arguments=None) -> None:
        """Navigate homepage."""
        self.navigate(self.homepage, page, args)

    def render(self, page: Page, args: Arguments=None, route_parameters: dict[str, Any]={}) -> None:
        """Render current route. If there is no route like that throw ROUTE-404 (if specified)."""
        if self.route not in self.routes:
            if ROUTE_404 in self.routes:
                page.clean()

                if 404 in self.appbars:
                    page.appbar = self.appbars[404]

                else:
                    page.appbar = None

                self.routes[ROUTE_404](
                    PageData(
                        page, self, args,

                        self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None,

                        route_parameters, 404
                    )
                )

                if self.route_changed_handler:
                    self.route_changed_handler(self.route)

        else:
            for route in self.routes:
                if self.route == route:
                    self.navigator_animation.animate_out(page, get_page_widgets(page))

                    page_id = list(self.routes.keys()).index(route) + 1

                    if page_id in self.appbars:
                        page.appbar = self.appbars[page_id]

                    else:
                        page.appbar = None

                    self.routes[route](
                        PageData(
                            page, self, args,

                            self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else '/',

                            route_parameters, page_id)
                    )

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

    def set_homepage(self, homepage: str) -> None:
        """Set homepage."""
        self.homepage = homepage

    def _nav_route_change_handler(self, _) -> None:
        route: str = self.page.route \
            .replace(' ', URL_FN_SPACE_CHARACTER) \
            .replace('%20', URL_FN_SPACE_CHARACTER) \
            .replace('+', URL_FN_SPACE_CHARACTER)

        if route.startswith('/') and len(route) >= 2:
            route = route[1:]

        parameters = {}

        if re_compile(self._nav_route_advanced_re).match(route):
            _parameters_list = route.split('?')[1]

            if '&' in _parameters_list:
                _parameters_list = _parameters_list.split('&')

            else:
                _parameters_list = [_parameters_list]

            for _parameter in _parameters_list:
                _parameter_parsed = _parameter.split('=')

                if _parameter_parsed[0].startswith('?'):
                    _parameter_parsed[0] = _parameter_parsed[0][1:]

                if len(_parameter_parsed) <= 1:
                    warn_explicit(
                        f'Unable to parse route parameters ({_parameters_list.index(_parameter)}).', Warning,
                        'flet_navigator::RouteChangeHandler', 261
                    )

                    continue

                if _parameter_parsed[0].isdigit():
                    warn_explicit(
                        f'Unable to parse route parameters ({_parameters_list.index(_parameter)}): key should be string.', Warning,
                        'flet_navigator::RouteChangeHandler', 266
                    )

                    continue

                if _parameter_parsed[1].isdigit():
                    parameters[_parameter_parsed[0]] = int(_parameter_parsed[1])

                elif re_compile(self._nav_is_float_re).match(_parameter_parsed[1]):
                    parameters[_parameter_parsed[0]] = float(_parameter_parsed[1])

                elif _parameter_parsed[1] in ['true', 'false']:
                    parameters[_parameter_parsed[0]] = bool(_parameter_parsed[1])

                else:
                    parameters[_parameter_parsed[0]] = _parameter_parsed[1].replace(URL_FN_SPACE_CHARACTER, ' ')

                self.route = route.split('?')[0]

        else:
            self.route = route.split('?')[0]

        self.render(self.page, self._nav_temp_args, parameters)

        self._nav_temp_args = None


def route(route_name: str) -> Any:
    """Link route to last initialized navigator."""
    def _route_decorator(page_definition: PageDefinition):
        _pre_def_routes[route_name] = page_definition

    return _route_decorator


def define_page(path: str, name: str=None) -> PageDefinition:
    """Get page from module."""
    path = path.replace('\\', '.').replace('/', '.')

    page = None

    try:
        page = getattr(import_module(path), path.split('.')[-1] if not name else name)
    except AttributeError:
        warn_explicit(f'Unable to define page: "{path}".', Warning, 'flet_navigator::define_page', 291)

    return page


def template(template_definition: TemplateDefinition, page_data: PageData, arguments: Arguments=None) -> Union[Control, None]:
    """Render template."""
    return template_definition(page_data, arguments)

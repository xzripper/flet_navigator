"""Navigator for Flet."""

from flet import Page, Control, Scale, Text, TextButton

from warnings import warn_explicit

from re import compile as re_compile

from importlib import import_module

from random import randint

from time import sleep

from typing import Union, Callable, Any


_pre_def_routes: 'Routes' = {}


_global_templates: dict[str, 'TemplateDefinition'] = {}


FLET_NAVIGATOR_VERSION: str = '2.8.5'
"""Flet Navigator Version."""

ROUTE_404: str = 'ROUTE-404'
"""Route 404 Typehint."""

URL_FN_SPACE_CHARACTER: str = '_$urlspace_'
"""FletNavigator URL Space Character."""


def get_page_widgets(page: Page) -> list[Control]:
    """Get page widgets."""
    return page._get_children()[0]._get_children()


class NavigatorAnimation:
    """Class for implementing animations between page change."""

    NONE: int = 0
    """None animation."""

    FADE: int = 1
    """Fade out animation."""

    SCALE: int = 2
    """Scale out animation."""

    SHRINK: int = 3
    """Shrink (width) out animation."""

    SHRINK_VERTICAL: int = 4
    """Shrink (height) out animation."""

    ROTATE: int = 5
    """Rotate out animation."""

    CUSTOM: int = 6
    """Custom animation."""

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
    """Animation optimized delay (when a lot of controls on the page)."""

    optimization_threshold: int = 5
    """Optimization threshold (maximal amount of controls that force optimized delay using instead of simple delay)."""

    _custom_animation_out: Callable[[Control, float, float], None] = None

    def __init__(self, animation: int=FADE, smoothness: list[float]=SMOOTHNESS_8, delay: float=0.01, optimized_delay: float=0.001, optimization_threshold: int=5) -> None:
        """Initialize navigator animation."""
        self.animation = animation
        self.smoothness = smoothness

        self.delay = delay
        self.optimized_delay = optimized_delay

        self.optimization_threshold = optimization_threshold

    def set_custom_animation(self, animation: Callable[[Control, float, float], None]) -> None:
        """Set custom animation (if custom selected)."""
        if self.animation == self.CUSTOM:
            self._custom_animation = animation

    def animate_out(self, page: Page, page_widgets: list[Control]) -> None:
        """Play out animation."""
        delay = self.delay

        if len(page_widgets) > self.optimization_threshold:
            delay = self.optimized_delay

        if self.animation == self.FADE:
            for control in page_widgets:
                if control._get_control_name() != 'appbar':
                    for opacity in self.smoothness:
                        control.opacity = opacity

                        page.update()

                        sleep(delay)

            page.clean()

        elif self.animation == self.SCALE:
            for control in page_widgets:
                if control._get_control_name() != 'appbar':
                    for scale in self.smoothness:
                        control.scale = scale

                        page.update()

                        sleep(delay)

            page.clean()

        elif self.animation == self.SHRINK:
            for control in page_widgets:
                if control._get_control_name() != 'appbar':
                    for width in self.smoothness:
                        control.scale = Scale(scale_x=width, scale_y=1)

                        page.update()

                        sleep(delay)

            page.clean()

        elif self.animation == self.SHRINK_VERTICAL:
            for control in page_widgets:
                if control._get_control_name() != 'appbar':
                    for height in self.smoothness:
                        control.scale = Scale(scale_x=1, scale_y=height)

                        page.update()

                        sleep(delay)

            page.clean()

        elif self.animation == self.ROTATE:
            for control in page_widgets:
                if control._get_control_name() != 'appbar':
                    rotation_smoothness = (len(self.SMOOTHNESS_10) - len(self.smoothness)) + 1

                    rotation_smoothness = rotation_smoothness // 2 if rotation_smoothness >= 2 else rotation_smoothness

                    for angle, scale in zip(range(0, randint(80, 160), rotation_smoothness - 1), self.smoothness):
                        if scale <= 0.0:
                            break

                        control.rotate = angle

                        control.scale = scale - 0.1

                        page.update()

                        sleep(delay)

            page.clean()

        elif self.animation == self.CUSTOM:
            if self._custom_animation == None:
                    warn_explicit(
                        'Animation is set to custom but no animation found.', Warning,
                        'flet_navigator::navigator_animation::animate_out', 202)

                    page.clean()

            else:
                for control in page_widgets:
                    if control._get_control_name() != 'appbar':
                        for mult in self.smoothness:
                            self._custom_animation(control, mult, (len(self.SMOOTHNESS_10) - len(self.smoothness)))

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

    def add(self, *controls: Control) -> None:
        """Append control(s) to page."""
        self.page.add(*controls)

    def navigate(self, route: str, args: Arguments=None, parameters: dict[str, Any]=None) -> None:
        """Navigate to specific route. Parameters aren't used if navigator is virtual."""
        if self.navigator.virtual:
            self.navigator.navigate(route, self.page, args)

        else:
            self.navigator.navigate(route, self.page, args, parameters)

    def navigate_homepage(self, args: Arguments=None, parameters: dict[str, Any]=None) -> None:
        """Navigate to homepage. Parameters aren't used if navigator is virtual."""
        if self.navigator.virtual:
            self.navigator.navigate_homepage(self.page, args)

        else:
            self.navigator.navigate_homepage(self.page, args, parameters)

    def set_appbar(self, appbar: Control) -> None:
        """Set appbar for this page (ID)."""
        self.page.appbar = appbar

        self.navigator.appbars[self.page_id] = appbar

    def __repr__(self) -> str:
        """Represent PageData. Mostly used for debug."""
        return f'{self.previous_page} -> {self.navigator.route} [{"NO-ARGUMENTS" if not self.arguments else self.arguments}, {"NO-PARAMETERS" if len(self.parameters) <= 0 else self.parameters}] ({self.page_id}) (NAVIGATOR-OBJECT {self.navigator})'


PageDefinition = Callable[[PageData], None]
"""Page Definition Type."""

TemplateDefinition = Callable[[PageData, Arguments], Union[Control, None]]
"""Template Definition Type(hint)."""

RouteChangedHandler = Callable[[str], None]
"""Route Changed Handler Type."""

Routes = dict[str, PageDefinition]
"""Routes Type."""


_DEFAULT_PAGE_404: PageDefinition = lambda pg: (
    globals().__setitem__('_PRE_H_A', pg.page.horizontal_alignment),
    globals().__setitem__('_PRE_V_A', pg.page.vertical_alignment),

    setattr(pg.page, 'horizontal_alignment', 'center'),
    setattr(pg.page, 'vertical_alignment', 'center'),

    pg.add(Text('404', color='yellow', size=60)),

    pg.add(TextButton(
        f'Back to {pg.previous_page}.',

        on_click=lambda _: (
            pg.page.clean(),

            setattr(pg.page, 'horizontal_alignment', globals()['_PRE_H_A']),
            setattr(pg.page, 'vertical_alignment', globals()['_PRE_V_A']),

            pg.navigator.navigate(pg.previous_page, pg.page)
        )
    )),

    pg.add(Text('Set your 404 page via ROUTE_404 (FletNavigator).', color='grey', size=10))
)
"""Default Page 404."""


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

    def __init__(self, routes: Routes={}, route_changed_handler: RouteChangedHandler=None, navigator_animation: NavigatorAnimation=NavigatorAnimation()) -> None:
        """Initialize Virtual Flet Navigator."""
        self.routes = routes

        self.route_changed_handler = route_changed_handler

        routes_to_delete = []

        for route in self.routes:
            if route != '/' and route != ROUTE_404:
                if not re_compile(self._nav_route_simple_re).match(route):
                    warn_explicit(
                        f'Wrong route name: "{route}". Allowed only digits and underscores.', Warning,
                        'flet_navigator::constructor', 373)

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
                'flet_navigator::navigate', 393)

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

                if self.route_changed_handler:
                    self.route_changed_handler(self.route)

                self.routes[ROUTE_404](
                    PageData(
                        page, self, args,

                        self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None,

                        {}, 404))

            else:
                page.clean()

                if self.route_changed_handler:
                    self.route_changed_handler(self.route)

                _DEFAULT_PAGE_404(PageData(
                    page, self, args,

                    self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None,

                    {}, 404))

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

                            {}, page_id))

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

    @property
    def virtual(self) -> bool:
        """Is navigator virtual? (True)."""
        return True


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

    def __init__(self, page: Page, routes: Routes={}, route_changed_handler: RouteChangedHandler=None, navigator_animation: NavigatorAnimation=NavigatorAnimation()) -> None:
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
                        'flet_navigator::constructor', 548)

                    routes_to_delete.append(route)

        for route_to_delete in routes_to_delete:
            self.routes.pop(route_to_delete)

        for route in self.routes:
            self.routes_data[route] = None

        self.page.on_route_change = self._nav_route_change_handler

        self.navigator_animation = navigator_animation

        for route in _pre_def_routes:
            self.routes[route] = _pre_def_routes[route]

    def navigate(self, route: str, page: Page, args: Arguments=None, parameters: dict[str, Any]=None) -> None:
        """Navigate to specific route."""
        self._nav_previous_routes.append(self.route)

        self._nav_temp_args = args

        self.route = route

        page.go(parameters_(route, **parameters))

    def navigate_homepage(self, page: Page, args: Arguments=None, parameters: dict[str, Any]=None) -> None:
        """Navigate homepage."""
        self.navigate(self.homepage, page, args, parameters)

    def render(self, page: Page, args: Arguments=None, route_parameters: dict[str, Any]={}) -> None:
        """Render current route. If there is no route like that throw ROUTE-404 (if specified)."""
        if self.route not in self.routes:
            if ROUTE_404 in self.routes:
                page.clean()

                if 404 in self.appbars:
                    page.appbar = self.appbars[404]

                else:
                    page.appbar = None

                if self.route_changed_handler:
                    self.route_changed_handler(self.route)

                self.routes[ROUTE_404](
                    PageData(
                        page, self, args,

                        self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None,

                        route_parameters, 404))

            else:
                page.clean()

                if self.route_changed_handler:
                    self.route_changed_handler(self.route)

                _DEFAULT_PAGE_404(PageData(
                    page, self, args,

                    self._nav_previous_routes[-1] if len(self._nav_previous_routes) >= 1 else None,

                    {}, 404))

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

                            route_parameters, page_id))

                    print(get_page_widgets(page))

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
                        'flet_navigator::RouteChangeHandler', 694)

                    continue

                if not _parameter_parsed[0].isalpha():
                    warn_explicit(
                        f'Unable to parse route parameters ({_parameters_list.index(_parameter)}): key should be string.', Warning,
                        'flet_navigator::RouteChangeHandler', 701)

                    continue

                if _parameter_parsed[1].isdigit():
                    parameters[_parameter_parsed[0]] = int(_parameter_parsed[1])

                elif re_compile(self._nav_is_float_re).match(_parameter_parsed[1]):
                    parameters[_parameter_parsed[0]] = float(_parameter_parsed[1])

                elif _parameter_parsed[1].lower() in ['true', 'false']:
                    parameters[_parameter_parsed[0]] = _parameter_parsed[1].lower() == 'true'

                else:
                    parameters[_parameter_parsed[0]] = _parameter_parsed[1].replace(URL_FN_SPACE_CHARACTER, ' ')

                self.route = route.split('?')[0]

        else:
            self.route = route.split('?')[0]

        self.render(self.page, self._nav_temp_args, parameters)

        self._nav_temp_args = None

    @property
    def virtual(self) -> bool:
        """Is navigator virtual? (False)."""
        return False


def route(route_name: str) -> Any:
    """Link route to last initialized navigator."""
    def _route_decorator(page_definition: PageDefinition) -> None:
        _pre_def_routes[route_name] = page_definition

    return _route_decorator


def define_page(path: str, name: str=None) -> PageDefinition:
    """Get page from module."""
    path = path.replace('\\', '.').replace('/', '.')

    page = None

    try:
        page = getattr(import_module(path), path.split('.')[-1] if not name else name)
    except AttributeError:
        warn_explicit(f'Unable to define page: "{path}".', Warning, 'flet_navigator::define_page', 750)

    return page


def parameters(route: str, **_parameters: dict) -> str:
    """Append route with parameters."""
    return f'{route}?{"&".join(f"{key}={value}" for key, value in _parameters.items())}' if len(_parameters) >= 1 else route

def parameters_(route: str, **_parameters: dict) -> str:
    """Append route with parameters."""
    return parameters(route, **_parameters);

def template(template_definition: Union[str, TemplateDefinition], page_data: PageData, arguments: Arguments=None) -> Union[Control, None]:
    """Render template."""
    if isinstance(template_definition, str):
        if template_definition in _global_templates:
            return _global_templates[template_definition](page_data, arguments)

        else:
            warn_explicit(
                f'No template found: `{template_definition}`.', Warning,
                'flet_navigator_main::template', 771)

    else:
        return template_definition(page_data, arguments)


def global_template(template_name: str=None) -> Any:
    """Register global template to last initialized navigator."""
    if isinstance(template_name, Callable):
        _global_templates[template_name.__name__] = template_name

    else:
        def _global_template(template: TemplateDefinition) -> None:
            _global_templates[template.__name__ if not template_name or not isinstance(template_name, str) else template_name] = template

        return _global_template


def render(page: Page=None, routes: Routes={}, args: Arguments=None, parameters: dict[str, Any]=None, route_changed_handler: RouteChangedHandler=None, navigator_animation: NavigatorAnimation=NavigatorAnimation(), virtual: bool=False) -> None:
    """Shortcut for rendering page at start (`Nav(page?).render(page)`)."""
    if virtual:
        VirtualFletNavigator(routes, route_changed_handler, navigator_animation).render(page, args)

    else:
        FletNavigator(page, routes, route_changed_handler, navigator_animation).render(page, args, parameters)

def anon(function: Callable, *args: tuple, **kwargs: dict) -> Callable:
    """Shortcut for anonymous redirection that doesn't require page as argument."""
    return lambda _: function(*args, **kwargs)

def anon_argless(function: Callable, *args: tuple, **kwargs: dict) -> Callable:
    """Shortcut for non-flet anonymous redirection that doesn't require page as argument."""
    return lambda: function(*args, **kwargs)

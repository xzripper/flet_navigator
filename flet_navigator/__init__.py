"""Navigator for Flet."""

from flet import Page

from typing import Callable, Any


FLET_NAVIGATOR_VERSION: float = '1.0.1'
"""Flet Navigator Version."""

ROUTE_404: str = 'ROUTE-404'
"""Route 404 Typehint."""

class FletNavigator:
    """Flet Navigator Class."""

    route: str = '/'
    """Current route."""

    routes: dict[str, Callable[[Page, 'FletNavigator', tuple[Any]], None]] = {}
    """All supported routes."""

    route_changed_handler: Callable[[str], None] = None
    """On route changed handler."""

    def __init__(self, routes: dict[str, Callable[[Page, 'FletNavigator', tuple[Any]], None]], route_changed_handler: Callable[[str], None]=None) -> None:
        """Initialize Flet Navigator."""
        self.routes = routes

        self.route_changed_handler = route_changed_handler

    def navigate(self, route: str, page: Page, args: tuple[Any]=None) -> None:
        """Navigate to specific route."""
        self.route = route

        self.render(page, args)

    def render(self, page: Page, args: tuple[Any]=None) -> None:
        """Render current route. If there is no route like that throw ROUTE-404 (if specified)."""
        if self.route not in self.routes:
            if ROUTE_404 in self.routes:
                page.clean()

                self.routes[ROUTE_404](page, self, args)

        else:
            for route in self.routes:
                if self.route == route:
                    page.clean()

                    self.routes[route](page, self, args)

                    page.update()

                    if self.route_changed_handler:
                        self.route_changed_handler(route)

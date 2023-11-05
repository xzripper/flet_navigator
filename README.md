<h1 align="center">FletNavigator V1.0.0</h1>
<i><p align="center">Simple and fast navigator (router) for Flet (Python) [<code>pip install flet_navigator</code>].</p>
<p align="center">Using Example:

```python
from flet import app, Page, Text, FilledButton, TextThemeStyle

from flet_navigator import FletNavigator, Any, ROUTE_404

from random import randint


def main_page(page: Page, navigator: FletNavigator, args: tuple[Any]) -> None:
    page.add(Text('Main Page!', style=TextThemeStyle.DISPLAY_MEDIUM))

    if args:
        page.add(Text(f'Message from {args[0]}: {args[1]}.'))

    page.add(
        FilledButton(
            'Navigate to second page!',

            on_click=lambda _: navigator.navigate('second_page', page, ('main page', 'Hello from main page!'))
        )
    )

    page.add(
        FilledButton(
            'Navigate to really_non_existent_page!',

            on_click=lambda _: navigator.navigate('really_non_existent_page', page)
        )
    )

def second_page(page: Page, navigator: FletNavigator, args: tuple[Any]) -> None:
    page.add(Text('Second Page!', style=TextThemeStyle.DISPLAY_SMALL))

    page.add(Text(f'Message from {args[0]}: {args[1]}'))

    page.add(
        FilledButton(
            'Navigate to main page!',

            on_click=lambda _: navigator.navigate('/', page, ('second page', randint(1, 100)))
        )
    )

def route_404(page: Page, navigator: FletNavigator, args: tuple[Any]) -> None:
    page.add(Text('How did you get here? There is no page like this registered in routes...'))

    page.add(
        FilledButton(
            'Navigate to the main page until it is too late...',

            on_click=lambda _: navigator.navigate('/', page)
        )
    )

def main(page: Page) -> None:
    flet_navigator = FletNavigator(
        {
            '/': main_page,
            'second_page': second_page,
            ROUTE_404: route_404
        }, lambda route: print(f'Route changed!: {route}')
    )

    flet_navigator.render(page)

app(target=main)
```

</p>

There is no documentation, or more examples, because you can use FletNavigator just by researching this small example! Also every function, and class field has own docstring.<br>
This example will be updated in next releases to keep everything up to date.

<hr>
<p align="center">FletNavigator v1.0.0.</p></i>

<h1 align="center"><b>⚓ FletNavigator V3</b></h1>
<p align="center"><img src="https://img.shields.io/badge/V3.10.11-880808?style=for-the-badge&logo=flutter&logoColor=white" width=117>
<img src="https://img.shields.io/badge/Python%203.9%2B-880808?style=for-the-badge&logo=python&logoColor=white" width=151>
<img src="https://img.shields.io/badge/Awesome%20Flet-880808?style=for-the-badge&logo=styledcomponents&logoColor=white&logoSize=auto" width=185></p>

<p align="center"><b>FletNavigator is a thorough navigation/routing module for the Flet framework that combines speed, simplicity, and efficiency. Features like cross-page arguments, URL parameters, templates, external routes, utilities & decorators, and more are present in FletNavigator! Install it and try it for yourself!</b></p>

<p align="center"><b>Copy&Paste into your terminal: <code>pip install <a href="https://pypi.org/project/flet-navigator/">flet_navigator</a></code></b></p>

<p align="center"><img src="https://github.com/xzripper/flet_navigator/blob/main/mini.gif?raw=true"></p>

<b>

```python
from flet import app, Text, FilledButton

from flet_navigator import RouteContext, route, fn_process


@route('/')
def main(ctx: RouteContext) -> None:
    ctx.add(Text('Hello World!'))

    ctx.add(FilledButton('Navigate to the second page!', on_click=lambda _: ctx.navigate('second')))

@route
def second(ctx: RouteContext) -> None:
    ctx.add(Text('I am the second page!'))

    ctx.add(FilledButton('Return to the homepage!', on_click=lambda _: ctx.navigate_homepage()))

app(fn_process())
```
</b>

<p align="center"><a href="https://xzripper.github.io/flet_navigator"><b>→ Read the official web API documentation.</b></a></p>

<hr><p align="center"><b>FletNavigator 2025</b></p>

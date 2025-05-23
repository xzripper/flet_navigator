<h1 align="center"><b>⚡ FletNavigator V3</b></h1>
<p align="center"><img src="https://img.shields.io/badge/V3.9.6-black?style=for-the-badge&logo=flutter&logoColor=white" width=100>
<img src="https://img.shields.io/badge/Python%203.9%2B-black?style=for-the-badge&logo=python&logoColor=white" width=150>
<img src="https://img.shields.io/badge/Awesome%20Flet-black?style=for-the-badge&logo=styledcomponents&logoColor=white&logoSize=auto" width=185></p>

<p align="center"><b>FletNavigator is a thorough navigation/routing module for the Flet framework that combines speed, simplicity, and efficiency. It supports cross-page templates, cross-page argument passing, URL parameters, 404 page customization, and other useful features, all with only ~120 lines of code (not including blank lines or docstrings). Install it and see for yourself!</b></p>

<p align="center"><b>Copy&Paste into your terminal: <code>pip install <a href="https://pypi.org/project/flet-navigator/">flet_navigator</a></code></b></p>

<p align="center"><img src="https://github.com/xzripper/flet_navigator/blob/main/mini.gif?raw=true"></p>

<b>

```python
from flet import app, Text, FilledButton

from flet_navigator import PublicFletNavigator, PageData, route


@route('/')
def main(pg: PageData) -> None:
    pg.add(Text('Hello World!'))

    pg.add(FilledButton('Navigate to the second page!', on_click=lambda _: pg.navigate('second')))

@route
def second(pg: PageData) -> None:
    pg.add(Text('I am the second page!'))

    pg.add(FilledButton('Return to the homepage!', on_click=lambda _: pg.navigate_homepage()))

app(lambda page: PublicFletNavigator(page).render(page))
```
</b>

<p align="center"><a href="https://github.com/xzripper/flet_navigator/blob/main/flet-navigator-docs.md"><b>-> Check the documentation <-</b></a></p>

<hr><p align="center"><b>FletNavigator 2025</b></p>

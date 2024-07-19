<h1 align="center">FletNavigator V2.<br><img src="https://img.shields.io/badge/V2.8.5-white?style=for-the-badge&logo=flutter&logoColor=red"> <img src="https://img.shields.io/badge/STABLE-white?style=for-the-badge&logo=python&logoColor=black"> <img src="https://img.shields.io/badge/AWESOME%20FLET-white?style=for-the-badge&logo=adventofcode&logoColor=black"><br><img src="https://img.shields.io/github/issues/xzripper/flet_navigator?style=for-the-badge&color=white"> <img src="https://img.shields.io/github/issues-closed/xzripper/flet_navigator?style=for-the-badge&color=white"> <img src="https://img.shields.io/github/last-commit/xzripper/flet_navigator/main?style=for-the-badge&color=white"></h1>
<p align="center"><img src="example2.gif" width=600><br><i>FletNavigator & <a href="https://github.com/xzripper/flet_restyle">FletReStyle</a>.</i></p>
<p align="center">Simple and fast navigator (router) for Flet (Python) that allows you to create multi-page applications! [<code>pip install flet_navigator</code>].<br><br>Click for <b><a href="https://github.com/xzripper/flet_navigator/blob/main/flet-navigator-docs.md">documentation</a>.</b></p><br>
<p align="center">Example:

```python
from flet import app, Text

from flet_navigator import PageData, render, anon, route


@route('/')
def main_page(pg: PageData) -> None:
    pg.add(Text('Main Page!')) # or `pg.page.add`.

@route('second_page')
def second_page(pg: PageData) -> None:
    ... # Second page content.

app(anon(render))
```

</p><br>

<p align="center"><img src="example.gif" width=500></p> <p align="center"><i>(Old Example GIF).</i></p>

See documentation <a href="https://github.com/xzripper/flet_navigator/blob/main/flet-navigator-docs.md">here</a>.

<hr>
<p align="center"><b>FletNavigator v2.8.5.</b></p>

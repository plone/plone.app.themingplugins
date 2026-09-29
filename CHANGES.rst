Changelog
=========

2.0.0 (unreleased)
------------------

Breaking changes:

- Drop support for Python 2 and Plone 4/5. Supported: Plone 6.0-6.3,
  Python 3.9+.
  [remdub]

- Replace ``pkg_resources`` namespace with PEP 420 native namespace,
  move to a ``src`` layout and move package metadata from ``setup.py``
  to ``pyproject.toml``.
  [remdub]


1.2 (2024-10-21)
----------------

- Python3 compat: Fix bytes decoding for views.cfg file


1.1 (2019-04-26)
----------------

- Python 3 compat, code-style.
  [jensens]

1.0 (2015-08-20)
----------------

- Fix parsing of views plugin settings
  [tlyng]

- Add `Quick Example` section to README
  [djowett]


1.0b1
-----

- Initial release spun off from plone.app.theming
  [optilude]

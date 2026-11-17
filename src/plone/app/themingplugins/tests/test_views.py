from App.config import getConfiguration
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.theming.interfaces import IThemeSettings
from plone.app.themingplugins.testing import THEMINGPLUGINS_FUNCTIONAL_TESTING
from plone.registry.interfaces import IRegistry
from plone.testing.zope import Browser
from Products.CMFCore.Expression import Expression
from Products.CMFCore.Expression import getExprContext
from urllib.error import HTTPError
from zope.component import getUtility

import unittest


class TestCase(unittest.TestCase):

    layer = THEMINGPLUGINS_FUNCTIONAL_TESTING

    def setUp(self):
        # Enable debug mode always to ensure cache is disabled by default
        getConfiguration().debug_mode = True

        self.settings = getUtility(IRegistry).forInterface(IThemeSettings)

        self.settings.enabled = False
        self.settings.rules = "python://plone.app.theming/tests/rules.xml"
        self.settings.parameterExpressions = {
            "stringParam": "string:string param value",
            "boolParam": "python:False",
            "requestParam": "request/useother | string:off",
        }

        import transaction

        transaction.commit()

    def tearDown(self):
        getConfiguration().debug_mode = False

    def evaluate(self, context, expression):
        ec = getExprContext(context, context)
        expr = Expression(expression)
        return expr(ec)

    def test_views_plugin_default(self):
        app = self.layer["app"]
        portal = self.layer["portal"]

        self.settings.enabled = True
        self.settings.rules = "/++theme++plone.app.themingplugins.tests/rules.xml"
        self.settings.currentTheme = "plone.app.themingplugins.tests"
        import transaction

        transaction.commit()

        browser = Browser(app)
        browser.open(portal.absolute_url() + "/@@test-view")

        self.assertTrue("<h1>Test view</h1>" in browser.contents)
        self.assertTrue("<div>Plone site</div>" in browser.contents)

    def test_views_plugin_disabled(self):
        app = self.layer["app"]
        portal = self.layer["portal"]

        self.settings.enabled = False
        self.settings.rules = "/++theme++plone.app.themingplugins.tests/rules.xml"
        self.settings.currentTheme = "plone.app.themingplugins.tests"
        import transaction

        transaction.commit()

        browser = Browser(app)

        try:
            browser.open(portal.absolute_url() + "/@@test-view")
        except HTTPError as e:
            self.assertEqual(e.code, 404)
        else:
            self.fail()

    def test_views_plugin_name(self):
        app = self.layer["app"]
        portal = self.layer["portal"]

        self.settings.enabled = True
        self.settings.rules = "/++theme++plone.app.themingplugins.tests/rules.xml"
        self.settings.currentTheme = "plone.app.themingplugins.tests"
        import transaction

        transaction.commit()

        browser = Browser(app)
        browser.open(portal.absolute_url() + "/@@other-name-view")

        self.assertTrue("<h1>Name view</h1>" in browser.contents)
        self.assertTrue("<div>Plone site</div>" in browser.contents)

    def test_views_plugin_context(self):
        app = self.layer["app"]
        portal = self.layer["portal"]

        setRoles(portal, TEST_USER_ID, ("Manager",))
        portal.invokeFactory("Folder", "f1", title="Folder 1")
        setRoles(portal, TEST_USER_ID, ("Member",))

        self.settings.enabled = True
        self.settings.rules = "/++theme++plone.app.themingplugins.tests/rules.xml"
        self.settings.currentTheme = "plone.app.themingplugins.tests"
        import transaction

        transaction.commit()

        browser = Browser(app)
        browser.open(portal.absolute_url() + "/@@context-view")

        self.assertTrue("<h1>Context view</h1>" in browser.contents)
        self.assertTrue("<div>Plone site</div>" in browser.contents)

        try:
            browser.open(portal.absolute_url() + "/f1/@@context-view")
        except HTTPError as e:
            self.assertEqual(e.code, 404)
        else:
            self.fail()

    def test_views_plugin_class(self):
        app = self.layer["app"]
        portal = self.layer["portal"]

        self.settings.enabled = True
        self.settings.rules = "/++theme++plone.app.themingplugins.tests/rules.xml"
        self.settings.currentTheme = "plone.app.themingplugins.tests"
        import transaction

        transaction.commit()

        browser = Browser(app)
        browser.open(portal.absolute_url() + "/@@class-view")

        self.assertTrue("<h1>Class view</h1>" in browser.contents)
        self.assertTrue("<div>Plone site</div>" in browser.contents)
        self.assertTrue(
            "<div>%s/@@class-view</div>" % portal.absolute_url() in browser.contents
        )

    def test_views_plugin_permission(self):
        app = self.layer["app"]
        portal = self.layer["portal"]

        self.settings.enabled = True
        self.settings.rules = "/++theme++plone.app.themingplugins.tests/rules.xml"
        self.settings.currentTheme = "plone.app.themingplugins.tests"
        import transaction

        transaction.commit()

        browser = Browser(app)

        browser.open(portal.absolute_url() + "/@@permission-view")
        self.assertIn("login", browser.url)

        # Don't try this at home, kids
        portal.manage_permission("Manage portal", ["Anonymous"], acquire=False)
        import transaction

        transaction.commit()

        browser.open(portal.absolute_url() + "/@@permission-view")

        self.assertTrue("<h1>Permission view</h1>" in browser.contents)
        self.assertTrue("<div>Plone site</div>" in browser.contents)

from plone.app.theming.interfaces import IThemeSettings
from plone.app.themingplugins.testing import THEMINGPLUGINS_FUNCTIONAL_TESTING
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from Products.CMFCore.Expression import Expression
from Products.CMFCore.Expression import getExprContext
from zope.component import getUtility

import Globals
import unittest2 as unittest


class TestCase(unittest.TestCase):

    layer = THEMINGPLUGINS_FUNCTIONAL_TESTING

    def setUp(self):
        # Enable debug mode always to ensure cache is disabled by default
        Globals.DevelopmentMode = True

        self.settings = getUtility(IRegistry).forInterface(IThemeSettings)

        self.settings.enabled = False
        self.settings.rules = (
            u'python://plone.app.themingplugins/tests/rules.xml'
        )
        self.settings.parameterExpressions = {
            'stringParam': 'string:string param value',
            'boolParam': 'python:False',
            'requestParam': 'request/useother | string:off',
        }

        import transaction

        transaction.commit()

    def tearDown(self):
        Globals.DevelopmentMode = False

    def evaluate(self, context, expression):
        ec = getExprContext(context, context)
        expr = Expression(expression)
        return expr(ec)

    def test_overrides_plugin_enabled(self):
        app = self.layer['app']
        portal = self.layer['portal']

        self.settings.enabled = True
        self.settings.rules = (
            u'/++theme++plone.app.themingplugins.tests/overridesrules.xml'
        )
        self.settings.currentTheme = u"plone.app.themingplugins.tests"
        import transaction

        transaction.commit()

        browser = Browser(app)
        browser.open(portal.absolute_url())

        # Title - pulled in with rules.xml
        self.assertTrue(portal.title in browser.contents)

        # Elsewhere - not pulled in
        self.assertFalse("Accessibility" in browser.contents)

        # The theme
        self.assertTrue("This is the theme" in browser.contents)

        # The customised template
        self.assertTrue("Powered by Diazo" in browser.contents)

    def test_overrides_plugin_disabled(self):
        app = self.layer['app']
        portal = self.layer['portal']

        self.settings.enabled = False
        self.settings.rules = (
            u'/++theme++plone.app.themingplugins.tests/overridesrules.xml'
        )
        self.settings.currentTheme = u"plone.app.themingplugins.tests"
        import transaction

        transaction.commit()

        browser = Browser(app)
        browser.open(portal.absolute_url())

        self.assertTrue(portal.title in browser.contents)
        self.assertTrue("Accessibility" in browser.contents)
        self.assertFalse("This is the theme" in browser.contents)
        self.assertFalse("Powered by Diazo" in browser.contents)

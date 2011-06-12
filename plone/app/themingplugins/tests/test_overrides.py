import unittest2 as unittest

from plone.app.theming.testing import THEMING_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser

import Globals

from Products.CMFCore.Expression import Expression, getExprContext

from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from plone.app.theming.interfaces import IThemeSettings

class TestCase(unittest.TestCase):

    layer = THEMING_FUNCTIONAL_TESTING

    def setUp(self):
        # Enable debug mode always to ensure cache is disabled by default
        Globals.DevelopmentMode = True

        self.settings = getUtility(IRegistry).forInterface(IThemeSettings)

        self.settings.enabled = False
        self.settings.rules = u'python://plone.app.theming/tests/rules.xml'
        self.settings.parameterExpressions = {
                'stringParam': 'string:string param value',
                'boolParam': 'python:False',
                'requestParam': 'request/useother | string:off'
            }

        import transaction; transaction.commit()

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
        self.settings.rules = u'/++theme++plone.app.theming.tests/overridesrules.xml'
        self.settings.currentTheme = u"plone.app.theming.tests"
        import transaction; transaction.commit()

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
        self.settings.rules = u'/++theme++plone.app.theming.tests/overridesrules.xml'
        self.settings.currentTheme = u"plone.app.theming.tests"
        import transaction; transaction.commit()

        browser = Browser(app)
        browser.open(portal.absolute_url())

        self.assertTrue(portal.title in browser.contents)
        self.assertTrue("Accessibility" in browser.contents)
        self.assertFalse("This is the theme" in browser.contents)
        self.assertFalse("Powered by Diazo" in browser.contents)

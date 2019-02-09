from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig


class ThemingPlugins(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import plone.app.themingplugins.tests

        xmlconfig.file(
            'configure.zcml',
            plone.app.themingplugins.tests,
            context=configurationContext,
        )

        # Run the startup hook
        from plone.app.theming.plugins.hooks import onStartup

        onStartup(None)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'plone.app.theming:default')


THEMINGPLUGINS_FIXTURE = ThemingPlugins()
THEMINGPLUGINS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(THEMINGPLUGINS_FIXTURE,), name="ThemingPlugins:Integration"
)
THEMINGPLUGINS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(THEMINGPLUGINS_FIXTURE,), name="ThemingPlugins:Functional"
)

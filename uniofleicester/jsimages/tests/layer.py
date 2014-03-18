from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import PLONE_FIXTURE

from zope.configuration import xmlconfig


class CookieLawSuite(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import uniofleicester.jsimages
        xmlconfig.file('configure.zcml', uniofleicester.jsimages,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'uniofleicester.jsimages:default')

    def tearDownZope(self, app):
        pass


FIXTURE = CookieLawSuite()
INTEGRATION_TESTING = IntegrationTesting(
                                        bases=(FIXTURE,),
                                        name="Integration"
                                    )
FUNCTIONAL_TESTING = FunctionalTesting(
                                        bases=(FIXTURE,),
                                        name="Functional"
                                    )

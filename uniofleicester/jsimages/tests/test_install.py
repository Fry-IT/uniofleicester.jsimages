# -*- coding: utf8 -*-
from plone import api
import unittest2
from plone.testing.z2 import Browser

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import login, setRoles
import transaction

from uniofleicester.jsimages.tests.layer import FUNCTIONAL_TESTING
from uniofleicester.jsimages.tests.layer import INTEGRATION_TESTING


class IntegrationTest(unittest2.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def testSetup(self):
        # browser layer
        from uniofleicester.jsimages.interfaces import IUOLImagesThemeLayer
        from plone.browserlayer.utils import registered_layers
        self.assertTrue(IUOLImagesThemeLayer in registered_layers())

        pt = api.portal.get_tool('portal_types')
        self.assertTrue(pt.getTypeInfo('Gallery'))

        # configlet
        #cp = api.portal.get_tool('portal_controlpanel')
        #actions = cp.listActions()
        #a_ids = [x.id for x in actions]
        #self.assertTrue('cookielaw-controlpanel' in a_ids)
        #for act in actions:
        #    if act.id == 'cookielaw-controlpanel':
        #        self.assertEqual(act.category, 'Products')

        # css registry
        css = api.portal.get_tool('portal_css')
        css_ids = css.getResourceIds()
        self.assertTrue('++resource++uniofleicester.jsimages/styles.css' in css_ids)
        self.assertTrue('++resource++uniofleicester.jsimages/photoswipe.css' in css_ids)

        # js registry
        js = api.portal.get_tool('portal_javascripts')
        js_ids = js.getResourceIds()
        self.assertTrue('++resource++uniofleicester.jsimages/simple-inheritance.min.js' in js_ids)
        self.assertTrue('++resource++uniofleicester.jsimages/code-photoswipe-jQuery-1.0.11.min.js' in js_ids)

        # configuration registry
        #record = api.portal.get_registry_record(
        #    'collective.cookielaw.controlpanel.ICookieLawPanel.more_url')
        #self.assertEqual(record, u'/cookies')

        # skins
        #skins = api.portal.get_tool('portal_skins')
        #for skin in skins.getSkinPaths():
        #    self.assertIn('cookielaw', skin[1].split(','))

    def testUninstall(self):
        qi = api.portal.get_tool('portal_quickinstaller')

        # the add-on should be installed
        installed = [x['id'] for x in qi.listInstalledProducts()]
        self.assertTrue('uniofleicester.jsimages' in installed)

        # so let's uninstall it
        qi.uninstallProducts(products=['uniofleicester.jsimages'])
        installed = [x['id'] for x in qi.listInstalledProducts()]
        self.assertFalse('uniofleicester.jsimages' in installed)

        # Uninstall new Gallery type
        pt = api.portal.get_tool('portal_types')
        self.assertFalse(pt.getTypeInfo('Gallery'))

        # browser layer
        from uniofleicester.jsimages.interfaces import IUOLImagesThemeLayer
        from plone.browserlayer.utils import registered_layers
        self.assertFalse(IUOLImagesThemeLayer in registered_layers())

        # css registry
        css = api.portal.get_tool('portal_css')
        css_ids = css.getResourceIds()
        self.assertFalse('++resource++uniofleicester.jsimages/styles.css' in css_ids)
        self.assertFalse('++resource++uniofleicester.jsimages/photoswipe.css' in css_ids)

        # js registry
        js = api.portal.get_tool('portal_javascripts')
        js_ids = js.getResourceIds()
        self.assertFalse('++resource++uniofleicester.jsimages/simple-inheritance.min.js' in js_ids)
        self.assertFalse('++resource++uniofleicester.jsimages/code-photoswipe-jQuery-1.0.11.min.js' in js_ids)


class FunctionalTest(unittest2.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def testGalleryType(self):
        pt = api.portal.get_tool('portal_types')
        gt = pt.getTypeInfo("Gallery")
        self.assertEqual(gt.allowed_content_types, ("Image", ))
        self.assertEqual(gt.default_view, "gallery_view")

    def testGalleryFolder(self):
        login(self.portal.aq_parent, SITE_OWNER_NAME)

        gallery = api.content.create(self.portal, "Gallery", "gallery", "Gallery")

        # Adding a page should fail
        self.assertRaises(api.content.InvalidParameterError,
                          api.content.create, gallery, "Page", "page", "Page")

        # Adding an image should pass
        img = api.content.create(gallery, "Image", "img1", "Image 1")

        # Commit so it is visible in the browser
        transaction.commit()

        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        browser.open(gallery.absolute_url())

        self.assertTrue('uol-gallery' in browser.contents)
        self.assertTrue(img.absolute_url() in browser.contents)
        self.assertTrue("photoSwipe" in browser.contents)

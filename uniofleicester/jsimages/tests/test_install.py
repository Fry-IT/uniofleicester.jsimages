# -*- coding: utf8 -*-
from os.path import dirname, join
from plone import api
import unittest2
from plone.testing.z2 import Browser

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login, setRoles
import transaction

from uniofleicester.jsimages import tests
from uniofleicester.jsimages.tests.layer import FUNCTIONAL_TESTING
from uniofleicester.jsimages.tests.layer import INTEGRATION_TESTING


def getData(filename):
    """ return contents of the file with the given name """
    filename = join(dirname(tests.__file__), filename)
    return open(filename, 'r').read()


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

        # css registry
        css = api.portal.get_tool('portal_css')
        css_ids = css.getResourceIds()
        self.assertTrue('++resource++uniofleicester.jsimages/styles.css' in css_ids)
        self.assertTrue('++resource++uniofleicester.jsimages/photoswipe.css' in css_ids)
        self.assertTrue('++resource++uniofleicester.jsimages/bjqs.css' in css_ids)

        # js registry
        js = api.portal.get_tool('portal_javascripts')
        js_ids = js.getResourceIds()
        self.assertTrue('++resource++uniofleicester.jsimages/simple-inheritance.min.js' in js_ids)
        self.assertTrue('++resource++uniofleicester.jsimages/code-photoswipe-jQuery-1.0.11.min.js' in js_ids)
        self.assertTrue('++resource++uniofleicester.jsimages/bjqs-1.3.js' in js_ids)

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
        self.assertFalse('++resource++uniofleicester.jsimages/bjqs.css' in css_ids)

        # js registry
        js = api.portal.get_tool('portal_javascripts')
        js_ids = js.getResourceIds()
        self.assertFalse('++resource++uniofleicester.jsimages/simple-inheritance.min.js' in js_ids)
        self.assertFalse('++resource++uniofleicester.jsimages/code-photoswipe-jQuery-1.0.11.min.js' in js_ids)
        self.assertFalse('++resource++uniofleicester.jsimages/bjqs-1.3.js' in js_ids)


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
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))

        gallery = api.content.create(self.portal, "Gallery", "gallery", "Gallery")

        # Adding a page should fail
        self.assertRaises(api.content.InvalidParameterError,
                          api.content.create, gallery, "Page", "page", "Page")

        # Adding an image should pass
        img = api.content.create(gallery, "Image", "img1", "Image 1", image=getData('image.jpg'))

        # Commit so it is visible in the browser
        transaction.commit()

        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        browser.open(gallery.absolute_url())

        self.assertTrue('uol-gallery' in browser.contents)
        self.assertTrue(img.absolute_url() in browser.contents)
        self.assertTrue("photoSwipe" in browser.contents)

    def testSlideshowFields(self):
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))

        from Products.Archetypes.atapi import Field
        page = api.content.create(self.portal, "Document", "test-page", "Test Page")
        gallery = api.content.create(self.portal, "Gallery", "gallery", "Gallery")
        img = api.content.create(gallery, "Image", "img1", "Image 1", image=getData('image.jpg'))

        field = page.getField('slideshow_gallery')
        self.assertTrue(isinstance(field, Field), "Page content type does not have a slideshow field")
        field.set(page, gallery)

        page.getField('scale').set(page, 'mini')

        # Commit so it is visible in the browser
        transaction.commit()

        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        browser.open(page.absolute_url())

        self.assertTrue('uol-slideshow' in browser.contents)
        self.assertTrue('"animspeed": 10000' in browser.contents)
        self.assertTrue('"usecaptions": true' in browser.contents)
        self.assertTrue(img.absolute_url() in browser.contents)
        self.assertTrue('"width": 200' in browser.contents)     # bjqs options
        self.assertTrue('width="200"' in browser.contents)     # image size

        page.getField('time_delay').set(page, 5)
        page.getField('show_captions').set(page, False)
        page.getField('scale').set(page, 'preview')
        transaction.commit()

        browser.open(page.absolute_url())
        self.assertTrue('"animspeed": 5000' in browser.contents)
        self.assertTrue('"usecaptions": false' in browser.contents)
        self.assertTrue('"width": 400' in browser.contents)     # bjqs options
        self.assertTrue('width="400"' in browser.contents)     # image size

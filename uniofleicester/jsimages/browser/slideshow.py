import json

from Acquisition import aq_inner

from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.imaging import utils


def field_getter(context, field_name, default=None):
    field = context.getField(field_name)
    if field is None:
        return default
    return field.get(context)


class SlideshowViewlet(ViewletBase):

    def update(self):
        super(SlideshowViewlet, self).update()
        context = aq_inner(self.context)
        self.gallery = field_getter(context, 'slideshow_gallery')
        if isinstance(self.gallery, list):
            self.gallery = self.gallery[0] if len(self.gallery) > 0 else None

        if self.gallery:
            link = field_getter(context, 'slideshow_link', None)
            if link:
                self.slideshow_link = self._get_link(link)
            else:
                self.slideshow_link = self.gallery.absolute_url()
        self.slideshow_scale = field_getter(context, 'scale')

    def images(self):
        if not self.gallery:
            return []

        context = aq_inner(self.context)
        count = field_getter(context, 'image_count', 0)

        contents = self.gallery.getFolderContents({'portal_type': ('Image', )})
        if count != 0:
            contents = contents[:count]

        return [x.getObject() for x in contents]

    def options(self):
        context = aq_inner(self.context)
        delay = field_getter(context, 'time_delay', 10)
        caps = field_getter(context, 'show_captions', True)
        position = field_getter(context, 'slideshow_position', 'right')

        scales = utils.getAllowedSizes()
        width, height = scales.get(self.slideshow_scale, (200, 200))

        data = {
            'animtype': 'slide',
            'height': height,
            'width': width,
            'responsive': True,
            'randomstart': False,
            'showcontrols': True,
            'showmarkers': False,
            'animspeed': delay * 1000,
            'usecaptions': caps,
            'float': position
        }
        return "var opts = {}".format(json.dumps(data))

    def escape(self, text):
        return text.replace('"', '&quot;')

    def _get_link(self, link):
        if link.startswith('http'):
            return link
        try:
            url = str(link)
            url = url.lstrip('/')
            portal = api.portal.get()
            portal.restrictedTraverse(url)
            purl = portal.absolute_url()
            return "%s/%s" % (purl, url)
        except:
            return None

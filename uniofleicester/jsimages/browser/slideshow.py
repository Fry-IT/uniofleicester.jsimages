import json
from Acquisition import aq_inner
from plone.app.layout.viewlets.common import ViewletBase


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

        data = {
            'animtype': 'slide',
            'height': 200,
            'width': 200,
            'responsive': True,
            'randomstart': False,
            'showcontrols': True,
            'showmarkers': False,
            'animspeed': delay * 1000,
            'usecaptions': caps
        }
        return "var opts = {}".format(json.dumps(data))

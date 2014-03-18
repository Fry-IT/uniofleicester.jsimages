from zope.component import adapts
from zope.interface import implements

from Products.Archetypes.atapi import StringField, ReferenceField, \
        AnnotationStorage, IntegerField, StringWidget, BooleanField, \
        BooleanWidget
from Products.ATContentTypes.interfaces import IATDocument
from Products.CMFCore.permissions import ModifyPortalContent

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

from uniofleicester.jsimages.interfaces import IUOLImagesThemeLayer


class ExBooleanField(ExtensionField, BooleanField):
    """ a boolean field """


class ExStringField(ExtensionField, StringField):
    """ a string field """


class ExIntegerField(ExtensionField, IntegerField):
    """ an integer field """


class ExReferenceField(ExtensionField, ReferenceField):
    """ a reference field """


class SlideshowExtender(object):
    adapts(IATDocument)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IUOLImagesThemeLayer

    fields = [
        ExReferenceField('slideshow_gallery',
            schemata='slideshow',
            relationship='relatesToGallery',
            multiValued=False,
            write_permission=ModifyPortalContent,
            allowed_types=("Gallery", ),
            keepReferencesOnCopy=True,
            storage=AnnotationStorage(),
            widget=ReferenceBrowserWidget(
                allow_search=True,
                allow_browse=True,
                show_indexes=False,
                force_close_on_insert=True,
                label=u'Slideshow gallery',
            )
        ),

        ExIntegerField('image_count',
            schemata='slideshow',
            required=True,
            default=0,
            write_permission = ModifyPortalContent,
            languageIndependent=True,
            storage=AnnotationStorage(),
            widget=StringWidget(
                description='Enter 0 for all images',
                label=u'Number of images to show'
            )
        ),

        ExBooleanField('show_captions',
            default=True,
            schemata='slideshow',
            widget = BooleanWidget(
                label="Show image captions"
            )
        ),

        ExIntegerField('time_delay',
            schemata='slideshow',
            required=True,
            default=10,
            write_permission = ModifyPortalContent,
            languageIndependent=True,
            storage=AnnotationStorage(),
            widget=StringWidget(
                description='',
                label=u'Time delay in seconds'
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

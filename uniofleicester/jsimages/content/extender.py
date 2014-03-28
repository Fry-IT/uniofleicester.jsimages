from zope.component import adapts
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.Archetypes.atapi import StringField, ReferenceField, \
        AnnotationStorage, IntegerField, StringWidget, BooleanField, \
        BooleanWidget, SelectionWidget
from Products.ATContentTypes.interfaces import IATDocument
from Products.CMFCore.permissions import ModifyPortalContent

from plone.app.imaging import utils

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

from uniofleicester.jsimages.interfaces import IUOLImagesThemeLayer


class ImageScalesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        sizes = utils.getAllowedSizes()
        values = sorted(sizes.items(), key=lambda x: -x[1][0])
        terms = [SimpleVocabulary.createTerm(x, x, "%s (%s, %s)" % (x, y[0], y[1]))
                 for x, y in values]

        return SimpleVocabulary(terms)


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
            multiValued=True,
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

        ExStringField('scale',
            schemata='slideshow',
            required=True,
            default=10,
            write_permission = ModifyPortalContent,
            languageIndependent=True,
            vocabulary_factory="uniofleicester.jsimages.imagesscalevocabulary",
            enforceVocabulary=1,
            storage=AnnotationStorage(),
            widget=SelectionWidget(
                description='',
                label=u'Image scale to display'
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

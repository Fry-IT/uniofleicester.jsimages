from zope.interface import implements

from Products.validation.i18n import PloneMessageFactory as _
from Products.validation.i18n import recursiveTranslate
from Products.validation.i18n import safe_unicode
from Products.validation.interfaces.IValidator import IValidator
from plone import api


class LinkValidator:

    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        if not value:
            return True
        if value.startswith('http'):
            return True
        try:
            url = str(value)
            url = url.lstrip('/')
            portal = api.portal.get()
            portal.restrictedTraverse(url)
        except:
            msg = _(u"Validation failed($name): $value is not a proper link.",
                mapping={'name': safe_unicode(self.name),
                        'value': safe_unicode(value)})
            return recursiveTranslate(msg, **kwargs)
        return True

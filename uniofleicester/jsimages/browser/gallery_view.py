from Products.Five import BrowserView


class GalleryView(BrowserView):

    def contents(self):
        return self.context.getFolderContents({'portal_type': ('Image', )},
                                              batch=True)

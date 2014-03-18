JS Images UX
============

Add-on that adds a new content type Gallery and extends Page
by a slideshow if a gallery is referenced.

Gallery
-------

Gallery is a new registration of a Plone's ATFolder with a default gallery view
and a restrited allowed types to Image so that no other content types can be inserted.

The overlay solution is build using a PhotoSwipe library - http://photoswipe.com/


Slideshow
---------

A Plone's Page has been extended by four fields:

 - Slideshow gallery - references a Gallery folder
 - Number of images to show
 - Show image captions - whether Image title's should be displayed
 - Time delay in seconds - Time delay between images

If a 'Slideshow gallery' reference is added to a Page a slideshow
viewlet is displayed. The viewlet is registered in the IAboveContentBody viewlet
manager.

The slideshow is build using Basic jQuery Slider - http://www.basic-slider.com/
modified to work with jQuery 1.4.2

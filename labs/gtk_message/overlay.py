#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk, cairo
from math import pi

supports_alpha = True

def create_window(title=None, resizable=True, size=None, parent=None):
    win = gtk.Window()
    if title is not None: 
        win.set_title(title)

    win.set_resizable(resizable)

    if size:
        win.resize(size[0], size[1])

    if parent:
        win.set_transient_for(parent)
    else:
        win.connect('destroy', lambda *args : gtk.main_quit())
    return win


def get_gui_base2(parent_window=None, title=None, resizable=True):
    win = create_window(title=title, resizable=resizable)
    # ==
    # ==
    return win, hbox


def expose (widget, event):
    global supports_alpha
    # ==
    cr = widget.window.cairo_create()
    cr.set_operator(cairo.OPERATOR_CLEAR)      # deletes everything below where an object is drawn
    cr.rectangle(0.0, 0.0, *widget.get_size()) # Makes the mask fill the entire window
    cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)       # Set the compositing operator back to the default

    # Draw a fancy little circle for demonstration purpose
    if supports_alpha:
        cr.set_source_rgba(0.5,1.0,0.0,1)
    else:
        cr.set_source_rgb(0.5,1.0,0.0)
    #==
    cr.arc(widget.get_size()[0]/2,widget.get_size()[1]/2,
           widget.get_size()[0]/2,0,pi*2)
    cr.fill()


def setup():
    global supports_alpha
    # ==
    winmain = create_window(title = "testing", size=(100, 100))
    hbox = gtk.HBox()
    hbox.pack_start(gtk.Label("toto"))
    winmain.add(hbox)

    #===
    win = create_window(parent=winmain, title = "testing")
    win.set_destroy_with_parent(True)
    win.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    win.set_decorated(True)
    win.set_deletable(True)
    #===
    hbox2 = gtk.HBox()
    win.add(hbox2)
    hbox2.pack_start(gtk.Label("toto"))
    btn = gtk.Button("hide")
    btn.connect("clicked", lambda w : win.hide())
    hbox2.pack_start(btn, expand=False, fill=True, padding=10)
    #===
    # Makes the window paintable, so we can draw directly on it
    win.set_app_paintable(True)
    win.set_size_request(100, 100)
    # This sets the windows colormap, so it supports transparency.
    # This will only work if the wm support alpha channel
    screen = win.get_screen()
    colormap = screen.get_rgba_colormap()
    if not colormap:
        supports_alpha = False
        colormap = screen.get_rgb_colormap()
    win.set_colormap(colormap)

    win.connect('expose-event', expose)
    win3 = create_window(parent=winmain, title = "testing")
    return winmain, win, win3


def main():
    wm, w, w3 = setup()
    wm.show_all()
    w.show_all()
    w3.show_all()
    try:
        from IPython.lib.inputhook import enable_gtk
        enable_gtk()
    except ImportError:
        gtk.main()


if __name__ == "__main__":
    main()

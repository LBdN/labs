import context

import os
os.environ["GTK2_RC_FILES"] = os.path.join(os.path.dirname(os.path.realpath(__file__)),  "../../../app/meta_appli/resources/themes/gtk-2.0/gtkrc")
from gamr7_lib.exception_hook import install_pdb_exception_hook
from gamr7_lib.gui import helpers_gui
#from gamr7_lib.full_edit import gui
import gamr7_lib.full_edit.property.inspector_manager as pim
import tests_inspect 
from gamr7_lib.full_edit      import inspector_v2
from gamr7_lib.full_edit.property.property_context import PropertyContext

import gtk

def test_gui_inspector():
    d, w, h = tests_inspect.test_WithDesc_default()
#    d, w, h = tests_inspect.test_WithDesc_instance()
    d.vector[0] = 5.0
    #==
#    h.redo()
#    h.undo()
    #==
    properties_inspector_manager, properties_gui = pim.create_property_inspector_manager()
    p_context = PropertyContext(properties_gui, properties_gui.container)
    inspector_v2.inspect(w, properties_inspector_manager, '', p_context)
#    gui_inspector = gui.create_gtk_edit_inspector()
#    gui_inspector.inspect(w)
    #==
#    win2, box = helpers_gui.get_gui_base2()
#    gui.gui_inspector(box, w)
#    win2.show()
    #==
    win2, box = helpers_gui.get_gui_base2()
    undo = helpers_gui.create_button('undo', set_label=True)
    redo = helpers_gui.create_button('redo', set_label=True)
    quit = helpers_gui.create_button('quit', set_label=True)
    undo.connect('clicked', lambda *args : h.undo())
    redo.connect('clicked', lambda *args : h.redo())
    quit.connect('clicked', lambda *args : gtk.main_quit()) 
    helpers_gui.attach(undo, box)
    helpers_gui.attach(redo, box)
    helpers_gui.attach(quit, box)
    win2.show()
    #==
    gtk.main()

if __name__ == "__main__":
    install_pdb_exception_hook()
    test_gui_inspector()

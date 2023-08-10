import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# nice tutorial for general purposes:
# https://python-gtk-3-tutorial.readthedocs.io/en/latest/builder.html
# .... for treeview
# https://docs.gtk.org/gtk3/treeview-tutorial.html
# or mb simpler
# https://python-gtk-3-tutorial.readthedocs.io/en/latest/treeview.html


class Handler:
    def on_click_button_a2(self, *args):
        print("Hello World1222!")
        Gtk.main_quit()

    def on_click_button3(self, button):
        print("Hello World1!")

    def on_click(self, button):
        print("this action will be evoked")


builder = Gtk.Builder()
builder.add_from_file("../rm/glade_test/test1.glade")
builder.connect_signals(Handler())

# try to fill the treeview
treeview = builder.get_object("treeview_test")


window = builder.get_object("window_test")
window.show_all()

Gtk.main()
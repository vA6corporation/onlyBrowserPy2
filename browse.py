#!/usr/bin/env python3.5

import gi, os
gi.require_version('WebKit2', '4.0')
gi.require_version('Gtk', '3.0')
#gi.require_version('Notify', '0.7')
from gi.repository import WebKit2, Gtk, GLib

op = os.path

class Browser():
    def __init__(self):
        gui= Gtk.Builder()
        gui.add_from_file('gui.glade')
        self.win = gui.get_object('window')
        self.password_dialog = gui.get_object('password_dialog')
        self.message_dialog = gui.get_object('message_dialog')
        self.password_entry = gui.get_object('password_entry')
        self.webLayout = gui.get_object("view")

        self.password_dialog.connect('delete-event', lambda w, e: w.hide() or True)
        self.message_dialog.connect('delete-event', lambda w, e: w.hide() or True)

        #Dark theme
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)
        self.win.set_default_size(500, 500)

        self.win.connect("destroy", Gtk.main_quit)
        #self.win.fullscreen()
        self.win.show()
        gui.connect_signals(self)

        self.webview = WebKit2.WebView()
        #print(dir(self.webview))
        self.webLayout.add(self.webview)
        self.webview.show()

        self.webview.load_uri('http://munisatipo.gob.pe/')
        #self.webview.open('http://www.munisatipo.gob.pe/index.php/galerias')

        self.webview.connect("decide-policy", self.check)
        #self.webview.connect("download-requested", self.download)
        #self.webview.connect("new-window-policy-decision-requested", self.new_window)
        #self.webview.connect("webkit_download_set_destination_uri", self.destino)

    def on_aceptar_button_clicked(self, widget, data=None):
        if self.password_entry.get_text() == "123":
            self.win.destroy()

    def on_message_button_clicked(self, widget, data=None):
        self.message_dialog.hide()

    def on_cancelar_button_clicked(self, widget, data=None):
        self.password_entry.delete_text(0,-1)
        self.password_dialog.hide()

    def on_home_button_clicked(self, widget, data=None):
        self.webview.load_uri('https://www.google.com/')

    def on_refresh_button_clicked(self, widget, data=None):
        self.webview.reload()

    def on_close_button_clicked(self, widget, data=None):
        self.password_dialog.show()

    def on_window_delete_event(self, widget, event, data=None):
        print ("delete event occurred")
        self.password_dialog.show()
        #self.win2.show()
        return True

    def check(self, widget, decision, decision_type ,data=None):
        print(decision_type)
        return False


    def new_window(self, widget, frame, req, nav, policy ,data=None):
        #self.message_dialog.show()
        print("Se abre una ventana")
        policy.download()

        return False

    def download(self, widget, download, data=None):
        print("Hay una descarga")

        print(dir(download))

        DOWNLOAD_DIR = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
        print(DOWNLOAD_DIR)

        name = download.get_suggested_filename()
        print(name)

        ext = op.splitext(name)
        print(ext)

        path = op.join(DOWNLOAD_DIR, name)
        print(path)

        download.set_destination_uri('file://%s' % path)
        print('file://%s' % path)

        #while download.get_status:
        #    print(download.get_status())
        #    pass

        new_dir = str.replace(path, " ", "\ ")
        os.system("evince -f %s" % new_dir)


        #download.set_destination_uri("file://home/vampirodx/hola.txt")
        #download.start(download)
        #down.webkit_download_start()
        return True

Browser()
Gtk.main()

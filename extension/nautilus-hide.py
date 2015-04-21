from gi.repository import Nautilus, GObject
from gettext import gettext, locale, bindtextdomain, textdomain

class NautilusHide(Nautilus.MenuProvider, GObject.GObject):
	def __init__(self):
		pass

	def get_file_items(self, window, files):
		return


	def _setup_gettext(self):
		"""Initializes gettext to localize strings."""
		try: # prevent a possible exception
			locale.setlocale(locale.LC_ALL, "")
		except:
			pass
		bindtextdomain("nautilus-admin", "@CMAKE_INSTALL_PREFIX@/share/locale")
		textdomain("nautilus-admin")

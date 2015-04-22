from gi.repository import Nautilus, GObject
from gettext import gettext, locale, bindtextdomain, textdomain

class NautilusHide(Nautilus.MenuProvider, GObject.GObject):
	"""Simple Nautilus extension that adds some actions to the context menu to
	hide and unhide files, by adding/removing their names to/from the folder's
	'.hidden' file."""
	def __init__(self):
		pass

	def get_file_items(self, window, files):
		"""Returns the menu items to display when one or more files/folders are
		selected."""
		# Add the menu items
		items = []
		self._setup_gettext();
		items += [self._create_hide_item(files)]
		items += [self._create_unhide_item(files)]

		return items


	def _setup_gettext(self):
		"""Initializes gettext to localize strings."""
		try: # prevent a possible exception
			locale.setlocale(locale.LC_ALL, "")
		except:
			pass
		bindtextdomain("nautilus-hide", "@CMAKE_INSTALL_PREFIX@/share/locale")
		textdomain("nautilus-hide")

	def _create_hide_item(self, files):
		"""Creates the 'Hide file(s)' menu item."""
		pass

	def _create_unhide_item(self, files):
		"""Creates the 'Unhide file(s)' menu item."""
		pass


	def _hide_run(self, menu, files):
		"""'Hide file(s)' menu item callback."""
		pass

	def _unhide_run(self, menu, files):
		"""'Unhide file(s)' menu item callback."""
		pass

import os
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
		# Make "files" paths relative and remove files that start with '.'
		# or that end with '~'
		dir_path = None
		filenames = []
		for file in files:
			if dir_path == None:
				dir_path = file.get_parent_location().get_path()
			name = file.get_name()
			if not name.startswith(".") and not name.endswith("~"):
				filenames += [name]

		if dir_path == None or len(filenames) == 0:
			return

		# Check if the user can edit the ".hidden" file
		if os.path.exists(dir_path + "/.hidden"):
			if not os.access(dir_path + "/.hidden", os.R_OK | os.W_OK):
				return
		else:
			if not os.access(dir_path, os.W_OK | os.X_OK):
				return

		# Read the ".hidden" file
		if os.path.exists(dir_path + "/.hidden"):
			with open(dir_path + "/.hidden") as f:
				hidden = {line.strip() for line in f.readlines()}
		else:
			hidden = set()

		# Count number of files that can be hidden and unhidden
		# TODO Only count total no. of files, and check if hidden and visible files exist
		nhidden, nvisible = 0, 0
		for file in filenames:
			if file in hidden:
				nhidden += 1
			else:
				nvisible += 1

		# Add the menu items
		items = []
		self._setup_gettext();
		if nvisible > 0:
			items += [self._create_hide_item(filenames, dir_path, hidden, nvisible)]
		if nhidden > 0:
			items += [self._create_unhide_item(filenames, dir_path, hidden, nhidden)]

		return items


	def _setup_gettext(self):
		"""Initializes gettext to localize strings."""
		try: # prevent a possible exception
			locale.setlocale(locale.LC_ALL, "")
		except:
			pass
		bindtextdomain("nautilus-hide", "@CMAKE_INSTALL_PREFIX@/share/locale")
		textdomain("nautilus-hide")

	def _create_hide_item(self, files, dir_path, hidden, nvisible):
		"""Creates the 'Hide file(s)' menu item."""
		if nvisible == 1:
			item = Nautilus.MenuItem(name="NautilusHide::HideFile",
				                     label=gettext("Hide File"),
				                     tip=gettext("Hide this file"))
		else:
			item = Nautilus.MenuItem(name="NautilusHide::HideFiles",
				                     label=gettext("Hide Files"),
				                     tip=gettext("Hide these files"))
		item.connect("activate", self._hide_run, files, dir_path, hidden)
		return item

	def _create_unhide_item(self, files, dir_path, hidden, nhidden):
		"""Creates the 'Unhide file(s)' menu item."""
		if nhidden == 1:
			item = Nautilus.MenuItem(name="NautilusHide::UnhideFile",
				                     label=gettext("Unhide File"),
				                     tip=gettext("Unhide this file"))
		else:
			item = Nautilus.MenuItem(name="NautilusHide::UnhideFiles",
				                     label=gettext("Unhide Files"),
				                     tip=gettext("Unhide these files"))
		item.connect("activate", self._unhide_run, files, dir_path, hidden)
		return item


	def _hide_run(self, menu, files, dir_path, hidden):
		"""'Hide file(s)' menu item callback."""
		for file in files:
			hidden.add(file)
		with open(dir_path + "/.hidden", "w") as f:
			for file in hidden:
				f.write(file + '\n')
		# TODO Remove file if empty
		# TODO Refresh Nautilus?

	def _unhide_run(self, menu, files, dir_path, hidden):
		"""'Unhide file(s)' menu item callback."""
		for file in files:
			try:
				hidden.remove(file)
			except:
				pass
		with open(dir_path + "/.hidden", "w") as f:
			for file in hidden:
				f.write(file + '\n')
		# TODO Remove file if empty
		# TODO Refresh Nautilus?

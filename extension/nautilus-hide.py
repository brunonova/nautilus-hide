# Copyright (c) 2015 Bruno Nova <brunomb.nova@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
		# or that end with '~' (files that are already hidden)
		dir_path = None # path of the directory
		filenames = []
		for file in files:
			if dir_path == None: # first file: find path to directory
				dir_path = file.get_parent_location().get_path()
				if file.get_uri_scheme() != "file": # must be a local directory
					return
			name = file.get_name()
			if not name.startswith(".") and not name.endswith("~"):
				filenames += [name]

		if dir_path == None or len(filenames) == 0:
			return

		# Check if the user has write access to the ".hidden" file and its
		# directory
		hidden_path = dir_path + "/.hidden" # path to the ".hidden" file
		if not os.access(dir_path, os.W_OK | os.X_OK) or \
		   (os.path.exists(hidden_path) and not os.access(hidden_path, os.R_OK | os.W_OK)):
			return

		# Read the ".hidden" file
		try:
			if os.path.exists(hidden_path):
				with open(hidden_path) as f:
					hidden = {line.strip() for line in f.readlines()}
			else:
				hidden = set()
		except: # ".hidden" file was deleted?
			hidden = set()

		# Determine what menu items to show (Hide, Unhide, or both)
		show_hide, show_unhide = False, False
		for file in filenames:
			if file in hidden:
				show_unhide = True
			else:
				show_hide = True
			if show_hide and show_unhide:
				break

		# Add the menu items
		items = []
		self._setup_gettext();
		if show_hide:
			items += [self._create_hide_item(filenames, hidden_path, hidden)]
		if show_unhide:
			items += [self._create_unhide_item(filenames, hidden_path, hidden)]

		return items


	def _setup_gettext(self):
		"""Initializes gettext to localize strings."""
		try: # prevent a possible exception
			locale.setlocale(locale.LC_ALL, "")
		except:
			pass
		bindtextdomain("nautilus-hide", "@CMAKE_INSTALL_PREFIX@/share/locale")
		textdomain("nautilus-hide")

	def _create_hide_item(self, files, hidden_path, hidden):
		"""Creates the 'Hide file(s)' menu item."""
		if len(files) == 1:
			item = Nautilus.MenuItem(name="NautilusHide::HideFile",
				                     label=gettext("Hide File"),
				                     tip=gettext("Hide this file"))
		else:
			item = Nautilus.MenuItem(name="NautilusHide::HideFiles",
				                     label=gettext("Hide Files"),
				                     tip=gettext("Hide these files"))
		item.connect("activate", self._hide_run, files, hidden_path, hidden)
		return item

	def _create_unhide_item(self, files, hidden_path, hidden):
		"""Creates the 'Unhide file(s)' menu item."""
		if len(files) == 1:
			item = Nautilus.MenuItem(name="NautilusHide::UnhideFile",
				                     label=gettext("Unhide File"),
				                     tip=gettext("Unhide this file"))
		else:
			item = Nautilus.MenuItem(name="NautilusHide::UnhideFiles",
				                     label=gettext("Unhide Files"),
				                     tip=gettext("Unhide these files"))
		item.connect("activate", self._unhide_run, files, hidden_path, hidden)
		return item

	def _update_hidden_file(self, hidden_path, hidden):
		"""Updates the '.hidden' file with the new filenames, or deletes it if
		empty (no files to hide)."""
		try:
			if hidden == set():
				if os.path.exists(hidden_path):
					os.remove(hidden_path)
			else:
				with open(hidden_path, "w") as f:
					for file in hidden:
						f.write(file + '\n')
			# TODO Refresh Nautilus?
		except:
			print("Failed to delete or write to {}!".format(hidden_path))


	def _hide_run(self, menu, files, hidden_path, hidden):
		"""'Hide file(s)' menu item callback."""
		for file in files:
			hidden.add(file)
		self._update_hidden_file(hidden_path, hidden)

	def _unhide_run(self, menu, files, hidden_path, hidden):
		"""'Unhide file(s)' menu item callback."""
		for file in files:
			try:
				hidden.remove(file)
			except: # file not in "hidden"
				pass
		self._update_hidden_file(hidden_path, hidden)

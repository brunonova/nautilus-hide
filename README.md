Nautilus Hide
=============

Nautilus Hide is a simple Python extension for the Nautilus file manager that
adds options to the right-click menu to hide or unhide files.

The extension hides the files without renaming them (i.e. without prefixing a
dot ('.') or suffixing a tilde ('~')).
It does that by adding their names to the folder's `.hidden` file, which
Nautilus reads to hide the listed files the next time you open or refresh the
folder.


Details
-------

In Linux, and other UNIX like systems, a file with a name that starts by a
dot ('.') is considered a *hidden file*.
Some file managers also hide files that end with a tilde ('~'), with are
considered *backup files*.

To hide an existing file, you would have to rename it. That's not always
feasible or desirable.

Some file managers, like Nautilus, offer an **alternative way of hiding files**:
you create a text file that lists, line-by-line, the names of all the files you
want to hide and save it in that folder with the name `.hidden`. The next time
you open or refresh that folder, those files will not be visible.

This extension simply uses that `.hidden` file to hide files. When you choose to
hide a file, its name is added to the folder's `.hidden` file. When you choose
to unhide it, the name is removed.
You will have to refresh the folder to see the result.
Installing Nautilus Hide from source
====================================

1.  Install the dependencies.
    In Ubuntu and Debian, these are the known dependencies:

    *   cmake
    *   gettext
    *   python-nautilus
    *   xdotool

2.  Open a terminal in the project directory and run:

        mkdir build
        cd build
        cmake ..
        make
        sudo make install

3.  If Nautilus is running, restart it:

        nautilus -q

    Then start it again.

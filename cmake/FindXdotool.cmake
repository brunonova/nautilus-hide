find_program(XDOTOOL NAMES xdotool)

if(XDOTOOL_NOTFOUND)
	message (FATAL_ERROR "-- Not Found xdotool: install it first")
else(XDOTOOL_FOUND)
	message ("-- Found xdotool")
endif()

find_package_handle_standard_args(Xdotool "Could not find xdotool!" XDOTOOL)

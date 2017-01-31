find_program(XDOTOOL NAMES xdotool)

if(XDOTOOL_NOTFOUND)
	message (FATAL_ERROR "-- Not Found xdotool: installed first")
else(XDOTOOL_FOUND)
	message ("-- Found xdotool")
endif()

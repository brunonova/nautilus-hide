cmake_minimum_required(VERSION 2.6)
project(NautilusHide NONE)
list (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
find_package(Gettext REQUIRED)
find_package(Xdotool REQUIRED)

configure_file(extension/nautilus-hide.py extension/nautilus-hide.py)

file(GLOB TRANSLATION_FILES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "po/*")
foreach(trans_file ${TRANSLATION_FILES})
    configure_file(${trans_file} ${trans_file} COPYONLY)
endforeach()
file(GLOB PO_FILES "${CMAKE_CURRENT_BINARY_DIR}/po/*.po")
gettext_create_translations("${CMAKE_CURRENT_BINARY_DIR}/po/nautilus-hide.pot"
                            ALL ${PO_FILES})

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/extension/nautilus-hide.py" DESTINATION /usr/share/nautilus-python/extensions)

# Uninstall target
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
               "${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake" IMMEDIATE @ONLY)
add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake)

# Project Needs a name ofcourse
project(plasma-mangaengine)
 
# Find the required Libaries
find_package(KDE4 REQUIRED)
include(KDE4Defaults)

install(DIRECTORY package/
        DESTINATION ${DATA_INSTALL_DIR}/plasma/plasmoids/mangaengine)

install(FILES package/metadata.desktop
        DESTINATION ${SERVICES_INSTALL_DIR}
        RENAME plasma-applet-mangaengine.desktop)

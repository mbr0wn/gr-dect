INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_DECT dect)

FIND_PATH(
    DECT_INCLUDE_DIRS
    NAMES dect/api.h
    HINTS $ENV{DECT_DIR}/include
        ${PC_DECT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    DECT_LIBRARIES
    NAMES gnuradio-dect
    HINTS $ENV{DECT_DIR}/lib
        ${PC_DECT_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(DECT DEFAULT_MSG DECT_LIBRARIES DECT_INCLUDE_DIRS)
MARK_AS_ADVANCED(DECT_LIBRARIES DECT_INCLUDE_DIRS)


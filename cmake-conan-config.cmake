get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}" ABSOLUTE)

include("${PACKAGE_PREFIX_DIR}/deploy/conan.cmake" OPTIONAL)
include("${PACKAGE_PREFIX_DIR}/conan.cmake")

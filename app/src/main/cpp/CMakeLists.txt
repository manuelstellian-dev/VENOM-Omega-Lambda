cmake_minimum_required(VERSION 3.22.1)

project("venom-bridge")

# Creates and names a library, sets it as either STATIC
# or SHARED, and provides the relative paths to its source code.
add_library(
    venom-bridge
    SHARED
    bridge_jni.cpp
)

# Searches for a specified prebuilt library and stores the path as a
# variable. Because CMake includes system libraries in the search path by
# default, you only need to specify the name of the public NDK library
# you want to add. CMake verifies that the library exists before
# completing its build.
find_library(
    log-lib
    log
)

# Specifies libraries CMake should link to your target library.
target_link_libraries(
    venom-bridge
    ${log-lib}
)

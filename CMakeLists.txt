cmake_minimum_required(VERSION 3.20)
project(AreaLight LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ---- Locate Nuke 17 --------------------------------------------------------
set(NUKE_DIR "" CACHE PATH "Root of the Nuke 17 installation")

if(NOT NUKE_DIR)
    foreach(_ver "17.0v1" "17.0v1-Beta.5" "17.0v2" "17.0v3" "17.0v4" "17.1v1")
        if(EXISTS "C:/Program Files/Nuke${_ver}/include/DDImage/GeomOp.h")
            set(NUKE_DIR "C:/Program Files/Nuke${_ver}")
            break()
        endif()
    endforeach()
endif()

if(NOT NUKE_DIR)
    message(FATAL_ERROR
        "Cannot find Nuke 17. Set -DNUKE_DIR=<path> to your Nuke install directory.\n"
        "Example: cmake -S . -B build --preset vs2022 -DNUKE_DIR=\"C:/Program Files/Nuke17.0v1\"")
endif()

message(STATUS "Nuke directory: ${NUKE_DIR}")

set(NUKE_INCLUDE "${NUKE_DIR}/include")

# ---- Required libraries -----------------------------------------------------
set(NUKE_LIBS
    "${NUKE_DIR}/DDImage.lib"
    "${NUKE_DIR}/FnUsdAbstraction.lib"
    "${NUKE_DIR}/FdkBase.2.1.lib"
)

foreach(_lib ${NUKE_LIBS})
    if(NOT EXISTS "${_lib}")
        message(FATAL_ERROR "Required library not found: ${_lib}")
    endif()
endforeach()

# ---- Plugin ----------------------------------------------------------------
add_library(AreaLight SHARED
    UsdAreaLightOp.cpp
    UsdAreaLightOp.h
)

target_include_directories(AreaLight PRIVATE "${NUKE_INCLUDE}")
target_link_libraries(AreaLight PRIVATE ${NUKE_LIBS})

target_compile_definitions(AreaLight PRIVATE
    FN_OS_WINDOWS
    NOMINMAX
    WIN32_LEAN_AND_MEAN
)

set_target_properties(AreaLight PROPERTIES
    PREFIX ""
    SUFFIX ".dll"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugin"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/plugin"
)

# ---- Install ----------------------------------------------------------------
if(WIN32)
    set(INSTALL_DIR "$ENV{USERPROFILE}/.nuke" CACHE PATH "Plugin install directory")
else()
    set(INSTALL_DIR "$ENV{HOME}/.nuke"        CACHE PATH "Plugin install directory")
endif()

install(TARGETS AreaLight
        RUNTIME DESTINATION "${INSTALL_DIR}"
        LIBRARY DESTINATION "${INSTALL_DIR}")

install(FILES menu.py DESTINATION "${INSTALL_DIR}")

cmake_minimum_required (VERSION 3.8.2)
project (Drosophila LANGUAGES CXX VERSION 1.0.0 DESCRIPTION "Drosophila Viewer Dynamics")
set (CMAKE_CXX_STANDARD 14)
set (CMAKE_CXX_STANDARD_REQUIRED ON)

# Drosophila Version
set (MAJOR    1)
set (MINOR    0)
set (REVISION 0)
add_definitions (-DMAJOR=${MAJOR} -DMINOR=${MINOR} -DREVISION=${REVISION})

#################################################################
#                         SETTING VARIABLES                     #
#################################################################

set (CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake/Modules/" ${CMAKE_MODULE_PATH})

if ( NOT APPLE )
  set (CMAKE_SKIP_BUILD_RPATH             FALSE )
  set (CMAKE_BUILD_WITH_INSTALL_RPATH     FALSE )
  set (CMAKE_INSTALL_RPATH_USE_LINK_PATH  TRUE  )
endif()


# make sure that the default is a RELEASE
set(default_build_type "Release")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

if ( CMAKE_COMPILER_IS_GNUCXX )
  if ( OMP )
    add_compile_options (-Wall -Wextra -Wno-unused-result -Wno-unknown-pragmas -Wfatal-errors)
  endif()
  string (REGEX REPLACE "-O3" "-Ofast" CMAKE_CXX_FLAGS_RELEASE ${CMAKE_CXX_FLAGS_RELEASE})
  if (${CMAKE_BUILD_TYPE} STREQUAL "Debug")
    set (CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0 -DDEBUG" )
  endif()
endif()
if ( MSVC )
  add_compile_options (/wd4028)
  add_compile_options (/wd4244)
  add_compile_options (/wd4267)
  add_compile_options (/wd4305)
  add_compile_options (/wd4477)
  add_compile_options (/wd4996)
  #set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /NODEFAULTLIB:MSVCRTD")
  #set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /NODEFAULTLIB:MSVCRT")
  set (CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

if (MSVC)
  add_definitions (-D_CRT_SECURE_NO_DEPRECATE -D_SCL_SECURE_NO_WARNINGS)
endif()

find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)

#################################################################
#                         SETTING DIRECTORIES                   #
#################################################################

set(SRC_DIR    ./src)
set(INC_DIR    ./include)
set(OUT_DIR    ./bin)

set(linked_libs ${OPENGL_gl_LIBRARY} ${OPENGL_glu_LIBRARY} ${OPENGL_LIBRARIES} ${GLUT_LIBRARIES})

file(GLOB CPP    "${SRC_DIR}/*.cpp")
file(GLOB HEADER "${INC_DIR}/*.h"  )

include_directories(${INC_DIR})
include_directories(${OPENGL_INCLUDE_DIRS})
include_directories(${GLUT_INCLUDE_DIR})

#################################################################
#                          SUMMARY                              #
#################################################################

message(STATUS ""                                                                    )
message(STATUS "================= Drosophila configuration Summary =================")
message(STATUS "   Drosophila version: ${MAJOR}.${MINOR}.${REVISION}"                )
message(STATUS ""                                                                    )
message(STATUS "   C++ :"                                                            )
message(STATUS "      C++ Compiler : ${CMAKE_CXX_COMPILER}"                          )
message(STATUS "      C++ flags    :"                                                )
foreach(FLAG ${CMAKE_CXX_FLAGS})
  message(STATUS "                    * ${FLAG}"                                     )
endforeach(FLAG)
if (${CMAKE_BUILD_TYPE} STREQUAL "Release")
  foreach(FLAG ${CMAKE_CXX_FLAGS_RELEASE})
    message(STATUS "                    * ${FLAG}"                                   )
  endforeach(FLAG)
elseif (${CMAKE_BUILD_TYPE} STREQUAL "Debug")
  foreach(FLAG ${CMAKE_CXX_FLAGS_DEBUG})
    message(STATUS "                    * ${FLAG}"                                   )
  endforeach(FLAG)
endif()
message(STATUS "      Linker flags : "                                               )
foreach(FLAG ${linked_libs})
  message(STATUS "                    * ${linked_libs}"                              )
endforeach(FLAG)
message(STATUS ""                                                                    )
message(STATUS "   OpenGL support : ${OPENGL_FOUND}"                                 )
message(STATUS ""                                                                    )

#################################################################
#                         MAIN RULES                            #
#################################################################

add_executable(viewer ${CMAKE_SOURCE_DIR}/viewer.cpp ${CPP})
target_link_libraries(viewer ${linked_libs})

#################################################################
#                          INSTALLERS                           #
#################################################################

install(TARGETS viewer           DESTINATION ${CMAKE_SOURCE_DIR}/${OUT_DIR})

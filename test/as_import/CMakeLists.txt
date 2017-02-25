project(submit)

cmake_minimum_required (VERSION 2.8)

SET(CMAKE_INCLUDE_CURRENT_DIR ON)
include_directories(cpp/include)

set(CMAKE_CXX_FLAGS "${CMAXE_CXX_FLAGS} -Wall")

add_definitions(-std=c++0x)
add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)

set(sources
   studentCode.cpp
   udacityMain.cpp)

add_executable(submit ${sources})

project(student_main)
cmake_minimum_required(VERSION 2.6)

include_directories(include
  $ENV{GRADER_HOME}/include)
add_definitions(-std=c++0x)
set(CMAKE_CXX_FLAGS "${CMAXE_CXX_FLAGS} -Wall")

set(testSources
   testMain.cpp)
set(submitSources
   submitMain.cpp)
add_executable(test_main ${testSources})
add_executable(submit_main ${submitSources})
target_link_libraries(submit_main grader)
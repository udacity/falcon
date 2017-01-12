project(grader_test)
cmake_minimum_required(VERSION 2.6)

include_directories(include
  $ENV{GTEST_HOME}/include
  lib/jsoncpp/include)
link_directories($ENV{GTEST_HOME}/mybuild)
add_definitions(-std=c++0x)
set(CMAKE_CXX_FLAGS "${CMAXE_CXX_FLAGS} -Wall")

set(sources
   lib/jsoncpp/include/jsoncpp.cpp
   test/test_main.cpp
   test/FeedbackTest.cpp
   test/GraderTest.cpp
   test/RubricItemTest.cpp
   test/StatsTest.cpp
   include/Grader.cpp
   include/Feedback.cpp
   include/RubricItem.cpp
   include/Stats.cpp)
add_executable(grader_test ${sources})
target_link_libraries(grader_test gtest)
target_link_libraries(grader_test pthread)
project(grader_test)
cmake_minimum_required(VERSION 2.6)

include_directories(include
  $ENV{GMOCK_HOME}/include
  $ENV{GTEST_HOME}/include
  lib/nlohmann_json/2.0.7/include)
link_directories($ENV{GMOCK_HOME}/mybuild $ENV{GTEST_HOME}/mybuild)
add_definitions(-std=c++0x)
set(CMAKE_CXX_FLAGS "${CMAXE_CXX_FLAGS} -Wall")

set(sources
   test_main.cpp
   FeedbackTest.cpp
   GraderTest.cpp
   RubricItemTest.cpp
   StatsTest.cpp
   Grader.cpp
   include/Feedback.cpp
   include/RubricItem.cpp
   include/Stats.cpp)
add_executable(grader_test ${sources})
target_link_libraries(grader_test pthread)
target_link_libraries(grader_test gmock)
target_link_libraries(grader_test gtest)
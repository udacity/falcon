#include <chrono>
#include <iostream>
#include <string>
#include "gtest/gtest.h"
#include "RubricItem.h"

using namespace ::testing;

class ARubricItem: public Test {
public:
  RubricItem test;
};

TEST_F(ARubricItem, DefaultsToNotCheckpoint) {
  ASSERT_FALSE(test.checkpoint);
}

TEST_F(ARubricItem, DefaultsToIncorrect) {
  ASSERT_FALSE(test.passed());
}

TEST_F(ARubricItem, CanSetAndEvaluateAFunction) {
  int thing = 4;
  test.set_callback([&thing]() { return thing > 0; }); // should pass
  test.evaluate();
}

TEST_F(ARubricItem, CanChangePassFailStateAfterEvaluation) {
  test.set_callback([]() { return true; });
  test.evaluate();
  ASSERT_TRUE(test.passed());
}

TEST_F(ARubricItem, RecordsTimeToEvaluate) {
  test.set_callback([]() { return true; });
  test.evaluate();
  ASSERT_GT(test.evaluation_time_ms(), 0.0);
}

TEST_F(ARubricItem, CanInitializeCorrectFeedback) {
  test.when_correct(std::string("Good job!"));
}

TEST_F(ARubricItem, CanInitializeIncorrectFeedback) {
  test.when_incorrect(std::string("Bad job!"));
}

TEST_F(ARubricItem, CanReportRightFeedbackAfterEvaluation)
{
  std::string right_feedback("right!");
  test.set_callback([]() { return true; });
  test.when_correct(right_feedback);
  test.evaluate();
  ASSERT_EQ(test.get_feedback()->msg, right_feedback);
}

// go back up to grader and make sure it reads the output
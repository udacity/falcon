#include <chrono>
#include <iostream>
#include <string>
#include "gtest/gtest.h"
#include "RubricItem.h"

using namespace ::testing;

class ARubricItem: public Test {
public:
  RubricItem item;
};

/* useful methods */

const std::string right_feedback("riiiiight");
const std::string wrong_feedback("wrooooong");

void evaluate(RubricItem& item)
{
  item.whenIncorrect(wrong_feedback);
  item.whenCorrect(right_feedback);
  item.evaluate();
}

void run_passing_eval(RubricItem& item)
{
  item.setCallback([]() { return true; });
  evaluate(item);
}

void run_failing_eval(RubricItem& item)
{
  item.setCallback([]() { return false; });
  evaluate(item);
}

/* actual tests */

TEST_F(ARubricItem, DefaultsToNotCheckpoint) {
  ASSERT_FALSE(item.checkpoint);
}

TEST_F(ARubricItem, DefaultsToIncorrect) {
  ASSERT_FALSE(item.passed());
}

TEST_F(ARubricItem, DefaultsToNotRun) {
  ASSERT_FALSE(item.ran());
}

TEST_F(ARubricItem, KnowsWhenItRan) {
  run_passing_eval(item);
  ASSERT_TRUE(item.ran());
}

TEST_F(ARubricItem, CanChangePassFailStateAfterEvaluation) {
  run_passing_eval(item);
  ASSERT_TRUE(item.passed());
}

TEST_F(ARubricItem, RecordsTimeToEvaluate) {
  run_passing_eval(item);
  ASSERT_GT(item.evaluation_time_ms(), 0.0);
}

TEST_F(ARubricItem, CanReportRightFeedbackAfterEvaluation)
{
  run_passing_eval(item);
  ASSERT_EQ(item.getFeedback()->msg, right_feedback);
}

// go back up to grader and make sure it reads the output
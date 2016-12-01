#include <iostream>
#include <string>
#include "gtest/gtest.h"
#include "json.hpp"
#include "RubricItem.h"
#include "Stats.h"

using namespace ::testing;
using namespace nlohmann; // for json

class AStats: public Test {
public:
  Stats stats;
};

/* useful methods */

const std::string right_feedback("riiiiight");
const std::string wrong_feedback("wrooooong");

void evaluate(Stats& stats, RubricItem& item)
{
  item.when_incorrect(wrong_feedback);
  item.when_correct(right_feedback);
  item.evaluate();
  stats.record(item);
}

void run_passing_eval(Stats& stats)
{
  RubricItem item([]() { return true; });
  evaluate(stats, item);
}

void run_failing_eval(Stats& stats)
{
  RubricItem item([]() { return false; });
  evaluate(stats, item);
}

/* actual tests */

TEST_F(AStats, InitializesEmpty)
{
  ASSERT_EQ(stats.num_run, 0u);
  ASSERT_EQ(stats.num_passed, 0u);
  ASSERT_EQ(stats.num_failed, 0u);
}

TEST_F(AStats, CanRecordThatAnEvaluatedRubricItemRan)
{
  run_passing_eval(stats);
  ASSERT_EQ(stats.num_run, 1u);
}

TEST_F(AStats, CanRecordWhetherAnEvaluatedRubricItemFailed)
{
  run_failing_eval(stats);
  ASSERT_EQ(stats.num_failed, 1u);
}

TEST_F(AStats, CanRecordRightStudentFeedback)
{
  run_passing_eval(stats);
  json results = stats.get_results();
  const std::string actual_feedback = results["feedback"];
  ASSERT_EQ(actual_feedback, right_feedback);
}

TEST_F(AStats, CanRecordFeedbackForTwoRubricItems)
{
  run_passing_eval(stats);
  run_failing_eval(stats);
  json results = stats.get_results();
  const std::string actual_feedback = results["feedback"];
  ASSERT_EQ(actual_feedback, right_feedback + "\n" + wrong_feedback);
}

TEST_F(AStats, CanRecordRightPassingAfterOneRubricItem)
{
  run_passing_eval(stats);
  json results = stats.get_results();
  const bool is_correct = results["is_correct"];
  ASSERT_TRUE(is_correct);
}
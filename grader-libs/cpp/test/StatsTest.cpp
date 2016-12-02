#include <iostream>
#include <memory>
#include <string>
#include "gtest/gtest.h"
#include "json.hpp"
#include "Grader.h"
#include "RubricItem.h"
#include "Stats.h"

using namespace ::testing;
using namespace nlohmann; // for json
using namespace std;

class AStats: public Test {
public:
  Stats stats;
};

/* useful methods */

const string right_feedback("riiiiight");
const string wrong_feedback("wrooooong");
Grader grader;

void evaluate(Stats& stats, shared_ptr<RubricItem> item)
{
  item->when_incorrect(wrong_feedback);
  item->when_correct(right_feedback);
  item->evaluate();
  stats.record(item);
}

void run_passing_eval(Stats& stats)
{
  auto item = grader.create_rubric_item([]() { return true; });
  evaluate(stats, item);
}

void run_passing_eval(Stats& stats, string name)
{
  auto item = grader.create_rubric_item([]() { return true; });
  item->name = name;
  evaluate(stats, item);
}

void run_failing_eval(Stats& stats)
{
  auto item = grader.create_rubric_item([]() { return false; });
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
  const string actual_feedback = results["feedback"];
  ASSERT_EQ(actual_feedback, right_feedback);
}

TEST_F(AStats, CanRecordFeedbackForTwoRubricItems)
{
  run_passing_eval(stats);
  run_failing_eval(stats);
  json results = stats.get_results();
  const string actual_feedback = results["feedback"];
  ASSERT_EQ(actual_feedback, right_feedback + "\n" + wrong_feedback);
}

TEST_F(AStats, CanRecordRightPassingAfterOneRubricItem)
{
  run_passing_eval(stats);
  json results = stats.get_results();
  const bool is_correct = results["is_correct"];
  ASSERT_TRUE(is_correct);
}

TEST_F(AStats, CanCombineWithAnotherStats)
{
  Stats stats2;
  run_passing_eval(stats);
  run_failing_eval(stats2);
  ASSERT_EQ((stats += stats2).num_run, 2u);
}

TEST_F(AStats, CanAddStats)
{
  Stats stats2;
  run_passing_eval(stats);
  run_failing_eval(stats2);
  Stats combo = stats + stats2;
  ASSERT_EQ(combo.num_run, 2u);
}

TEST_F(AStats, ReportsJSONStatsOnNumberOfTestsRun)
{
  run_passing_eval(stats, "a name");
  string executor_results = stats.json_dump();
  json results = json::parse(executor_results);
  ASSERT_EQ(results["num_run"].get<unsigned>(), 1u);
}
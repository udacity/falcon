#include <iostream>
#include <memory>
#include <string>
#include "gtest/gtest.h"
#include "json/json.h"
#include "Grader.h"
#include "RubricItem.h"
#include "Stats.h"

using namespace ::testing;
using namespace std;
typedef Json::Value json;

class AStats: public Test {
public:
  Stats stats;
  Grader grader;
};

/* useful methods */

const string right_feedback("riiiiight");
const string wrong_feedback("wrooooong");

void evaluate(Stats& stats, shared_ptr<RubricItem> item)
{
  item->whenIncorrect(wrong_feedback);
  item->whenCorrect(right_feedback);
  item->evaluate();
  stats.record(item);
}

void run_passing_eval(Grader& grader, Stats& stats)
{
  auto item = grader.createRubricItem([]() { return true; });
  evaluate(stats, item);
}

void run_passing_eval(Grader& grader, Stats& stats, string name)
{
  auto item = grader.createRubricItem([]() { return true; });
  item->name = name;
  evaluate(stats, item);
}

void run_optional_passing_eval(Grader& grader, Stats& stats)
{
  auto item = grader.createRubricItem([]() { return true; });
  item->optional = true;
  evaluate(stats, item);
}

void run_optional_passing_eval(Grader& grader, Stats& stats, string name)
{
  auto item = grader.createRubricItem([]() { return true; });
  item->name = name;
  item->optional = true;
  evaluate(stats, item);
}

void run_failing_eval(Grader& grader, Stats& stats)
{
  auto item = grader.createRubricItem([]() { return false; });
  evaluate(stats, item);
}

void run_failing_eval(Grader& grader, Stats& stats, string name)
{
  auto item = grader.createRubricItem([]() { return false; });
  item->name = name;
  evaluate(stats, item);
}

void run_optional_failing_eval(Grader& grader, Stats& stats)
{
  auto item = grader.createRubricItem([]() { return false; });
  item->optional = true;
  evaluate(stats, item);
}

void run_optional_failing_eval(Grader& grader, Stats& stats, string name)
{
  auto item = grader.createRubricItem([]() { return false; });
  item->optional = true;
  item->name = name;
  evaluate(stats, item);
}

const json generate_sample_stats(Grader& grader, Stats& stats, int times)
{
  for (int i = 0; i < times; i++)
  {
    if (i % 2 == 0)
      run_passing_eval(grader, stats, string("a name"));
    else
      run_failing_eval(grader, stats, string("a different name"));
  }
  string executor_results = stats.results();
  json results;
  Json::Reader reader;
  reader.parse(executor_results, results);
  return results;
}

const json generate_sample_stats(Grader& grader, int times)
{
  return generate_sample_stats(grader, grader.stats, times);
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
  run_passing_eval(grader, stats);
  ASSERT_EQ(stats.num_run, 1u);
}

TEST_F(AStats, CanRecordWhetherAnEvaluatedRubricItemFailed)
{
  run_failing_eval(grader, stats);
  ASSERT_EQ(stats.num_failed, 1u);
}

TEST_F(AStats, DoesNotBreakIfYouTryToExportStatsWithoutRunningTests)
{
  json results = stats.resultsJson();
  const string actual_feedback = results["feedback"].asCString();
  ASSERT_TRUE(actual_feedback.empty());
}

TEST_F(AStats, CanRecordRightStudentFeedback)
{
  run_passing_eval(grader, stats);
  json results = stats.resultsJson();
  const string actual_feedback = results["feedback"].asCString();
  ASSERT_EQ(actual_feedback, right_feedback);
}

TEST_F(AStats, CanRecordFeedbackForTwoRubricItems)
{
  run_passing_eval(grader, stats);
  run_failing_eval(grader, stats);
  json results = stats.resultsJson();
  const string actual_feedback = results["feedback"].asCString();
  ASSERT_EQ(actual_feedback, right_feedback + "\n" + wrong_feedback);
}

TEST_F(AStats, CanRecordRightPassingAfterOneRubricItem)
{
  run_passing_eval(grader, stats);
  json results = stats.resultsJson();
  const bool is_correct = results["is_correct"].asBool();
  ASSERT_TRUE(is_correct);
}

TEST_F(AStats, DoesNotRecordFailingOptionalRubricItemsAsFails)
{
  run_optional_failing_eval(grader, grader.stats);
  run_passing_eval(grader, grader.stats);
  ASSERT_TRUE(grader.stats.passed());
}

TEST_F(AStats, CanCombineWithAnotherStats)
{
  Stats stats2;
  run_passing_eval(grader, stats);
  run_failing_eval(grader, stats2);
  ASSERT_EQ((stats += stats2).num_run, 2u);
}

TEST_F(AStats, CanAddStats)
{
  Stats stats2;
  run_passing_eval(grader, stats);
  run_failing_eval(grader, stats2);
  Stats combo = stats + stats2;
  ASSERT_EQ(combo.num_run, 2u);
}

TEST_F(AStats, ReportsJSONStatsOnNumberOfRubricItemsRun)
{
  const json results = generate_sample_stats(grader, grader.stats, 5);
  ASSERT_EQ(results["num_run"].asUInt(), 5u);
}

TEST_F(AStats, ReportsJSONStatsOnNumberOfRubricItemsCreated)
{
  const json results = generate_sample_stats(grader, grader.stats, 5);
  ASSERT_EQ(results["num_created"].asUInt(), 5u);
}

TEST_F(AStats, ReportsJSONStatsOnPassedRubricItems)
{
  const json results = generate_sample_stats(grader, grader.stats, 5);
  ASSERT_EQ(results["passed"].size(), static_cast<size_t>(3));
}

TEST_F(AStats, ReportsJSONStatsOnOptionalRubricItems)
{
  const json results = generate_sample_stats(grader, grader.stats, 5);
  ASSERT_EQ(results["num_optional"].asUInt(), 0u);
}

TEST_F(AStats, ReportsJSONStatsOnARunRubricItem)
{
  const json results = generate_sample_stats(grader, grader.stats, 5);
  ASSERT_EQ(results["failed"][0]["name"].asString(), "a different name");
  ASSERT_EQ(results["failed"][0]["tag"].asString(), "");
  ASSERT_EQ(results["failed"][0]["message"].asString(), wrong_feedback);
  ASSERT_GT(results["failed"][0]["elapsed_time"].asDouble(), 0.0);
  ASSERT_FALSE(results["failed"][0]["optional"].asBool());
  ASSERT_FALSE(results["failed"][0]["passed"].asBool());
}

TEST_F(AStats, KnowsHowLongItSpentEvaluating)
{
  run_passing_eval(grader, grader.stats);
  run_passing_eval(grader, grader.stats);
  run_passing_eval(grader, grader.stats);
  ASSERT_GT(grader.resultsJson()["elapsed_time"].asDouble(), 0.0);
}
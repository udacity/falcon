#include <iostream>
#include "gtest/gtest.h"
#include "json.hpp"
#include "Grader.h"

using namespace ::testing;
using namespace std;
using namespace nlohmann;

class AGrader: public Test {
public:
 Grader grader;
};

/* useful methods */

const string right_feedback("riiiiight");
const string wrong_feedback("wrooooong");

void set_feedback(shared_ptr<RubricItem> item)
{
  item->whenIncorrect(wrong_feedback);
  item->whenCorrect(right_feedback);
}

void create_passing_item(Grader& grader)
{
  shared_ptr<RubricItem> item = grader.createRubricItem("this item passes");
  item->setCallback([]() { return true; });
  set_feedback(item);
}

void create_failing_item(Grader& grader)
{
  shared_ptr<RubricItem> item = grader.createRubricItem("this item fails");
  item->setCallback([]() { return false; });
  set_feedback(item);
}

/* actual tests */

TEST_F(AGrader, CanKeepTrackOfTheNumberOfTests)
{
  grader.createRubricItem();
  ASSERT_EQ(grader.stats.num_created, 1u);
}

TEST_F(AGrader, CanGenerateAReportBeforeRunningItems)
{
  json report = grader.resultsJson();
  ASSERT_EQ(report["num_created"].get<unsigned>(), 0u);
}

TEST_F(AGrader, KnowsWhenItRanAtLeastOneTest)
{
  grader.run();
  ASSERT_TRUE(grader.has_run);
}

TEST_F(AGrader, CanRunMoreThanOneTest) {
  create_passing_item(grader);
  create_passing_item(grader);
  grader.run();
  ASSERT_EQ(grader.resultsJson()["num_run"].get<unsigned>(), 2u);
}

TEST_F(AGrader, CanDetermineOverallPassState)
{
  create_passing_item(grader);
  create_passing_item(grader);
  grader.run();
  ASSERT_TRUE(grader.resultsJson()["is_correct"].get<bool>());
}

TEST_F(AGrader, CanDetermineOverallFailState)
{
  create_passing_item(grader);
  create_failing_item(grader);
  grader.run();
  ASSERT_FALSE(grader.resultsJson()["is_correct"].get<bool>());
}

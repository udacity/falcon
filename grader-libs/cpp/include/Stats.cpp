#include <iostream>
#include <memory>
#include <numeric>
#include <string>
#include <vector>
#include "json.hpp"
#include "Stats.h"

using namespace nlohmann; // for json
using namespace std;

string join_with_newline(vector<string>& vec)
{
  string joined = accumulate(++vec.begin(), vec.end(), vec[0], [] (string& a, string& b) {
    return a + '\n' + b;
  });

  return joined;
}

Stats& Stats::operator+=(const Stats& rhs)
{
  for_each(rhs.items.cbegin(), rhs.items.cend(), [this](shared_ptr<RubricItem> item) {
    record(item);
  });

  return *this;
}

Stats Stats::operator+(const Stats& rhs)
{
  Stats lhs = *this;
  return lhs += rhs;
}

void Stats::record(shared_ptr<RubricItem> item)
{
  if (item->ran())
  {
    item->passed() ? num_passed++ : num_failed++;
    num_run++;
    is_correct = (num_passed > 0u && num_failed == 0u) ? true : false;
    appendFeedback(item);
    items.push_back(item);
  }
}

void Stats::appendFeedback(shared_ptr<RubricItem> item)
{
  student_feedback.push_back(item->getFeedback()->format());
}

json Stats::getResults()
{
  buildJsonResults();
  return report;
}

json Stats::buildRubricItemReport(shared_ptr<RubricItem> item)
{
  string name = item->name;
  Feedback* feedback = item->getFeedback();
  return json::parse("{}");
}

json Stats::buildRubricItemsReport()
{
  vector<json> tests;
  for (auto i : items)
  {
    json item = buildRubricItemReport(i);
    tests.push_back(item);
  }
  return tests;
}

void Stats::buildJsonResults()
{
  vector<json> tests = buildRubricItemsReport();
  report["tests"] = tests;
  report["feedback"] = join_with_newline(student_feedback);
  report["is_correct"] = is_correct;
  report["num_created"] = num_created;
  report["num_run"] = num_run;
  report["num_passed"] = num_passed;
  report["num_failed"] = num_failed;
}

string Stats::jsonDump()
{
  buildJsonResults();
  return report.dump();
}
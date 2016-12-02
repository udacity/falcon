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
  Feedback* feedback = item->getFeedback();

  json itemReport;
  itemReport["name"] = item->name;
  itemReport["message"] = feedback->msg;
  itemReport["tag"] = feedback->tag;
  itemReport["elapsed_time"] = item->evaluation_time_ms();

  return itemReport;
}

json Stats::buildRubricItemsReport()
{
  json tests;
  tests["passed"] = {};
  tests["failed"] = {};
  for (auto i : items)
  {
    json item = buildRubricItemReport(i);
    if (i->passed())
      tests["passed"].push_back(item);
    else
      tests["failed"].push_back(item);
  }
  return tests;
}

void Stats::buildJsonResults()
{
  json tests = buildRubricItemsReport();
  report["passed"] = tests["passed"];
  report["failed"] = tests["failed"];
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
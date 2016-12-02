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
    append_feedback(item);
    items.push_back(item);
  }
}

void Stats::append_feedback(shared_ptr<RubricItem> item)
{
  student_feedback.push_back(item->get_feedback()->format());
}

json Stats::get_results()
{
  build_json_results();
  return report;
}

json Stats::build_rubric_item_report(shared_ptr<RubricItem> item)
{
  string name = item->name;
  Feedback* feedback = item->get_feedback();
  return json::parse("{}");
}

json Stats::build_rubric_items_report()
{
  vector<json> tests;
  for (auto i : items)
  {
    json item = build_rubric_item_report(i);
    tests.push_back(item);
  }
  return tests;
}

void Stats::build_json_results()
{
  vector<json> tests = build_rubric_items_report();
  report["tests"] = tests;
  report["feedback"] = join_with_newline(student_feedback);
  report["is_correct"] = is_correct;
  report["num_created"] = num_created;
  report["num_run"] = num_run;
  report["num_passed"] = num_passed;
  report["num_failed"] = num_failed;
}

string Stats::json_dump()
{
  build_json_results();
  return report.dump();
}
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
#include "json.hpp"
#include "Stats.h"

using namespace nlohmann; // for json

std::string join_with_newline(std::vector<std::string>& vec)
{
  std::string joined = std::accumulate(++vec.begin(), vec.end(), vec[0], [] (std::string& a, std::string& b) {
    return a + '\n' + b;
  });

  return joined;
}

void Stats::record(RubricItem& item)
{
  item.passed() ? num_passed++ : num_failed++;
  num_run++;
  is_correct = (num_passed > 0u && num_failed == 0u) ? true : false;
  append_feedback(item);
}

void Stats::append_feedback(RubricItem& item)
{
  student_feedback.push_back(item.get_feedback()->format());
}

json Stats::get_results()
{
  build_json_results();
  return report;
}

void Stats::build_json_results()
{
  report["feedback"] = join_with_newline(student_feedback);
  report["is_correct"] = is_correct;
  // etc
  // std::cout << "json: " <<report.dump() << std::endl;
}

std::string Stats::json_dump()
{
  build_json_results();
  return report.dump();
}
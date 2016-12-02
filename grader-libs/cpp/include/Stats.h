#ifndef Stats_H_
#define Stats_H_

#include <memory>
#include <string>
#include <vector>
#include "json.hpp"
#include "Feedback.h"
#include "RubricItem.h"

using namespace nlohmann; // for json

/**
  Record stats against RubricItems that have run.
*/
class Stats
{
public:
  Stats& operator+=(const Stats&);
  Stats operator+(const Stats&);

  unsigned num_created{0};
  unsigned num_run{0};
  unsigned num_passed{0};
  unsigned num_failed{0};

  std::vector<shared_ptr<RubricItem>> items;

  // assumes that the RubricItem already ran
  void record(shared_ptr<RubricItem>);
  std::string json_dump();
  json get_results();

private:
  json report;
  bool is_correct = false;
  std::vector<std::string> student_feedback;

  json build_rubric_item_report(shared_ptr<RubricItem>);
  json build_rubric_items_report();
  void build_json_results();
  void append_feedback(shared_ptr<RubricItem>);
};

#endif
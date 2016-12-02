#ifndef Stats_H_
#define Stats_H_

#include <memory>
#include <string>
#include <vector>
#include "json.hpp"
#include "Feedback.h"
#include "RubricItem.h"

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

  std::vector<std::shared_ptr<RubricItem>> items;

  // assumes that the RubricItem already ran
  void record(std::shared_ptr<RubricItem>);
  std::string json_dump();
  nlohmann::json get_results();

private:
  nlohmann::json report;
  bool is_correct = false;
  std::vector<std::string> student_feedback;

  nlohmann::json build_rubric_item_report(std::shared_ptr<RubricItem>);
  nlohmann::json build_rubric_items_report();
  void build_json_results();
  void append_feedback(std::shared_ptr<RubricItem>);
};

#endif
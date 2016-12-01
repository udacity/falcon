#ifndef Stats_H_
#define Stats_H_

#include <string>
#include <vector>
#include "json.hpp"
#include "Feedback.h"
#include "RubricItem.h"

using namespace nlohmann; // for json

class Stats
{
public:
  void record(RubricItem&);

  unsigned num_run{0};
  unsigned num_passed{0};
  unsigned num_failed{0};

  std::string json_dump();
  json get_results();

private:
  json report;
  std::vector<std::string> student_feedback;
  bool is_correct = false;

  void build_json_results();
  void append_feedback(RubricItem&);
};

#endif
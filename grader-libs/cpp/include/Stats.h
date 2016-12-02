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

  bool passed();
  bool failed();

  // assumes that the RubricItem already ran
  void record(std::shared_ptr<RubricItem>);
  std::string results();
  nlohmann::json resultsJson();

private:
  nlohmann::json report;
  bool is_correct = false;
  std::vector<std::string> student_feedback;

  double getTotalEvalTime();

  nlohmann::json buildRubricItemReport(std::shared_ptr<RubricItem>);
  nlohmann::json buildRubricItemsReport();
  void buildJsonResults();
  void appendFeedback(std::shared_ptr<RubricItem>);
};

#endif
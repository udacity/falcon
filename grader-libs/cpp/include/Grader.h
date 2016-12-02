#ifndef Grader_H_
#define Grader_H_

#include <memory>
#include <string>
#include <vector>
#include "Stats.h"
#include "RubricItem.h"

class Grader
{
public:
  bool has_evaluated = false;

  Stats stats; // public for testing purposes

  std::shared_ptr<RubricItem> createRubricItem();
  std::shared_ptr<RubricItem> createRubricItem(const std::string&);
  std::shared_ptr<RubricItem> createRubricItem(const std::function<bool()>&);
  void run();
  void run_debug();

  bool failed();
  bool passed();

  std::string getFeedback();

  nlohmann::json resultsJson();
  std::string results();

private:
  std::vector<std::shared_ptr<RubricItem>> items;

  void post_createRubricItem(std::shared_ptr<RubricItem>);
};

#endif
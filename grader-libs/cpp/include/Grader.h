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
  bool has_run = false;
  Stats stats;
  size_t num_tests;

  shared_ptr<RubricItem> create_rubric_item();
  shared_ptr<RubricItem> create_rubric_item(const string&);
  shared_ptr<RubricItem> create_rubric_item(const function<bool()>&);
  void run();
  void run_debug();

  bool failed();
  bool passed();

  std::string get_feedback();

  std::vector<std::string> report(); // will switch to json

private:
  std::vector<shared_ptr<RubricItem>> items;

  void post_create_rubric_item(shared_ptr<RubricItem>);
};

#endif
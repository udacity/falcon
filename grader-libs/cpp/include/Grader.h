#ifndef Grader_H_
#define Grader_H_

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

  void create_test();
  void run();
  void run_debug();

  bool failed();
  bool passed();

  std::string get_feedback();

  std::vector<std::string> report(); // will switch to json

private:
  std::vector<RubricItem> tests;

};

#endif
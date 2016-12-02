#ifndef RubricItem_H_
#define RubricItem_H_

#include <chrono>
#include <ctime>
#include <functional>
#include <string>
#include "Feedback.h"

class RubricItem
{
public:
  RubricItem() = default;
  RubricItem(const std::function<bool()>& _callback) : callback(_callback) {};
  RubricItem(const std::string& _name) : name(_name) {};
  RubricItem(const std::string& _name, const std::function<bool()>& _callback) : name(_name), callback(_callback) {};

  std::string name;
  bool checkpoint = false;

  void set_callback(const std::function<bool()>&);

  void when_correct(const std::string&);
  void when_correct(const std::string&, const std::string&);
  void when_incorrect(const std::string&);
  void when_incorrect(const std::string&, const std::string&);

  void evaluate();
  bool ran();
  bool passed();
  bool failed();
  Feedback* get_feedback();
  double evaluation_time_ms();

private:
  bool has_run{false};
  std::function<bool()> callback;

  Feedback correct_feedback, incorrect_feedback;

  std::chrono::time_point<std::chrono::high_resolution_clock> start, end;
  std::chrono::duration<double, std::ratio<1, 1000000>> evaluation_duration {std::chrono::duration<double, std::ratio<1, 1000000>>::zero()};

  bool has_passed = false;
};

#endif
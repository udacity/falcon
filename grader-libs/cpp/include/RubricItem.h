#ifndef RubricItem_H_
#define RubricItem_H_

#include <chrono>
#include <ctime>
#include <functional>
#include <string>
#include "Feedback.h"

using namespace std;

class RubricItem
{
public:
  RubricItem() = default;
  RubricItem(const function<bool()>& _callback) : callback(_callback) {};
  RubricItem(const string& _name) : name(_name) {};
  RubricItem(const string& _name, const function<bool()>& _callback) : name(_name), callback(_callback) {};

  string name;
  bool checkpoint = false;

  void set_callback(const function<bool()>&);

  void when_correct(const string&);
  void when_correct(const string&, const string&);
  void when_incorrect(const string&);
  void when_incorrect(const string&, const string&);

  void evaluate();
  bool ran();
  bool passed();
  bool failed();
  Feedback* get_feedback();
  double evaluation_time_ms();

private:
  bool has_run{false};
  function<bool()> callback;

  Feedback correct_feedback, incorrect_feedback;

  chrono::time_point<chrono::high_resolution_clock> start, end;
  chrono::duration<double, ratio<1, 1000000>> evaluation_duration {chrono::duration<double, ratio<1, 1000000>>::zero()};

  bool has_passed = false;
};

#endif
#include <functional>
#include <iostream>
#include "Feedback.h"
#include "RubricItem.h"

using namespace std;

void RubricItem::set_callback(const function<bool()>& _callback)
{
  callback = _callback;
}

void RubricItem::when_correct(const string& message)
{
  correct_feedback = Feedback(message);
}

void RubricItem::when_correct(const string& message, const string& tag)
{
  correct_feedback = Feedback(message, tag);
}

void RubricItem::when_incorrect(const string& message)
{
  incorrect_feedback = Feedback(message);
}

void RubricItem::when_incorrect(const string& message, const string& tag)
{
  incorrect_feedback = Feedback(message, tag);
}

void RubricItem::evaluate()
{
  start = std::chrono::high_resolution_clock::now();
  callback() == true ? has_passed = true : has_passed = false;
  end = std::chrono::high_resolution_clock::now();
  evaluation_duration = end - start;
  has_run = true;
}

bool RubricItem::ran()
{
  return has_run;
}

bool RubricItem::passed()
{
  return has_passed;
}

bool RubricItem::failed()
{
  return !has_passed;
}

Feedback* RubricItem::get_feedback()
{
  if (has_passed == true)
    return &correct_feedback;
  else
    return &incorrect_feedback;
}

double RubricItem::evaluation_time_ms()
{
  return evaluation_duration.count();
}
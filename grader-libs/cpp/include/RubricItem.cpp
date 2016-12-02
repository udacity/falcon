#include <functional>
#include <iostream>
#include "Feedback.h"
#include "RubricItem.h"

using namespace std;

void RubricItem::setCallback(const function<bool()>& _callback)
{
  callback = _callback;
}

void RubricItem::whenCorrect(const string& message)
{
  correct_feedback = Feedback(message);
}

void RubricItem::whenCorrect(const string& message, const string& tag)
{
  correct_feedback = Feedback(message, tag);
}

void RubricItem::whenIncorrect(const string& message)
{
  incorrect_feedback = Feedback(message);
}

void RubricItem::whenIncorrect(const string& message, const string& tag)
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

Feedback* RubricItem::getFeedback()
{
  if (has_passed == true)
    return &correct_feedback;
  else
    return &incorrect_feedback;
}

double RubricItem::evaluationTimeMs()
{
  return evaluation_duration.count();
}
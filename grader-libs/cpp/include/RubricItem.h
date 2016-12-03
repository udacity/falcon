#ifndef RubricItem_H_
#define RubricItem_H_

#include <chrono>
#include <ctime>
#include <functional>
#include <memory>
#include <string>
#include "Feedback.h"

class RubricItem
{
public:
  /**
  * The default constructor.
  */
  RubricItem() = default;
  /**
  * A constructor that sets the callback.
  */
  RubricItem(const std::function<bool()>& _callback) : callback(_callback) {};
  /**
  * A constructor that sets the name.
  */
  RubricItem(const std::string& _name) : name(_name) {};
  /**
  * A constructor that sets the name and callback.
  */
  RubricItem(const std::string& _name, const std::function<bool()>& _callback) : name(_name), callback(_callback) {};

  std::string name; /**< Optional identifier of the RubricItem. */
  bool checkpoint = false; /**< If checkpoint, no RubricItems after this one will evaluate if this one fails. */
  bool optional = false; /**< If optional, the RubricItem does not count towards the Grader pass/fail state. */

  /**
  * Set the work to be done when this RubricItem is evaluated. Likely a lambda function.
  */
  void setCallback(const std::function<bool()>&);

  /**
  * Set the message to give to students if this RubricItem passes. Optional.
  */
  void whenCorrect(const std::string& message);
  /**
  * Set the message and tag to give to students if this RubricItem passes. Optional.
  */
  void whenCorrect(const std::string& message, const std::string& tag);
  /**
  * Set the message to give to students if this RubricItem fails. Optional.
  */
  void whenIncorrect(const std::string& message);
  /**
  * Set the message and tag to give to students if this RubricItem fails. Optional.
  */
  void whenIncorrect(const std::string& message, const std::string& tag);

  /**
  * Run the callback to determine if this RubricItem passed or failed.
  */
  void evaluate();
  /**
  * Whether or not this RubricItem has run.
  */
  bool ran();
  /**
  * Whether or not this RubricItem passed. Will be false until it actually runs.
  */
  bool passed();
  /**
  * Whether or not this RubricItem failed.
  */
  bool failed();
  /**
  * Only useful after the RubricItem is evaluated. Gets the corresponding Feedback to its pass/fail state.
  */
  std::shared_ptr<Feedback> getFeedback();
  /**
  * High precision time in milliseconds representing how long the callback itself took to run.
  */
  double evaluationTimeMs();

private:
  bool has_run{false}; /**< Whether or not the RubricItem has been evaluated. */
  std::function<bool()> callback; /**< The callback to determine pass/fail. */

  Feedback correct_feedback, incorrect_feedback; /**< Feedback for passing and failing */

  std::chrono::time_point<std::chrono::high_resolution_clock> start, end; /**< Timestamps for when the callback starts and stops. */
  std::chrono::duration<double, std::ratio<1, 1000000>> evaluation_duration {std::chrono::duration<double, std::ratio<1, 1000000>>::zero()}; /**< Amount of time elapsed while the callback ran. */

  bool has_passed = false; /**< Whether or not the RubricItem has passed. */
};

#endif
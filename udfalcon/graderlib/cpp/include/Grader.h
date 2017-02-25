#ifndef Grader_H_
#define Grader_H_

#include <memory>
#include <string>
#include <vector>
#include "Stats.h"
#include "RubricItem.h"

/**
The main Grader tool. Responsible for creating RubricItems, running them and then outputting results.
*/
class Grader
{
public:
  bool has_evaluated = false; /**< True after it completes evaluating RubricItems */

  Stats stats; /**< Stores and generates info on evaluated RubricItems. public for testing purposes */

  /**
  * Generates a RubricItem.
  */
  std::shared_ptr<RubricItem> createRubricItem();
  /**
  * Generates a RubricItem.
  */
  std::shared_ptr<RubricItem> createRubricItem(const std::string&);
  /**
  * Generates a RubricItem.
  */
  std::shared_ptr<RubricItem> createRubricItem(const std::function<bool()>&);
  /**
  * Evaluates all RubricItems and respects checkpoint and optional flags.
  */
  void run();
  /**
  * Evaluates all RubricItems regardless of flags.
  */
  void run_debug();

  /**
  * Whether or not the Grader as a whole has failed.
  */
  bool failed();
  /**
  * Whether or not the Grader as a whole has passed. Every RubricItem must pass or be optional for this to be true.
  */
  bool passed();

  /**
  * Get a JSON representation of the evaluation results.
  */
  Json::Value resultsJson();
  /**
  * Get a stringified JSON representation of the evaluation results. Good for outputting to another environment.
  */
  std::string results();

private:
  std::vector<std::shared_ptr<RubricItem>> items; /**< Contains all the RubricItems. */

  /**
  * The work that needs to be done after creating a RubricItem.
  */
  void postCreateRubricItem(std::shared_ptr<RubricItem>);
};

#endif

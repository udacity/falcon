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
  /**
  * For adding Stats (likely from different Graders).
  */
  Stats& operator+=(const Stats&);
  /**
  * For adding Stats (likely from different Graders).
  */
  Stats operator+(const Stats&);

  unsigned num_created{0}; /**< Number of RubricItems created. */
  unsigned num_run{0}; /**< Number of RubricItems that were evaluated. */
  unsigned num_passed{0}; /**< Number of RubricItems that passed (and were not optional). */
  unsigned num_failed{0}; /**< Number of RubricItems that failed (and were not optional). */
  unsigned num_optional{0}; /**< Number of RubricItems that were optional. */

  std::vector<std::shared_ptr<RubricItem>> items; /**< A collection of all the RubricItems that were evaluated. Public for overloading + and +=. */

  /**
  * Whether or not all of the non-optional RubricItems passed.
  */
  bool passed();
  /**
  * Whether or not at least one of the non-optional RubricItems failed.
  */
  bool failed();

  /**
  * Record pass/fail/optional state and feedback. Also aggregates overall stats.
  * Noop if the RubricItem has not run.
  */
  void record(std::shared_ptr<RubricItem>);
  /**
  * Get a stringified JSON of the overall stats.
  */
  std::string results();
  /**
  * Get a JSON of the overall stats.
  */
  nlohmann::json resultsJson();

private:
  nlohmann::json report; /**< Manipulated to create the output results. */
  bool is_correct = false; /**< Whether or not the pass/fail state is passed. */
  std::vector<std::string> student_feedback; /**< Holds the formatted feedback written for student eyes. */

  /**
  * The time in milliseconds that elapsed for all callbacks.
  */
  double getTotalEvalTime();

  /**
  * Aggregate stats on one (evaluted) RubricItem for output.
  */
  nlohmann::json buildRubricItemReport(std::shared_ptr<RubricItem>);
  /**
  * Aggregate stats on all (evaluated) RubricItems for output.
  */
  nlohmann::json buildRubricItemsReport();
  /**
  * Create a properly formatted JSON for output.
  */
  void buildJsonResults();
  /**
  * Aggregate feedback from evaluted RubricItems for student eyes.
  */
  void appendFeedback(std::shared_ptr<RubricItem>);
};

#endif
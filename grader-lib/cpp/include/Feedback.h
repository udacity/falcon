#ifndef Feedback_H_
#define Feedback_H_

#include <string>

class Feedback
{
public:
  std::string msg{""}; /**< Message for students. */
  std::string tag{""}; /**< Optional tag describing the message. */

  /**
  * Default constructor.
  */
  Feedback() = default;
  /**
  * Construct with a message.
  */
  Feedback(const std::string& _msg) : msg(_msg) {};
  /**
  * Construct with a message and tag.
  */
  Feedback(const std::string& _msg, const std::string& _tag) : msg(_msg), tag(_tag) {};

  /**
  * Format the feedback as "TAG: Message for students." (TAG only shows up if it exists.)
  */
  std::string format();
};

#endif
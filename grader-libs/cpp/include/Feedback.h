#ifndef Feedback_H_
#define Feedback_H_

#include <string>

class Feedback
{
public:
  std::string msg{""};
  std::string tag{""};

  Feedback() = default;
  Feedback(const std::string& _msg) : msg(_msg) {};
  Feedback(const std::string& _msg, const std::string& _tag) : msg(_msg), tag(_tag) {};

  std::string format();
};

#endif
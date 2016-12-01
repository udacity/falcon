#ifndef Feedback_H_
#define Feedback_H_

#include <string>

using namespace std;

class Feedback
{
public:
  string msg{""};
  string tag{""};

  Feedback() = default;
  Feedback(const string& _msg) : msg(_msg) {};
  Feedback(const string& _msg, const string& _tag) : msg(_msg), tag(_tag) {};

  string format();
};

#endif
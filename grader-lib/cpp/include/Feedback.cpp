#include <string>
#include "Feedback.h"

std::string uppercase(std::string& str)
{
  std::string container;
  for (auto& c : str)
    container += toupper(c);
  return container;
}

std::string Feedback::format()
{
  if (!tag.empty())
    return uppercase(tag) + ": " + msg;
  else
    return msg;
}

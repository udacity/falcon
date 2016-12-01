#include <iostream>
#include <string>
#include "gtest/gtest.h"
#include "Feedback.h"

using namespace ::testing;

class AFeedback: public Test {
public:
 Feedback feedback;
};

TEST_F(AFeedback, ShouldDefaultToEmptyStrings)
{
  ASSERT_EQ(feedback.msg, "");
  ASSERT_EQ(feedback.tag, "");
}

TEST_F(AFeedback, CanFormatFeedbackWithoutATag)
{
  std::string msg("a sample message");
  feedback.msg = msg;
  ASSERT_EQ(feedback.format(), msg);
}

TEST_F(AFeedback, CanFormatFeedbackWithATag)
{
  std::string msg("a sample message");
  std::string tag("sometag");
  feedback.msg = msg;
  feedback.tag = tag;
  ASSERT_EQ(feedback.format(), "SOMETAG: a sample message");
}
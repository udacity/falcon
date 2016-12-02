#include <iostream>
#include "gtest/gtest.h"
#include "Grader.h"

using namespace ::testing;

class AGrader: public Test {
public:
 Grader grader;
};

/* useful methods */



/* actual tests */

TEST_F(AGrader, CanKeepTrackOfTheNumberOfTests) {
  grader.create_rubric_item();
  ASSERT_EQ(grader.num_tests, 1u);
}

TEST_F(AGrader, KnowsWhenItRanAtLeastOneTest) {
  grader.run();
  ASSERT_TRUE(grader.has_run);
}

// TEST_F(AGrader, CanRunMoreThanOneTest) {
//   // add two tests
//   Grader.run();
//   ASSERT_
// }
#include "Grader.h"
#include "RubricItem.h"

void Grader::run()
{
  // TODO: placeholder

  has_run = true;
}

void Grader::create_test()
{
  RubricItem test;
  // TODO: actually make the test
  tests.push_back(test);

  num_tests = tests.size();
}
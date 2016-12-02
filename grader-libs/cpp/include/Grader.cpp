#include <memory>
#include "Grader.h"
#include "RubricItem.h"

using namespace std;

void Grader::run()
{
  // TODO: placeholder
  // some kind of loop through items

  has_run = true;
}

shared_ptr<RubricItem> Grader::create_rubric_item()
{
  shared_ptr<RubricItem> item = make_shared<RubricItem>();
  post_create_rubric_item(item);
  return item;
}

shared_ptr<RubricItem> Grader::create_rubric_item(const string& name)
{
  shared_ptr<RubricItem> item = make_shared<RubricItem>(name);
  post_create_rubric_item(item);
  return item;
}

shared_ptr<RubricItem> Grader::create_rubric_item(const function<bool()>& _callback)
{
  shared_ptr<RubricItem> item = make_shared<RubricItem>(_callback);
  post_create_rubric_item(item);
  return item;
}

void Grader::post_create_rubric_item(shared_ptr<RubricItem> item)
{
  items.push_back(item);
  num_tests = items.size();
}
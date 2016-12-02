#include <memory>
#include "json.hpp"
#include "Grader.h"
#include "RubricItem.h"

using namespace std;
using namespace nlohmann;

void Grader::run()
{
  for (auto i: items)
  {
    i->evaluate();
    stats.record(i);

    if (i->failed() && !i->optional)
      break;
  }
  has_evaluated = true;
}

void Grader::run_debug()
{
  for (auto i: items)
  {
    i->evaluate();
    stats.record(i);
  }
}

shared_ptr<RubricItem> Grader::createRubricItem()
{
  shared_ptr<RubricItem> item = make_shared<RubricItem>();
  post_createRubricItem(item);
  return item;
}

shared_ptr<RubricItem> Grader::createRubricItem(const string& name)
{
  shared_ptr<RubricItem> item = make_shared<RubricItem>(name);
  post_createRubricItem(item);
  return item;
}

shared_ptr<RubricItem> Grader::createRubricItem(const function<bool()>& _callback)
{
  shared_ptr<RubricItem> item = make_shared<RubricItem>(_callback);
  post_createRubricItem(item);
  return item;
}

void Grader::post_createRubricItem(shared_ptr<RubricItem> item)
{
  items.push_back(item);
  stats.num_created = static_cast<unsigned>(items.size());
}

bool Grader::passed()
{
  return stats.passed();
}

bool Grader::failed()
{
  return stats.failed();
}

json Grader::resultsJson()
{
  return stats.resultsJson();
}

string Grader::results()
{
  return stats.results();
}
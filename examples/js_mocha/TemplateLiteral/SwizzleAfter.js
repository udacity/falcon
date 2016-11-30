// tests to verify the student's code
;(function() {
  // require assertion library, javascript parser, querying library, and file system
  var chai = require('chai');
  var esprima = require('esprima');
  var esquery = require('esquery');
  var fs = require('fs');

  var assert = chai.assert;
  var tree = '';
  var content = '';

  // get students' file
  content = fs.readFileSync(__dirname + '/StudentMain.js', 'utf8');
  // generate abstract systax tree (AST)
  tree = esprima.parse(content);

  // define selector
  var selector = esquery.parse('[id.name="greeting"]');
  // query AST with selector
  var matches = esquery.match(tree, selector);

  // tests
  describe('Your code', function() {
    // check if myName exists
    it('should have a variable `myName`', function() {
      assert.isDefined(myName, "The variable `myName` doesn't exist");
    });

    // check if greeting exists
    it('should have a variable `greeting`', function() {
      assert.isDefined(greeting, "The variable `greeting` doesn't exist");
    });

    // check if greeting has been changed to a template literal
    it('should have a template literal `greeting`', function() {
      assert.deepEqual('TemplateLiteral', matches[0].init.type, "The `greeting` string should be changed to a template literal");
    });
  });

  if(matches[0].init.type === 'TemplateLiteral') {
    describe('Your template literal', function() {
      // check if greeting template literal matches original greeting string
      it('should match the original `greeting` string', function() {
        assert.deepEqual('Hello, my name is myName', matches[0].init.quasis[0].value.raw + matches[0].init.expressions[0].name, "The value of the `greeting` template literal doesn't match the original `greeting` string");
      });
    });
  }

}());
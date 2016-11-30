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
  var selector = esquery.parse('');
  // query AST with selector
  var matches = esquery.match(tree, selector);

  // tests
  describe('Your code', function() {
    it('should have a variable `x` that is larger than 5', function() {
      assert.isAbove(x, 5, "Hmmm, `x` doesn't seem to be large enough");
    });

    it('should have a variable `foo`', function() {
      assert.isDefined(foo, "Hmmm, `foo` doesn't seem to exist");
    });

     it('should have a variable `beverages`', function() {
      assert.isDefined(beverages, "Hmmm, `beverages` doesn't seem to exist");
    });
  });

  describe('The `beverage` object', function(){
    it('should have a property `teas`', function() {
      assert.property(beverages, 'teas', "Hmmm, `beverages` is supposed to have the `teas` property");
    });
  });

}());
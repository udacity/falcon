// tests to verify the student's code
;(function() {
  var chai = require('chai');
  var assert = chai.assert;

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

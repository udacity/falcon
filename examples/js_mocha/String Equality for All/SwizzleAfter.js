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
    var selector = esquery.parse('[id.name="answer"]');
    // query AST with selector
    var matches = esquery.match(tree, selector);

    // tests
    describe('Your code', function() {
        // check if answer exists
        it('should have a variable `answer`', function() {
            assert.isDefined(answer, "The variable `answer` doesn't exist");
        });
    });

    if(matches[0] != null) {
        describe('Your expression', function() {
            // check if left side of expression matches original
            it('should have "ALL Strings are CrEaTeD equal" on the left side', function() {
                assert.equal("ALL Strings are CrEaTeD equal", matches[0].init.left.value, "The left side of the expression has changed. Try resetting the quiz.");
            });
            // check if still using == operator
            it('should use `==` comparison', function() {
                assert.equal("==", matches[0].init.operator, "The `==` comparison is missing. Try resetting the quiz.");
            });
            // check if expression evaluates to true
            it('should evaluate to true', function() {
                assert.equal(answer, true, "The expression doesn't evaulate to `true`");
            });
        });
        describe('The right side of your expression', function() {
            // check if right side of expression matches left side
            it('should match the left side', function() {
                assert.equal("ALL Strings are CrEaTeD equal", matches[0].init.right.value, "The right side of the expression doesn't match the left side");
            });
        });
    }

}());
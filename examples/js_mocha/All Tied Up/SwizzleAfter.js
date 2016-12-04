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
    var selector = esquery.parse('[id.name="joke"]');
    // query AST with selector
    var matches = esquery.match(tree, selector);

    // tests
    describe('Your code', function() {
        // check if joke exists
        it('should have a variable `joke`', function() {
            assert.isDefined(joke, "The variable `joke` doesn't exist");
        });
        // check if joke is one string
        it('should use only one string', function() {
            assert.equal('Literal', matches[0].init.type, "Your joke should only use one, single string");
        });
    });

    if(matches[0].init.type === 'Literal') {
        describe('Your joke', function() {
            // check if joke matches correct format
            it('matches the correct format', function() {
                assert.match(matches[0].init.raw, /^.*\\n.*/, 'Your joke doesn\'t match the correct format');
            });
        });
    }

}());
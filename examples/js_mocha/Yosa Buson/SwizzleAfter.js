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
    var selector = esquery.parse('[id.name="haiku"]');
    // query AST with selector
    var matches = esquery.match(tree, selector);

    // tests
    describe('Your code', function() {
        // check if haiku exists
        it('should have a variable `haiku`', function() {
            assert.isDefined(haiku, "The variable `haiku` doesn't exist");
        });
    });

    if(matches[0] != null) {
        describe('Your code', function() {
            // check if haiku uses string concatenation
            it('should use string concatenation', function() {
                assert.equal('BinaryExpression', matches[0].init.type, "Your haiku should use string concatenation");
            });
        });
        if(matches[0].init.type === 'BinaryExpression') {
            // define new selector
            var selector2 = esquery.parse('[raw]');
            // query AST with selector
            var pieces = esquery.match(tree, selector2);
            // init poem
            var poem = "";
            for(let piece of pieces) {
                // build poem string from binary expression(s)
                poem += piece.value;
            }
            describe('Your poem', function() {
                // check if poem matches haiku poem
                it('matches the famous haiku poem', function() {
                    assert.equal(poem, 'Blowing from the west\nFallen leaves gather\nIn the east.', 'Your `poem` doesn\'t match the famous haiku poem');
                });
            });
        }
    }

}());
// tests to verify the student's code
if (typeof myString !== 'undefined') {
    pass('myString exists');

    if (typeof myString === 'string') {
        pass('myString is string type');
        var firstChar = myString.charCodeAt(0);
        if(firstChar <= 90 && firstChar >= 65) {
            pass('first character in myString is capitalized');
        } else {
            fail('first character in myString is not capitalized', 'feedback #2');
        }
    } else {
        fail('myString is not string type', 'wrong type is used');
        fail('first character in myString is not capitalized', 'feedback #2');
    }

} else {
    fail('myString DNE', 'did you declare myString?');
}

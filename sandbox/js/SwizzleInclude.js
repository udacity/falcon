function pass(criteria, feedback) {
    console.log('<PASS::>' + criteria);
    if (feedback !== undefined) {
        console.log('<FEEDBACK::>' + feedback);
    }
}

function fail(criteria, feedback) {
    console.log('<FAIL::>' + criteria);
    if (feedback !== undefined) {
        console.log('<FEEDBACK::>' + feedback);
    }
}

/*:
 # SwizzleAfter.swift

 Code that is hidden to students but is swizzled together with their code when
 they click "Submit".

 Use this section to insert any code that should come after student code like
 executing run-time checks that determine correctness.

 When performing run-time checks use the `pass` and `fail` functions provided
 by SwizzleInclude.swift.

 - Important: When necessary, use obfuscated names that will not conflict
 with student code.
 */
if larger(x: 0, y: 0) == 0 {
    pass(criteria: "larger(x: 0, y: 0) returns 0")
} else {
    fail(criteria: "larger(x: 0, y: 0) returns \(larger(x: 0, y: 0)), but should return 0")
}

if larger(x: -100, y: 100) == 100 {
    pass(criteria: "larger(x: -100, y: 100) returns 100")
} else {
    fail(criteria: "larger(x: -100, y: 100) returns \(larger(x: 0, y: 0)), but should return 100")
}

if larger(x: 10, y: 20) == 20 {
    pass(criteria: "larger(x: 10, y: 20) returns 20")
} else {
    fail(criteria: "larger(x: 10, y: 20) returns \(larger(x: 10, y: 20)), but should return 20")
}

if larger(x: 5, y: 3) == 5 {
    pass(criteria: "larger(x: 5, y: 3) returns 5")
} else {
    fail(criteria: "larger(x: 5, y: 3) returns \(larger(x: 5, y: 3)), but should return 5")
}

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
if type(of: x) is String.Type {
    pass(criteria: "x is a String")
    let y = x as! String
    if y == "Swift is Awesome" {
        pass(criteria: "x contains the value \"Swift is Awesome\"")
    } else {
        fail(criteria: "x doesn't contain the value \"Swift is Awesome\"")
    }
} else {
    fail(criteria: "x is a \(type(of: x)), but it should be a String")
    fail(criteria: "x doesn't contain the value \"Swift is Awesome\"")
}

/// Formatting prefixes used for feedback.
enum FalconPrefix: String {
    case
    pass = "<PASS::>",
    fail = "<FAIL::>",
    feedback = "<FEEDBACK::>"
}

/// Use to indicate student code passed a specific criteria.
///
/// - parameter criteria: A string describing the checked critieria.
public func pass(criteria: String, feedback: String? = nil) {
    print("\(FalconPrefix.pass.rawValue)\(criteria)")
    if let feedback = feedback {
        print("\(FalconPrefix.feedback.rawValue)\(feedback)")
    }
}

/// Use to indicate student code failed a specific criteria.
///
/// - parameter criteria: A string describing the checked critieria.
public func fail(criteria: String, feedback: String? = nil) {
    print("\(FalconPrefix.fail.rawValue)\(criteria)")
    if let feedback = feedback {
        print("\(FalconPrefix.feedback.rawValue)\(feedback)")
    }
}

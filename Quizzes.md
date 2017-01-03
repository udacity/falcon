## Programming Quizzes

Programming quizzes (PQs) are assessments which test a student’s understanding of a programming concept by asking them to write code which can be evaluated for correctness. Here’s an example of a PQ displayed in the Udacity classroom with labels for the main sections:

<img src="https://github.com/jarrodparkes/images/blob/master/falcon-classroom.png?raw=true" width="600" />

1. Coding Area - displays code that a student can read and edit
2. Test Feedback Area - displays output when a student tests/submits code
3. Test Code Button - runs code without evaluation for correctness
4. Submit Code Button - submits code to be evaluated for correctness
5. Reset Quiz Button - resets quiz to initial state

Not shown in the example above is the Main Feedback dialog:

<img src="https://github.com/jarrodparkes/images/blob/master/falcon-feedback.png?raw=true" width="600" />

When a student submits the code (by pressing the "Submit Code" button), this dialog informs the student whether they correctly answered the quiz as well as any additional feedback that may be helpful for addressing incorrect answers or providing encouragement.

## Design Principles

### Instructional Prompts

All PQs should include an instructional prompt that tells the student how to begin the quiz. The prompt may exist about the quiz (for example, in a Video or Text Atom) or it may be embedded in the Coding Area in the files using comments.

### Descriptive Feedback

When a student incorrectly answers a PQ, it is paramount that the feedback provided gives them information that helps drive them towards the correct answer. If the feedback is simply “Failed”, then the student has no way to diagnose the problem with their code, and they may become frustrated and/or skip the quiz.

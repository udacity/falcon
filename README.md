<img src="https://github.com/jarrodparkes/images/blob/master/falcon-icon.png?raw=true" alt="Falcon icon" align="left" height="64">

# Falcon

Falcon is a command-line program for running programming quizzes and retrieving feedback using [Udacity's remote execution stack (REX)](https://github.com/udacity/udacity-clyde). The basic idea is that Falcon runs on a virtual machine and has access to the student code and our grading code. It allows you to easily define and then execute the sequence of steps necessary for compiling, running and analyzing the output of student code in any language or runtime environment. It also provides output in a way that's easy for the Udacity classroom to digest.

Within Falcon, there are multiple grading libraries designed as unit test tools for teaching - rather than focus on the PASS/FAIL state of tests, they focus on providing feedback. See `udfalcon/graderlib` for individual grading libraries. Currently only JavaScript and C++ have grader libraries, but the architecture is small and straightforward. Let me know if you want to port it to another language!

## Udacity's Philosophy on Quiz Behavior

We evaluate quizzes under two circumstances: when students want to test (click 'Test Run' in the classroom) and when students want to submit (click 'Submit').

While every quiz is different, we generally follow the paradigm that we run student code as is when students test, and we run student code against our tests and provide detailed feedback when students submit.

If you're interested in learning more about how to provide usefl, I recommend reading [this](https://github.com/udacity/js-grader##grader-philosophy) and checking out the **Grader Libraries** section below.

## Why Falcon is Useful

"Running code is always nice," you say, "but what's the point of Falcon?" Great question!

Falcon itself isn't fancy. The whole thing is basically a big wrapper around Python's `subprocess` module. What makes it useful is that it (a) handles `subprocess`'s somewhat gnarly API so you don't have to, and (b) neatly organizes stdout and stderr from each step to make it easy to figure out what happened.

If you keep reading, you'll learn that Falcon works by executing a series of commands that you determine. Falcon captures stdout and stderr from each command along the way so that you can easily access it. Let's run through a few scenarios.

## How Falcon Generally Works

1. Create template files for students.
2. Create your grading files.
3. Create a Falcon configuration file (default is 'falconf.yaml`.)
4. Fly it and see the output!

### Examples

#### Running an Interpreted Language

Let's say you want to test a student's JavaScript. The student writes their code in one file, 'student\_main.js', while your unit tests are written in another file, 'udacity\_tests.js. Let's imagine that you want students to write a function, `double(x)` that returns a value.

```javascript
// student_main.js

function double(x) {
  // student code goes here
}

// here's something to help students test
console.log(double(10));

module.exports = double;
```

```javascript
// udacity_tests.js

// assuming Node runtime
const assert = require('assert');
const double = require('./student_main');

try {
  assert.equal(double(5), 10);
  console.log('Great job!');
} catch (e) {
  const stdout = double(5);
  console.log(`Not quite. We got ${stdout} when we tried to double 5.`);
}
```

```yaml
# falconf.yaml

test:
  main: node student_main.js
submit:
  main: node udacity_tests.js
```

```python
# test code

import udfalcon
udfalcon.fly({'mode': 'test', 'output': 'clean'})
```

```python
# submit code

import udfalcon
udfalcon.fly({'mode': 'submit', 'output': 'json'})
```

Here, you just specify different behavior for testing and submitting. Upon clicking 'Test Run,' students will only see the output of `double(10)`. Falcon can take care of making sure the output is clean and easy to read.

When students click 'Submit,' we run our (oversimplified) test against student code and pass the results back to the classroom as JSON to be ingested by grading code.

This example works great if all of the student's code is neatly encapsulated into functions or classes, but some procedural code lacks structure. Students in beginner level courses often write code without any encapsulation. If you want to create some kind of structure or book-end their code with something, you can take advantage of one of Falcon's features: concatting files.

---

```javascript
// student_main.js

const x = 1;
const y = 2;
```

```javascript
// udacity_tests.js

try {
  assert.equal(x, 1);
  assert.equal(y, 2);
  console.log('You can set variables!');
} catch (e) {
  console.log(`Not quite. It looks like your variables are x=${x}, y=${y}.`)
}
```

```yaml
# falconf.yaml

test:
  main: node student_main.js
submit:
  preprocess: falcon.concat student_main.js udacity_tests.js concatted_file.js
  main: node concatted_file.js
```

When students test, they'll just see their code run (which would output nothing at the moment as there aren't any print statements). When students submit, we'll run the test specified in udacity\_tests.js'.

Here, I used `falcon.concat` to jam together the contents of N files (in this case, 2 files) into an output file in the preprocess step. This Frankensteined file, 'concatted\_file.js', consists of the student code and our test. Assuming the Frankensteined concatted\_file.js' is still valid JavaScript (and c'mon, what *isn't* valid JavaScript?), then the main step should have no problem running it and returning the output in a nice JSON for the classroom.

Let's have a bit more fun. What if you're worried that students will include a number of erroneous print statements in their work? In the previous example, any calls to `console.log` in 'student\_main.js' will be printed alongside any of our feedback from 'udacity_tests.js'. What if you want to keep the output clean?

You need to be able to separate *your* stdout from the student's. I'll show you an example with Python, however it's possible to do the same with any language that can write a file to disk.

---

```python
# udacity_tests.py

from udfalcon import util
import student_code

def test_student_code(student_code):
  # insert tests against student code here...

friendly_feedback_msg_string = test_student_code(student_code)

util.write_udacity_out(friendly_feedback_msg_string)
```

In this example, I'm taking advantage of a utility function, `write_udacity_out()`, meant to store output written for students. Using `write_udacity_out()` to provide feedback is totally optional, however if you do use it, students will *only* see the feedback that's passed to this function. Their own stdout and stderr will be hidden by default.

`write_udacity_out` works by writing a temp file, '~/.ud\_falcon\_temp', which gets read and subsequently deleted by Falcon during the process of generating output. You don't need to worry about deleting it, you just need to create it. As such, this technique works with any language and runtime that can write files to disk!

Here's another situation. What if you want to read stdout from a previous step? For instance, what if you want to read stdout after executing student code by itself?

---

```yaml
submit:
  main: python student_code.py
  postprocess: python udacity_tests.py
```

```python
# submit_main_out.txt

with open('.falcontmp/submit_main_out.txt', 'r') as f:
  student_output = f.read()
  test_student_output(student_output)
```

Every Falcon flight creates a set of temporary files that get stored in .falcontmp within the current directory. Some of those files include stdout and stderr from each step. These files follow the naming scheme: `{mode}_{step}_out.txt`, where `{mode}` is one of 'test' and 'submit', and `{step}` is one of the steps listed in **Execution Steps**.

If you run a postprocess step, Falcon will pick up the output from postprocess instead of main. As such, students will only see the feedback that you provide to them from postprocess.

Speaking of feedback, let's take a look at your built-in options for generating more detailed feedback.

---

// grader libs

// something about grabbing file output

// something about temp out and it's priority for the output

#### Running a Compiled Language

// something about compiling c++

## Falcon Dependencies

Falcon requires the following dependencies for installation and execution:

- `python3.4+` (installation depends on your OS)
- `pip3` (installation depends on your OS)
- `pyyaml` package (`pip3 install pyyaml`)

## Installing and Running Falcon Locally

Testing on REX can be a pain, but you can mimic it by running Falcon locally. To do so, install Falcon with:

```sh
pip3 install https://github.com/udacity/falcon/blob/master/dist/falcon-0.2.0-py32-none-any.whl?raw=true
````

You can now import Falcon or run it as a module from the command line.

Note that the applications and packages installed on a REX unsafer will likely differ from your machine. See [udacity-clyde](https://github.com/udacity/udacity-clyde/docs/vagrant-unsafer.md) for information about spinning up an unsafer Vagrant box.

### Importing within a Script

```python
import udfalcon
udfalcon.fly({'debug': True})
```

### As a Module on the Command Line

```sh
python3 -m udfalcon
```

## Using Falcon

### Execution Steps

To run (fly!) Falcon, you must understand how it is executes — it uses a series of execution steps:

|Order|Execution Step       |Typical Uses                                         |
|-----|---------------------|-----------------------------------------------------|
|1    |`preprocess`         |setup and configure the executing environment        |
|2    |`compile`            |compile student code or our code                     |
|3    |`main`               |run student's code (required)                        |
|4    |`postprocess`        |prepare output to be sent back to classroom          |
|5    |`tear_down`          |clean up executing environment; remove temp files    |

Technically, each step executes the exact same way. However, they are not interchangable! Each step is treated differently when generating the output after a flight. You can read more about each step in **Explanation of Each Step**.

Each step represents a point during execution where you can specify your own custom commands. The steps and commands must be defined in a `falconf.yaml` file (see the eponymous section below).

### Specifying Commands

A command can be one of the following:

* A shell command, eg. `python app.py`.
* An executable file `foo.sh`.
  - Note: this file must _already_ be executable. Falcon will _not_ try to change permissions for any file.
* A Falcon action. See **Falcon Actions** below.
* Nothing.
  - Falcon will look for a local file with the basename `{mode}_{step}` to execute. Once again, this file would need to be executable.

### falconf.yaml

Falcon + Config = falconf.

Here's a simple `falconf.yaml` for a Swift programming quiz:

```yaml
test:
  main: swift StudentMain.swift
submit:
  preprocess: falcon.concat SwizzleInclude.swift SwizzleBefore.swift StudentMain.swift SwizzleAfter.swift SwizzledMain.swift
  main: swift SwizzledMain.swift
  tear_down: rm SwizzledMain.swift
```

Here's an expanded `falconf.yaml` template:

```yaml
test:
  env_vars:
    VAR: value
    VAR2: value2
  grader_libs: [lib1, lib2]
  preprocess: command
  compile: command
  main: command
  postprocess: command
  tear_down: command
submit:
  (same structure as test)
```

Notice the file is split into `test` and `submit` sections. These sections correspond to Falcon's `test` and `submit` modes, and they control which steps/commands are run when Falcon is invoked. The only required step for either section is `main`.

> **Note:** Any steps not listed for a section will be skipped. Steps can also be listed in any order, but they will _always_ executed in the order listed under Execution Steps.

The `test` and `submit` modes should emulate what happens when a student selects "Test Code" or "Submit Code" in the classroom. Specifically, `test` should run a student's code without evaluating it for correctness, and `submit` should evaluate the student's code by testing it for correctness. Note that there is no check within Falcon for this behavior - it's up to you to keep to it.

### Explanation of Each Step

1. `env_vars`: A dict with any environment variables you want to set during the flight.

2. `grader_libs`: A list of directories within `udfalcon/graderlib` that you want to temporarily symlink into the cwd. This allows you to use any of the grader libraries without worrying about actually copying, moving or maintaining those files. They also disappear when the flight finishes, so your quiz directory stays clean (see **Grader Libraries** and **Testing a Grader Library** more info).

3. `preprocess`: Any preparation that needs to happen before compiling.

4. `compile`: Compile code.

5. `main`*: Required! Run student code here. See **The Results JSON** below.

6. `postprocess`: Examine the output of student code here. See **The Results JSON** below.

7. `tear_down`: Any file or resource cleanup that needs to happen.

### Falcon Commands

Currently, the only command supported is `concat`.

#### Concat

Concatenate the contents of 2+ files into an amalgamated output file.

Usage: `falcon.concat file1 file2 fileN outputFile`

The files will be concatenated in the order specified.

### Grader Libraries

There are currently two grader libraries.

#### JS Grader

See the [documentation here](https://github.com/udacity/js-grader).

Usage:

```yaml
# in falconf.yaml

grader_libs: [js]
```

```javascript
// in your grading code
// assuming you're running Node

const Grader = require('./grader');

const grader = new Grader();
```

#### C++ Grader

See the [documentation here](https://github.com/udacity/falcon/tree/master/udfalcon/graderlib/cpp)

### When to Test

either in main or post process.

## Falcon Output

As Falcon executes, it produces output for each execution step (as a JSON-like string) so that it can be passed back to the classroom for further evaluation. Here's example output generated by Falcon using the Swift example (for submit) from above:

```json
{   "config_file": "",
    "elapsed_time": 0,
    "is_correct": null,
    "mode": "submit",
    "steps": [   {   "command": "swift SwizzledMain.swift",
                     "elapsed_time": 111,
                     "err": "",
                     "name": "main",
                     "out": "hello from swift.\n"
                            "<PASS::>larger(x: 0, y: 0) returns 0\n"
                            "<PASS::>larger(x: -100, y: 100) returns 100\n"
                            "<PASS::>larger(x: 10, y: 20) returns 20\n"
                            "<PASS::>larger(x: 5, y: 3) returns 5",
                     "type": "shell"},
                 {   "command": "falcon.concat SwizzleInclude.swift "
                                "SwizzleBefore.swift StudentMain.swift "
                                "SwizzleAfter.swift SwizzledMain.swift",
                     "elapsed_time": 1,
                     "err": "",
                     "name": "preprocess",
                     "out": "",
                     "type": "falcon"},
                 {   "command": "rm SwizzledMain.swift",
                     "elapsed_time": 5,
                     "err": "",
                     "name": "tear_down",
                     "out": "",
                     "type": "shell"},
                 {   "command": "noop",
                     "elapsed_time": 0,
                     "err": "",
                     "name": "postprocess",
                     "out": "",
                     "type": "noop"},
                 {   "command": "noop",
                     "elapsed_time": 0,
                     "err": "",
                     "name": "compile",
                     "out": "",
                     "type": "noop"}],
    "student_err": "",
    "student_out": "hello from swift.\n"
                   "<PASS::>larger(x: 0, y: 0) returns 0\n"
                   "<PASS::>larger(x: -100, y: 100) returns 100\n"
                   "<PASS::>larger(x: 10, y: 20) returns 20\n"
                   "<PASS::>larger(x: 5, y: 3) returns 5"}
```

> **Note:** Depending on how you design your quizzes, you can determine whether or not a student's submission is correct during Falcon's execution (the `is_correct` key/value pair) or later in the classroom. For example, using the output from above, one could determine correctness later, in the classroom, by analyzing the `<PASS::>` tags in the `student_out` key/value pair.

### The Results JSON

* `config_file`: The name of the configuration file.

* `elapsed_time`: Time to execute all steps in milliseconds.

* `is_correct`: TODO

* `student_out`: one of 3 things...

### Output Options

* `json`

* `formatted`

* `clean`

* `return`

### Reading and Writing Udacity Out

`~/.ud_falcon_temp`

### Running Falcon from the Command Line

Once Falcon is installed on your $PATH, you can run it from anywhere. By default, it looks for a `falconf.yaml` file in the execution directory, but you can provide a custom path as well.

### Using a Grader Library

You'll need to link to the library.

### Testing a Grader Library

There's a feature to symlink a library to cwd without running Falcon.

## Advanced Strategies

### Temporary Files

.falcontmp/

### How to Grab Output from a Previous Step

The output from every execution step is saved to a file with this format: '.falcontmp/{mode}\_{step}\_out.txt'. For example: '.falcontmp/test\_main\_out.txt' is the output of the main step in test mode.

These files are automatically deleted at the end of every run.

## Usage Instructions

`falcon -h`

#### Run Falcon using Test Mode

`falcon -m test`

#### Run Falcon using Submit Mode

`falcon -m submit`

#### Run Falcon and See Debug Output for Each Execution Step

`falcon [-m MODE] -d`

## Developing Falcon or Installing from Source

- setuptools
- pytest

1. `git clone https://github.com/udacity/falcon`
2. `cd falcon`
3. `pip install requirements.txt`
4. `python setup.py install`
5. `python setup.py test`

The final two commands (python `setup.py`) will build and install a command line program called `falcon` onto your machine, make `falcon` available on your $PATH, and test `falcon` to ensure it works. Assuming all goes well, you can begin authoring programming quizzes wherever and whenever your heart desires :sparkling_heart:! Seriously, you don't even need to venture into this repository anymore... unless Falcon changes, and you have to re-build it :wink:.

### Testing with Vagrant

`vagrant login -c` if you have 2FA set.

## Maintainers

@jarrodparkes, @cameronwp

## FAQs

* 'Cameron, what the hell is this?'

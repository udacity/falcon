<img src="https://github.com/jarrodparkes/images/blob/master/falcon-icon.png?raw=true" alt="Falcon icon" align="left" height="64">

# Falcon

Falcon is a command-line program for authoring, testing, and running programming quizzes using [Udacity's remote execution stack (REX)](https://github.com/udacity/udacity-clyde).

> **Note:** If you are unfamiliar with programming quizzes, then please take a moment to read [Programming Quizzes](Quizzes.md) before continuing.

## Dependencies

Minimally, Falcon requires the following dependencies:

- `python3.4+`
- `pip` (should be included with Python)

As you begin using Falcon to write quizzes for certain programming languages and their associated testing harnesses, you may need to install other dependencies.

## Installing Falcon

To install Falcon run the following commands:

- `git clone https://github.com/udacity/falcon`
- `cd falcon`
- `pip install requirements.txt`
- `python setup.py install`
- `python setup.py test`

The final two commands (python `setup.py`) will build and install a command line program called `falcon` onto your machine, make `falcon` available on your $PATH, and test `falcon` to ensure it works. Assuming all goes well, you can begin authoring programming quizzes wherever and whenever your heart desires :sparkling_heart:! Seriously, you don’t even need to venture into this repository anymore... unless Falcon changes, and you have to re-build it :wink:.

## Using Falcon

### Execution Steps

To run/fly with Falcon, you must understand how it is executes — it uses a series of execution steps:

|Order|Execution Step       |Typical Uses                                         |
|-----|---------------------|-----------------------------------------------------|
|1    |`preprocess`         |setup and configure the executing environment        |
|2    |`compile`            |compile (student’s) code                             |
|3    |`static_file_check`  |analyze student files                                |
|4    |`main`               |run student’s code with or without a test harness    |
|5    |`postprocess`        |prepare output to be sent back to classroom          |
|6    |`tear_down`          |clean up executing environment; remove temp files    |

Each step represents a point during execution where you can specify your own custom commands. The steps and commands must be defined in a `falcon.yaml` file. Here’s a simple `falconf.yaml` for a Swift programming quiz:

```yaml
test:
  main: swift StudentMain.swift
submit:
  preprocess: falcon.concat SwizzleInclude.swift SwizzleBefore.swift StudentMain.swift SwizzleAfter.swift SwizzledMain.swift
  main: swift SwizzledMain.swift
  tear_down: rm SwizzledMain.swift
```

Notice the file is split into `test` and `submit` sections. These sections correspond to Falcon’s `test` and `submit` modes, and they control which steps/commands are run when Falcon is invoked (using `falcon -m test` or `falcon -m submit`). The only required step for either section is `main`.

> **Note:** Any steps not listed for a section will be skipped. Steps can also be listed in any order, but they will always executed in same order (`preprocess`, `compile`, ...).

The `test` and `submit` modes should emulate what happens when a student selects “Test Code” or “Submit Code” in the classroom. Specifically, `test` should run a student’s code without evaluating it for correctness, and `submit` should evaluate the student’s code by testing it for correctness.

### falconf.yaml

Here’s an expanded `falconf.yaml` template:

```yaml
test:
  env_vars:
    VAR: value
    VAR2: value2
  grader_libs: [lib1, lib2]
  preprocess: cmd
  compile: cmd
  static_file_check: cmd
  main: cmd
  postprocess: cmd
  tear_down: cmd
submit:
  (same structure as test)
```

It includes new entries — `env_vars` and `grader_libs` — in addition to the execution steps. (@cameronwp can you elaborate here?)

### From Commands to Execution

For each step listed in `falconf.yaml`, its associated command will be interpreted and executed using one of the following rules:

|#|Command Type                       |Example of Command   |File Required for Command    |What’s Executed by Falcon? |
|-|-----------------------------------|---------------------|-----------------------------|---------------------------|
|1|Run a program/script               |file.ext             |file.ext                     |./file.ext                 |
|2|Run a Falcon utility function      |falcon.function      |                             |falcon function            |
|3|Run a shell command                |echo “bar”           |                             |echo “bar                  |
|4|Auto-run a program/script          |                     |stepname.ext                 | ./stepname.ext            |
|5|Omit step                          |                     |                             |                           | |

A few more things to know about the rules:

- All executables must have an extension!
- For a full listing of Falcon utility functions, do [X] (@cameronwp can you elaborate here?)
- For Rule 4, if Falcon detects a filename matching the stepname, then it will attempt to execute that file for the step.

### Falcon Output

As Falcon executes, it produces output for each execution step (as a JSON-like string) so that it can be passed back to the classroom for further evaluation. Here’s example output generated by Falcon using the Swift example (for submit) from above:

```json
{   'config_file': '',
    'elapsed_time': 0,
    'is_correct': None,
    'mode': 'submit',
    'steps': [   {   'command': 'swift SwizzledMain.swift',
                     'elapsed_time': 111,
                     'err': '',
                     'name': 'main',
                     'out': 'hello from swift.\n'
                            '<PASS::>larger(x: 0, y: 0) returns 0\n'
                            '<PASS::>larger(x: -100, y: 100) returns 100\n'
                            '<PASS::>larger(x: 10, y: 20) returns 20\n'
                            '<PASS::>larger(x: 5, y: 3) returns 5',
                     'type': 'shell'},
                 {   'command': 'falcon.concat SwizzleInclude.swift '
                                'SwizzleBefore.swift StudentMain.swift '
                                'SwizzleAfter.swift SwizzledMain.swift',
                     'elapsed_time': 1,
                     'err': '',
                     'name': 'preprocess',
                     'out': '',
                     'type': 'falcon'},
                 {   'command': 'rm SwizzledMain.swift',
                     'elapsed_time': 5,
                     'err': '',
                     'name': 'tear_down',
                     'out': '',
                     'type': 'shell'},
                 {   'command': 'noop',
                     'elapsed_time': 0,
                     'err': '',
                     'name': 'postprocess',
                     'out': '',
                     'type': 'noop'},
                 {   'command': 'noop',
                     'elapsed_time': 0,
                     'err': '',
                     'name': 'compile',
                     'out': '',
                     'type': 'noop'}],
    'student_err': '',
    'student_out': 'hello from swift.\n'
                   '<PASS::>larger(x: 0, y: 0) returns 0\n'
                   '<PASS::>larger(x: -100, y: 100) returns 100\n'
                   '<PASS::>larger(x: 10, y: 20) returns 20\n'
                   '<PASS::>larger(x: 5, y: 3) returns 5'}
```

> **Note:** Depending on how you design your quizzes, you can determine whether or not a student’s submission is correct during Falcon’s execution (the `is_correct` key/value pair) or later in the classroom. For example, using the output from above, one could determine correctness later, in the classroom, by analyzing the `<PASS::>` tags in the `student_out` key/value pair.

### Running Falcon from the Command Line

Once Falcon is installed on your $PATH, you can run it from anywhere. By default, it looks for a `falconf.yaml` file in the execution directory, but you can provide a custom path as well.

#### Usage Instructions

`falcon -h`

#### Run Falcon using Test Mode

`falcon -m test`

#### Run Falcon using Submit Mode

`falcon -m submit`

#### Run Falcon and See Debug Output for Each Execution Step

`falcon [-m MODE] -d`

## Maintainers

@jarrodparkes, @cameronwp

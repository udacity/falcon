<img src="https://github.com/jarrodparkes/images/blob/master/falcon-icon.png?raw=true" alt="Falcon icon" align="left" height="64">

# Falcon

Falcon is a command-line program for running programming quizzes and retrieving feedback using [Udacity's remote execution stack (REX)](https://github.com/udacity/udacity-clyde). The basic idea is that Falcon runs on a virtual machine and has access to the student code and our grading code. It takes care of running the sequence of steps necessary for compiling, running and analyzing the output of student code in any language or runtime environment. It also provides output in a way that's easy for the Udacity classroom to digest.

Within Falcon, there are multiple grading libraries designed as unit test tools for teaching - rather than focus on the PASS/FAIL state of tests, they focus on providing feedback. See `udfalcon/graderlib` for individual grading libraries. Currently only JavaScript and C++ have grader libraries, but the architecture is small and straightforward. Let me know if you want to port it to another language!

## Why Falcon is Useful

"Running code is always nice," you say, "but what's the point of Falcon?" Great question!

Falcon itself isn't fancy. The whole thing is basically a big wrapper around Python's `subprocess` module. What makes it useful is that it (a) handles `subprocess`'s somewhat gnarly API so you don't have to, and (b) neatly organizes stdout and stderr from each step to make it easy to figure out what happened.

If you keep reading, you'll learn that Falcon works by executing a series of commands that you determine. Falcon captures stdout and stderr from each command along the way so that you can easily access it. Let's talk through a few scenarios.

#### Running JavaScript

Let's say you want to test a student's JavaScript. The student writes their code in one file, `student_main.js`, while your unit tests are written in another file, `udacity_tests.js`. Let's imagine that you want students to write a function, `foo()` that returns a value.

```yaml
test:
  main: node student_main.js
submit:
  main: node udacity_tests.js
```

Here, you just specify different behavior for testing and submitting. Node includes interfaces for importing other files, so you could `require('./student_main')` from within `udacity_test.js` and be on your way testing. Call `foo()` however you'd like, check the return value with your tests, and Falcon will return stdout from `udacity_tests.js` to the classroom.

This example works great if all of the student's code is neatly encapsulated into functions or classes, but some procedural code lacks structure. Students in beginner level courses often write code without any encapsulation. If you want to create some kind of structure or book-end their code with something, you can take advantage of one of Falcon's features: concatting files.

```yaml
test:
  main: node student_main.js
submit:
  preprocess: falcon.concat before_student.js student_main.js after_student.js udacity_tests.js concatted_file.js
  main: node concatted_file.js
```

Here, I used `falcon.concat` to jam together N files into an output file in the preprocess step. Assuming the Frankensteined `concatted_file.js` is still valid JavaScript (and c'mon, what *isn't* valid JavaScript?), then the main step should have no problem running it and returning the output in a nice JSON for the classroom.

Let's have a bit more fun. What if you're worried that students will include a number of erroneous print statements in their work? If you're simply parsing stdout to figure out what the student's code did (which is the predicament of REX), then you need to be able to separate *your* stdout from the student's.

For that, you need to get a little creative. In the past, we've printed special tokens and tags to identify our official output from the student's print statements. Regexing stdout is, of course, a massive hack that makes it hard to sleep at night. That's why there are grader libraries.

// something about using a grader lib

// something about compiling c++

// something about temp out

## Falcon Dependencies

Falcon requires the following dependencies for installation and execution:

- `python3.4+` (installation depends on your OS)
- `pip3` (installation depends on your OS)
- `pyyaml` package (`pip3 install pyyaml`)

## Installing and Running Falcon Locally

Testing on REX can be a pain, but you can mimic it by running Falcon locally. To do so, install Falcon with:

```sh
pip3 install [INSERTURL].whl
````

You can now import Falcon or run it as a module from the command line.

Note that the applications and packages installed on REX will likely differ from your machine. I recommend checking your environment against [Clyde](https://github.com/udacity/udacity-clyde) and/or [Ossus](https://github.com/udacity/ossus).

### Importing within a Script

```python
import udfalcon
udfalcon.fly()
```

### As a Module on the Command Line

```sh
python3 -m udfalcon
```

## Using Falcon

### Execution Steps

To run/fly Falcon, you must understand how it is executes — it uses a series of execution steps:

|Order|Execution Step       |Typical Uses                                         |
|-----|---------------------|-----------------------------------------------------|
|1    |`preprocess`         |setup and configure the executing environment        |
|2    |`compile`            |compile (student's) code                             |
|3    |`static_file_check`  |analyze student files (NOT READY!)                   |
|4    |`main`               |run student's code (required)                        |
|5    |`postprocess`        |prepare output to be sent back to classroom          |
|6    |`tear_down`          |clean up executing environment; remove temp files    |

Each step represents a point during execution where you can specify your own custom commands. The steps and commands must be defined in a `falconf.yaml` file. Here's a simple `falconf.yaml` for a Swift programming quiz:

```yaml
test:
  main: swift StudentMain.swift
submit:
  preprocess: falcon.concat SwizzleInclude.swift SwizzleBefore.swift StudentMain.swift SwizzleAfter.swift SwizzledMain.swift
  main: swift SwizzledMain.swift
  tear_down: rm SwizzledMain.swift
```

Notice the file is split into `test` and `submit` sections. These sections correspond to Falcon's `test` and `submit` modes, and they control which steps/commands are run when Falcon is invoked. The only required step for either section is `main`.

> **Note:** Any steps not listed for a section will be skipped. Steps can also be listed in any order, but they will always executed in same order (`preprocess`, `compile`, ...).

The `test` and `submit` modes should emulate what happens when a student selects "Test Code" or "Submit Code" in the classroom. Specifically, `test` should run a student's code without evaluating it for correctness, and `submit` should evaluate the student's code by testing it for correctness. Note that there is no check within Falcon for this behavior - it's up to you to keep to it.

### falconf.yaml

Here's an expanded `falconf.yaml` template:

```yaml
test:
  env_vars:
    VAR: value
    VAR2: value2
  grader_libs: [lib1, lib2]
  preprocess: command
  compile: command
  static_file_check: command (NOT READY, THIS WILL DO NOTHING)
  main: command
  postprocess: command
  tear_down: command
submit:
  (same structure as test)
```

It includes new entries — `env_vars` and `grader_libs` — in addition to the execution steps.

`env_vars` is a dict with any environment variables you want to set during the flight.

`grader_libs` is a list of directories within `udfalcon/graderlib` that you want to temporarily symlink into the cwd. This allows you to use any of the grader libraries without worrying about actually copying, moving or maintaining those files. They also disappear when the flight finishes, so your quiz directory stays clean (see "Testing a Grader Lib" below for more info).

### From Commands to Execution

Every command results in a captured stdout and stderr.

There are a few ways to define a command for each step in your falconf.yaml files. Here they are in descending order of "likelihood you'll use them":

1. A shell command, eg. `node app.js`.
2. A Falcon command, eg. `falcon.concat file1.swift file2.swift outfile.swift` (more on this momentarily).
3. An executable file, eg. `main.out`.
4. Nothing in the falconf, but a specially named file exists (more on this below).


#### (1) A Shell Command

```yaml
test:
  main: node student_app.js
```

Here, a shell command is executed.

### Default Files

Falcon tries to be smart. You can create default files for each step without specifying them within `falconf.yaml` by adhering to the following naming scheme within the directory from which you call Falcon:

`mode_stepname.ext`,

where `mode` is one of `test` or `submit` and `stepname` is one of the steps from above. Any extension works, however the file will be called as `./mode_stepname.ext`, so the file MUST BE EXECUTABLE. This may be a problem as `chmod`ing from Python feels dangerous and I don't do it at the moment.

### Falcon Output

As Falcon executes, it produces output for each execution step (as a JSON-like string) so that it can be passed back to the classroom for further evaluation. Here's example output generated by Falcon using the Swift example (for submit) from above:

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

> **Note:** Depending on how you design your quizzes, you can determine whether or not a student's submission is correct during Falcon's execution (the `is_correct` key/value pair) or later in the classroom. For example, using the output from above, one could determine correctness later, in the classroom, by analyzing the `<PASS::>` tags in the `student_out` key/value pair.

### Reading and Writing Udacity Out

`~/.ud_falcon_temp`

### Running Falcon from the Command Line

Once Falcon is installed on your $PATH, you can run it from anywhere. By default, it looks for a `falconf.yaml` file in the execution directory, but you can provide a custom path as well.

### Using a Grader Library

You'll need to link to the library.

### Testing a Grader Library

There's a feature to symlink a library to cwd without running Falcon.

#### Usage Instructions

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

## Maintainers

@jarrodparkes, @cameronwp

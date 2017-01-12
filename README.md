<img src="https://github.com/jarrodparkes/images/blob/master/falcon-icon.png?raw=true" alt="Falcon icon" align="left" height="64">

# Falcon

Falcon is a Python command-line tool for authoring and testing programming quizzes using [Udacity's remote execution stack (REX)](https://github.com/udacity/udacity-clyde).

## falconf.yaml

Sample falconf.yaml
```yaml
test:
  env_vars:
    VAR: value
    VAR2: value2
  grader_libs: [cpp-grader]
  preprocess: cmd
  compile: cmd
  static\_file\_check: cmd
  main: cmd
  postprocess: cmd
  tear_down: cmd
submit:
  (same structure as test)
```

Where each `cmd` can be one of (in priority order):

        falconf         |      file       |       Action
------------------------|-----------------|---------------------
1)  file.ext            |      <--        |   ./file.ext
2)  falcon.action ...   |       *         |   falcon action
3)  echo "bar"          |       *         |   echo "bar"
4)      --              | stepname.ext    |   ./stepname.ext
5)      --              |      --         |         --

Falcon commands take the form of `falcon.concat file1 file2 ... fileN outfile`.

EXECUTABLES MUST HAVE AN EXTENSION!

## Modes

In Falcon, two evaluation modes are supported:

- Test: Runs student's code without evaluating it for correctness
- Submit: Evaluate student's code by testing it for correctness.

## Stacks

In Falcon, a stack refers to a programming language and testing framework. Currently, the following stacks are supported:

- Swift^
- Javascript^
- Javascript + Mocha
- Ruby^
- C++

^ These stacks use simple pass/fail functions (like asserts) for testing.

## Running Locally

To run Falcon locally, use a command like the following:

`python falcon.py -s swift -m test -l`

In this case, this tells Falcon to...

1. evaluate the student's code in  **test** mode using the **swift** stack
2. substitute the local sandbox files as the "student's code"
3. use the **swift** stack's local-only functionality for setting up and tearing down your environment

Assuming you have all the proper tools installed (in this case, the Swift compiler — `swift`), and they are accessible via your `$PATH`, then you should be able to run this example without error. However, if you need to custom configure your environment or `$PATH`to run a stack, then you should take the following steps:

1. Create a **config** folder at the root
2. Create a file for the stack in the **config** folder (ex. `config/swift.sh`)
  - This file should contain any bash commands needed to configure your local environment to run the specified stack

### Special Flags

- use `-h` to see Falcon usage instructions
- use `-p` to "pretty format" results from **submit** mode
- if you are developing `falcon` and running into problems, use `-d` to see uncaught exceptions

## Running on REX

For the following reasons, running Falcon on REX is much easier than running it locally:

- REX environment and `$PATH` are preconfigured to work with each stack
- The student's code is delivered into the environment instead of being substituted from a local sandbox

To run previous example on REX, the following command would be used:

`python falcon.py -s swift -m test`

## Maintainers

@jarrodparkes

"""Generate feedback for student after evaluating their Code."""

import json
import falcon.files as files

def parse_results(results):
    """Analyzes results by consuming tags generated during evaluation.

    Currently, the classroom understands the following tags:
        - <PASS::>
        - <FAIL::>
        - <FEEDBACK::>

    Args:
        results (string): Output generated when student submits code.

    Returns:
        A tuple with the following values:
            - (bool) did student pass all criteria?
            - (int) number of passed criteria
            - (int) number of failed criteria
            - (array) an array of feedback strings
    """
    # keep running total of (passed) criteria
    numberOfCriteria = 0
    numberOfPasses = 0
    passed_criteria = []
    failed_criteria = []
    feedback = []
    # split lines by newline
    lines = results.split('\n')
    # go line-by-line and find formatted tags for criteria
    for line in lines:
        if line.startswith('<PASS::>'):
            numberOfCriteria += 1
            numberOfPasses += 1
            # strip tag and add criteria to array
            passed_criteria.append(line[8:])
        if line.startswith('<FAIL::>'):
            numberOfCriteria += 1
            # strip tag and add criteria to array
            failed_criteria.append(line[8:])
        if line.startswith('<FEEDBACK::>'):
            # strip tag and add feedback to array
            feedback.append(line[12:])
    # return results
    return (numberOfCriteria == numberOfPasses, passed_criteria, failed_criteria, feedback)

def markdown_from_criteria(passing_criteria, failing_criteria):
    """Generates markdown-like string based on passing/failing criteria.

    Args:
        passing_criteria (list): All passing criteria from quiz
        failing_criteria (list): All failing criteria from quiz

    Returns:
        A string in a markdown-like format that can be displayed in the classroom.
    """
    # init markdown-like string
    markdown = ''
    # was there more than 1 criteria?
    if passing_criteria + failing_criteria > 1:
        # add passing criteria to markdown
        if len(passing_criteria) >= 1:
            markdown += '# What Went Well\n\n'
            for criteria in passing_criteria:
                markdown += '- ' + criteria + '\n'
            markdown += '\n'
        # add failing criteria to markdown
        if len(failing_criteria) >= 1:
            markdown += '# What Went Wrong\n\n'
            for criteria in failing_criteria:
                markdown += '- ' + criteria + '\n'
            markdown += '\n'
    else:
        # if only 1 criteria, add it without headers to markdown
        markdown = passing_criteria[0] if grade_result['correct'] else failing_criteria[0]
    # return markdown-like string
    return markdown

def convert_json_string_to_feedback(results):
    """Converts results from remote exeuction into human-readable format.

    Args:
        results (string): JSON-like string containing all results from remote exeuction.

    Returns:
        A string in a markdown-like format that can be displayed in the classroom.
    """
    try:
        # convert JSON-like string into Python dictionary
        results_out = results[files.RESULTS_OUT]
    except:
        # if there was an error during the conversion, display it
        return 'could not convert json string into feedback'
    else:
        # did the execution produce an error?
        if results[files.RESULTS_ERR] == '':
            # nope! we can safely use the results
            (submission_correct, passing_criteria, failing_criteria, feedback) = parse_results(results_out)
            # use default markdown for criteria/feedback
            markdown_feedback = markdown_from_criteria(passing_criteria, failing_criteria)
            total_criteria = len(failing_criteria) + len(passing_criteria)
            all_feedback = markdown_feedback + '# Feedback\n\n'
            if len(failing_criteria) == 0:
                all_feedback += 'Your answer passed all our tests! Awesome job!'
            elif len(passing_criteria) >= total_criteria / 2:
                all_feedback += 'Not everything is correct yet, but you\'re close!'
            else:
                all_feedback += 'There\'s work left to do. Try tackling one problem at a time.'
            return all_feedback
        else:
            # main generated some an error, so display it!
            return 'An error occurred while testing your code.\n\nCheck to ensure these items are true:\n\n- clicking **TEST RUN** doesn\'t produce any issues\n- you\'ve followed all instructions\n- you\'ve used the correct names\n\nIf you make all these checks, but it still doesn\'t fix the error, then please contact us at *ios-support@udacity.com* and provide a link to the quiz and a copy of your code.\n\nNOTE: If you cannot find the instructions, click **RESET QUIZ** to reset the quiz to its original state.'

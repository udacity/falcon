import udfalcon
import os

def test_outputs_return_results():
    assert isinstance(udfalcon.fly({'output': 'return', 'mode': 'test'}), dict)

def test_can_symlink_grader_lib():
    os.chdir(os.path.dirname(os.path.join(os.environ['FALCON_HOME'], 'test')))
    output = udfalcon.fly({'config': 'test/as_import/falconf.yaml', 'mode': 'submit', 'output': 'return'})
    assert output['student_out'] == 'udacity main worked!'

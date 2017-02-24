import udfalcon

def test_outputs_return_results():
    assert isinstance(udfalcon.fly({'output': 'return', 'mode': 'test'}), dict)

import yaml

import lexic


def get_state_machines():
    sm = []
    for dic_file in ['delimiters', 'equal', 'brackets', 'logic', 'integers', 'variables']:
        with open(f"../state-machine-data/{dic_file}.yaml", 'r') as f:
            sm.append(yaml.full_load(f))
    return sm


def test_wrong_variables():
    sm = get_state_machines()
    assert lexic.lexic('1a', sm) == """Lexic error: unexpected data. 
 1A 
 ^"""
    assert lexic.lexic('-a-1', sm) == """Lexic error: unexpected data. 
 -A-1 
 ^"""


def test_wrong_equal():
    sm = get_state_machines()
    assert lexic.lexic('==', sm) == """Lexic error: unexpected data. 
 == 
 ^"""


def test_wrong_full():
    sm = get_state_machines()
    data = """1 2 3AND 4 NOT;NOT;1234
1234;5;1XOR = abacaba
a1aaa"""
    expected_result = """Lexic error: unexpected data. 
 1 2 3AND 4 NOT
     ^"""

    assert lexic.lexic(data, sm) == expected_result


test_wrong_variables()
test_wrong_equal()
test_wrong_full()

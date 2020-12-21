import yaml

import lexic


def get_state_machines():
    sm = []
    for dic_file in ['delimiters', 'equal', 'brackets', 'logic', 'integers', 'variables']:
        with open(f"../state-machine-data/{dic_file}.yaml", 'r') as f:
            sm.append(yaml.full_load(f))
    return sm


def test_correct_variables():
    sm = get_state_machines()
    assert lexic.lexic('a', sm) == [('VARIABLE', 'A')]
    assert lexic.lexic('a-1', sm) == [('VARIABLE', 'A-1')]
    assert lexic.lexic('a-b-a-c-a-ba-123', sm) == [('VARIABLE', 'A-B-A-C-A-BA-123')]


def test_correct_integers():
    sm = get_state_machines()
    assert lexic.lexic('0', sm) == [('INTEGER', '0')]
    assert lexic.lexic('10', sm) == [('INTEGER', '10')]
    assert lexic.lexic('910', sm) == [('INTEGER', '910')]


def test_correct_delimeters():
    sm = get_state_machines()
    assert lexic.lexic(';', sm) == [('DELIMITER', ';')]
    assert lexic.lexic(';;', sm) == [('DELIMITER', ';'), ('DELIMITER', ';')]
    assert lexic.lexic('\n ;', sm) == [('DELIMITER', '\n'), ('DELIMITER', ' '), ('DELIMITER', ';')]


def test_correct_equal():
    sm = get_state_machines()
    assert lexic.lexic('=', sm) == [('EQUAL', '=')]


def test_correct_logic():
    sm = get_state_machines()
    assert lexic.lexic('AND', sm) == [('LOGIC', 'AND')]
    assert lexic.lexic('XOR', sm) == [('LOGIC', 'XOR')]


def test_correct_brackets():
    sm = get_state_machines()
    assert lexic.lexic('(', sm) == [('BRACKET', '(')]
    assert lexic.lexic(')', sm) == [('BRACKET', ')')]
    assert lexic.lexic('((', sm) == [('BRACKET', '('), ('BRACKET', '(')]


def test_correct_full():
    sm = get_state_machines()
    data = """1 2 3 AND 4 NOT;NOT;1234
1234;5;XOR = abacaba
a1aaa"""
    expected_result = [
        ('INTEGER', '1'), ('DELIMITER', ' '), ('INTEGER', '2'), ('DELIMITER', ' '),
        ('INTEGER', '3'), ('DELIMITER', ' '), ('LOGIC', 'AND'), ('DELIMITER', ' '),
        ('INTEGER', '4'), ('DELIMITER', ' '), ('LOGIC', 'NOT'), ('DELIMITER', ';'),
        ('LOGIC', 'NOT'), ('DELIMITER', ';'), ('INTEGER', '1234'), ('DELIMITER', '\n'),
        ('INTEGER', '1234'), ('DELIMITER', ';'), ('INTEGER', '5'), ('DELIMITER', ';'),
        ('LOGIC', 'XOR'), ('DELIMITER', ' '), ('EQUAL', '='), ('DELIMITER', ' '),
        ('VARIABLE', 'ABACABA'), ('DELIMITER', '\n'), ('VARIABLE', 'A1AAA')
    ]

    assert lexic.lexic(data, sm) == expected_result


test_correct_variables()
test_correct_integers()
test_correct_delimeters()
test_correct_equal()
test_correct_logic()
test_correct_brackets()
test_correct_full()
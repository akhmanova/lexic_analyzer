import yaml

import lexic
import unittest


class TestCorrectData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sm = []
        print('Get state machines')
        for dic_file in ['delimiters', 'equal', 'brackets', 'logic', 'integers', 'variables']:
            with open(f"state-machine-data/{dic_file}.yaml", 'r') as f:
                cls.sm.append(yaml.full_load(f))

    def test_correct_variables(self):
        assert lexic.lexic('a', self.sm) == [('VARIABLE', 'A')]
        assert lexic.lexic('a-1', self.sm) == [('VARIABLE', 'A-1')]
        assert lexic.lexic('a-b-a-c-a-ba-123', self.sm) == [('VARIABLE', 'A-B-A-C-A-BA-123')]

    def test_correct_integers(self):
        assert lexic.lexic('0', self.sm) == [('INTEGER', '0')]
        assert lexic.lexic('10', self.sm) == [('INTEGER', '10')]
        assert lexic.lexic('910', self.sm) == [('INTEGER', '910')]

    def test_correct_delimeters(self):
        assert lexic.lexic(';', self.sm) == [('DELIMITER', ';')]
        assert lexic.lexic(';;', self.sm) == [('DELIMITER', ';'), ('DELIMITER', ';')]
        assert lexic.lexic('\n ;', self.sm) == [('DELIMITER', '\n'), ('DELIMITER', ' '), ('DELIMITER', ';')]

    def test_correct_equal(self):
        assert lexic.lexic('=', self.sm) == [('EQUAL', '=')]

    def test_correct_logic(self):
        assert lexic.lexic('AND', self.sm) == [('LOGIC', 'AND')]
        assert lexic.lexic('XOR', self.sm) == [('LOGIC', 'XOR')]

    def test_correct_brackets(self):
        assert lexic.lexic('(', self.sm) == [('BRACKET', '(')]
        assert lexic.lexic(')', self.sm) == [('BRACKET', ')')]
        assert lexic.lexic('((', self.sm) == [('BRACKET', '('), ('BRACKET', '(')]

    def test_correct_full(self):
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

        assert lexic.lexic(data, self.sm) == expected_result
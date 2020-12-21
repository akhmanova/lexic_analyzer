import yaml
import unittest

import lexic


class TestCorrectData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sm = []
        print('Get state machines')
        for dic_file in ['delimiters', 'equal', 'brackets', 'logic', 'integers', 'variables']:
            with open(f"state-machine-data/{dic_file}.yaml", 'r') as f:
                cls.sm.append(yaml.full_load(f))

    def test_wrong_variables(self):
        assert lexic.lexic('1a', self.sm) == """Lexic error: unexpected data. 
 1A 
 ^"""
        assert lexic.lexic('-a-1', self.sm) == """Lexic error: unexpected data. 
 -A-1 
 ^"""

    def test_wrong_equal(self):
        assert lexic.lexic('==', self.sm) == """Lexic error: unexpected data. 
 == 
 ^"""

    def test_wrong_full(self):
        data = """1 2 3AND 4 NOT;NOT;1234
1234;5;1XOR = abacaba
a1aaa"""
        expected_result = """Lexic error: unexpected data. 
 1 2 3AND 4 NOT
     ^"""

        assert lexic.lexic(data, self.sm) == expected_result

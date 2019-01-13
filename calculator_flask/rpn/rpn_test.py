import unittest

from calculator_flask.rpn import rpn


class TestCalculator(unittest.TestCase):
    def test_split(self):
        result = rpn.split_on_elements("10+10*10")
        self.assertEqual(
            ["10", "+", "10", "*", "10"],
            result,
        )

    def test_split_with_spaces(self):
        result = rpn.split_on_elements("10 + 10   * 10 ")
        self.assertEqual(
            ["10", "+", "10", "*", "10"],
            result,
        )

    def test_split_with_variations(self):
        result = rpn.split_on_elements(" 10 +10* 10")
        self.assertEqual(
            ["10", "+", "10", "*", "10"],
            result,
        )

    def test_split_with_parentheless(self):
        result = rpn.split_on_elements("(1 + 2) * 2")
        self.assertEqual(
            ["(", "1", "+", "2", ")", "*", "2"],
            result,
        )

    def test_with_letters(self):
        with self.assertRaises(RuntimeError) as cm:
            rpn.split_on_elements('10 + 10abc')

        self.assertIn('invalid symbol', str(cm.exception))

    def test_build_rpn(self):
        result = rpn.build_rpn(["2", "*", "3", "*", "4", "+", "5"])
        self.assertEqual(
            ["2", "3", "4", "*", "*", "5", "+"],
            result,
        )

    def test_build_rpn_2(self):
        result = rpn.build_rpn(["2", "*", "3", "*", "4", "+", "5", "/", "6"])
        self.assertEqual(
            ["2", "3", "4", "*", "*", "5", "6", "/", "+"],
            result,
        )

    def test_build_rpn_exponentiation(self):
        result = rpn.build_rpn(["2", "*", "3", "*", "4", "+", "5", "^", "2"])
        self.assertEqual(
            ["2", "3", "4", "*", "*", "5", "2", "^", "+"],
            result,
        )

    def test_build_rpn_parentheless(self):
        result = rpn.build_rpn(["(", "1", "+", "2", ")", "*", "2"])
        self.assertEqual(
            ["1", "2", "+", "2", "*"],
            result,
        )


    def test_stack_calculations(self):
        result = rpn.stack_calculations(["2", "3", "4", "*", "*", "5", "+"])
        self.assertEqual(29, result)

    def test_stack_calculations_2(self):
        result = rpn.stack_calculations(["2", "3", "4", "*", "*", "5", "-"])
        self.assertEqual(19, result)

    def test_stack_calculations_exponentiation(self):
        result = rpn.stack_calculations(["2", "3", "4", "*", "*", "5", "2", "^", "+"])
        self.assertEqual(49, result)

    def test_extra_operations(self):
        expressions = [
            "5 + 3 * 8 *",
            "5 + 3 * 8 * * *",
            "5 + 3 * * * 8",
            " / 5 + 3 * 8",

        ]
        for exp in expressions:
            with self.assertRaises(RuntimeError) as cm:
                rpn.evaluate(exp)
            self.assertIn('mismatched operators', str(cm.exception))

    def test_extra_operands(self):
        expressions = [
            "5 + 3 * 8 18",
            "20 5 + 3 * 8",
            "5 + 3 30 * 8"
        ]
        for exp in expressions:
            with self.assertRaises(RuntimeError) as cm:
                rpn.evaluate(exp)
            self.assertIn('mismatched operators', str(cm.exception))

    def test_extra_open_brackets(self):
        expressions = [
            "(1 + (5 + 3) * 8",
            "((2 + 10)",
            "(2 + 5"
        ]
        for exp in expressions:
            with self.assertRaises(RuntimeError) as cm:
                rpn.evaluate(exp)
            self.assertIn('mismatched brackets', str(cm.exception))

    def test_extra_closed_brackets(self):
        expressions = [
            "(1 + (5 + 3))) * 8",
            "(2 + 10))",
            "2 + 5)"
        ]
        for exp in expressions:
            with self.assertRaises(RuntimeError) as cm:
                rpn.evaluate(exp)
            self.assertIn('mismatched brackets', str(cm.exception))
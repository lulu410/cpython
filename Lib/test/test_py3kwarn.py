import unittest
from test.test_support import catch_warning, TestSkipped, run_unittest
import warnings

# TODO: This is a hack to raise TestSkipped if -3 is not enabled. Instead
# of relying on callable to have a warning, we should expose the -3 flag
# to Python code somehow
with catch_warning() as w:
    callable(int)
    if w.message is None:
        raise TestSkipped('%s must be run with the -3 flag' % __name__)

class TestPy3KWarnings(unittest.TestCase):

    def test_type_inequality_comparisons(self):
        expected = 'type inequality comparisons not supported in 3.x.'
        with catch_warning() as w:
            self.assertWarning(int < str, w, expected)
        with catch_warning() as w:
            self.assertWarning(type < object, w, expected)

    def test_object_inequality_comparisons(self):
        expected = 'comparing unequal types not supported in 3.x.'
        with catch_warning() as w:
            self.assertWarning(str < [], w, expected)
        with catch_warning() as w:
            self.assertWarning(object() < (1, 2), w, expected)

    def test_dict_inequality_comparisons(self):
        expected = 'dict inequality comparisons not supported in 3.x.'
        with catch_warning() as w:
            self.assertWarning({} < {2:3}, w, expected)
        with catch_warning() as w:
            self.assertWarning({} <= {}, w, expected)
        with catch_warning() as w:
            self.assertWarning({} > {2:3}, w, expected)
        with catch_warning() as w:
            self.assertWarning({2:3} >= {}, w, expected)

    def test_cell_inequality_comparisons(self):
        expected = 'cell comparisons not supported in 3.x.'
        def f(x):
            def g():
                return x
            return g
        cell0, = f(0).func_closure
        cell1, = f(1).func_closure
        with catch_warning() as w:
            self.assertWarning(cell0 == cell1, w, expected)
        with catch_warning() as w:
            self.assertWarning(cell0 < cell1, w, expected)

    def assertWarning(self, _, warning, expected_message):
        self.assertEqual(str(warning.message), expected_message)

def test_main():
    run_unittest(TestPy3KWarnings)

if __name__ == '__main__':
    test_main()

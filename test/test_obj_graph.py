from hypothesis import given
import hypothesis.strategies as st
import io
import unittest

from blendplot.obj_graph import *

import utilities

class TestObjGraph(unittest.TestCase):
    def test_add_cube_verticies(self):
        cube_str = ""
        x = 1.0
        y = 2.0
        z = 3.0
        point_size = 1.0

        actual = add_cube_verticies(cube_str, x, y, z, point_size)

        expected = "v 2.0 1.0 2.0\nv 2.0 1.0 4.0\nv 0.0 1.0 4.0\nv 0.0 1.0 2.0\nv 2.0 3.0 2.0\nv 2.0 3.0 4.0\nv 0.0 3.0 4.0\nv 0.0 3.0 2.0\n"

        self.assertEqual(actual, expected)

    def test_add_cube_verticies_non_empty(self):
        cube_str = "test\n"
        x = 1.0
        y = 2.0
        z = 3.0
        point_size = 1.0

        actual = add_cube_verticies(cube_str, x, y, z, point_size)

        expected = "test\nv 2.0 1.0 2.0\nv 2.0 1.0 4.0\nv 0.0 1.0 4.0\nv 0.0 1.0 2.0\nv 2.0 3.0 2.0\nv 2.0 3.0 4.0\nv 0.0 3.0 4.0\nv 0.0 3.0 2.0\n"

        self.assertEqual(actual, expected)

    def test_add_cube_faces(self):
        cube_str = ""
        start_num = 0

        actual = add_cube_faces(cube_str, start_num)

        expected = "f 1 2 3 4\nf 5 8 7 6\nf 1 5 6 2\nf 2 6 7 3\nf 3 7 8 4\nf 5 1 4 8\n"

        self.assertEqual(actual, expected)

    def test_add_cube_faces_non_empty(self):
        cube_str = "test\n"
        start_num = 0

        actual = add_cube_faces(cube_str, start_num)

        expected = "test\nf 1 2 3 4\nf 5 8 7 6\nf 1 5 6 2\nf 2 6 7 3\nf 3 7 8 4\nf 5 1 4 8\n"

        self.assertEqual(actual, expected)

    def test_cube_string(self):
        x = 1.0
        y = 2.0
        z = 3.0
        point_size = 1.0
        start_num = 0

        actual = cube_string(x, y, z, point_size, start_num)

        expected = "v 2.0 1.0 2.0\nv 2.0 1.0 4.0\nv 0.0 1.0 4.0\nv 0.0 1.0 2.0\nv 2.0 3.0 2.0\nv 2.0 3.0 4.0\nv 0.0 3.0 4.0\nv 0.0 3.0 2.0\nf 1 2 3 4\nf 5 8 7 6\nf 1 5 6 2\nf 2 6 7 3\nf 3 7 8 4\nf 5 1 4 8\n"

        self.assertEqual(actual, expected)

    def test_add_cube(self):
        x = 1.0
        y = 2.0
        z = 3.0
        point_size = 1.0
        start_num = 0
        output_file = io.StringIO()

        add_cube(x, y, z, point_size, start_num, output_file)
        actual = output_file.getvalue()

        expected = "v 2.0 1.0 2.0\nv 2.0 1.0 4.0\nv 0.0 1.0 4.0\nv 0.0 1.0 2.0\nv 2.0 3.0 2.0\nv 2.0 3.0 4.0\nv 0.0 3.0 4.0\nv 0.0 3.0 2.0\nf 1 2 3 4\nf 5 8 7 6\nf 1 5 6 2\nf 2 6 7 3\nf 3 7 8 4\nf 5 1 4 8\n"

        self.assertEquals(actual, expected)

    def test_plot(self):
        rows = [(1.0, 1.0, 1.0), (2.0, 2.0, 2.0)]
        spacing = 0.5
        point_size = 0.1
        output_file = io.StringIO()
        start_num = 0

        actual_ret = plot(rows, spacing, point_size, output_file, start_num)
        expected_ret = 16

        self.assertEquals(actual_ret, expected_ret)

        actual_output = output_file.getvalue()

        expected_output = "v 0.6 0.4 0.4\nv 0.6 0.4 0.6\nv 0.4 0.4 0.6\nv 0.4 0.4 0.4\nv 0.6 0.6 0.4\nv 0.6 0.6 0.6\nv 0.4 0.6 0.6\nv 0.4 0.6 0.4\nf 1 2 3 4\nf 5 8 7 6\nf 1 5 6 2\nf 2 6 7 3\nf 3 7 8 4\nf 5 1 4 8\nv 1.1 0.9 0.9\nv 1.1 0.9 1.1\nv 0.9 0.9 1.1\nv 0.9 0.9 0.9\nv 1.1 1.1 0.9\nv 1.1 1.1 1.1\nv 0.9 1.1 1.1\nv 0.9 1.1 0.9\nf 9 10 11 12\nf 13 16 15 14\nf 9 13 14 10\nf 10 14 15 11\nf 11 15 16 12\nf 13 9 12 16\n"

        self.assertEquals(actual_output, expected_output)

    def test_plot_file(self):
        input_filename = "test/resources/data_01.csv"
        output_file = io.StringIO()
        num_rows = None
        columns = ["a", "b", "c"]
        spacing = 0.5
        point_size = 0.1
        category_column = None
        scale_function = "scale"

        actual_ret = plot_file(input_filename, output_file, num_rows, columns, spacing, point_size, category_column, scale_function)
        expected_ret = 5

        self.assertEquals(actual_ret, expected_ret)

        actual_output = output_file.getvalue()

        test_file = "test/expected/test_plot_file.obj"
        with open(test_file, 'r') as myfile:
            expected_output = myfile.read()

            self.assertEquals(actual_output, expected_output)

    def test_plot_file_scale_functions(self):
        functions = ["maxabs_scale", "minmax_scale", "normalize", "robust_scale", "scale", "none"]
        for func in functions:
            input_filename = "test/resources/data_01.csv"
            output_file = io.StringIO()
            num_rows = None
            columns = ["a", "b", "c"]
            spacing = 0.5
            point_size = 0.1
            category_column = None
            scale_function = func

            actual_ret = plot_file(input_filename, output_file, num_rows, columns, spacing, point_size, category_column, scale_function)
            expected_ret = 5

            self.assertEquals(actual_ret, expected_ret)

            actual_output = output_file.getvalue()

            test_file = "test/expected/test_plot_file_scale_function_" + func + ".obj"
            with open(test_file, 'r') as myfile:
                expected_output = myfile.read()

                self.assertEquals(actual_output, expected_output)

    def test_plot_file_invalid_column(self):
        input_filename = "test/resources/data_01.csv"
        output_file = io.StringIO()
        num_rows = None
        invalid_column = "u"
        columns = [invalid_column, "b", "c"]
        spacing = 0.5
        point_size = 0.1
        category_column = None
        scale_function = "scale"

        func = lambda x: plot_file(input_filename, output_file, num_rows, columns, spacing, point_size, category_column, scale_function)

        (actual_return, actual_error) = utilities.capture_stderr(func)
        expected_error = "Invalid column(s): %s\nValid columns are: a, b, c, d, category\n" % invalid_column

        self.assertEquals(actual_error, expected_error)
        self.assertEquals(actual_return, None)

        actual_output = output_file.getvalue()
        expected_output = ""

        self.assertEquals(actual_output, expected_output)

    def test_plot_file_invalid_column_multiple(self):
        input_filename = "test/resources/data_01.csv"
        output_file = io.StringIO()
        num_rows = None
        invalid_columns = ["u", "A"]
        columns = ["c"] + invalid_columns
        spacing = 0.5
        point_size = 0.1
        category_column = None
        scale_function = "scale"

        func = lambda x: plot_file(input_filename, output_file, num_rows, columns, spacing, point_size, category_column, scale_function)

        (actual_return, actual_error) = utilities.capture_stderr(func)
        expected_error = "Invalid column(s): %s, %s\nValid columns are: a, b, c, d, category\n" % (invalid_columns[0], invalid_columns[1])

        self.assertEquals(actual_error, expected_error)
        self.assertEquals(actual_return, None)

        actual_output = output_file.getvalue()
        expected_output = ""

        self.assertEquals(actual_output, expected_output)

    def test_plot_file_category(self):
        input_filename = "test/resources/data_01.csv"
        output_file = io.StringIO()
        num_rows = 4
        columns = ["a", "b", "c"]
        spacing = 0.5
        point_size = 0.1
        category_column = "category"
        scale_function = "scale"

        actual_ret = plot_file(input_filename, output_file, num_rows, columns, spacing, point_size, category_column, scale_function)
        expected_ret = num_rows

        self.assertEquals(actual_ret, expected_ret)

        actual_output = output_file.getvalue()

        test_file = "test/expected/test_plot_file_category.obj"
        with open(test_file, 'r') as myfile:
            expected_output = myfile.read()

            self.assertEquals(actual_output, expected_output)

    def test_plot_file_category_invalid(self):
        input_filename = "test/resources/data_01.csv"
        output_file = io.StringIO()
        num_rows = 4
        columns = ["a", "b", "c"]
        spacing = 0.5
        point_size = 0.1
        invalid_category_column = "cats"
        scale_function = "scale"

        func = lambda x: plot_file(input_filename, output_file, num_rows, columns, spacing, point_size, invalid_category_column, scale_function)

        (actual_return, actual_error) = utilities.capture_stderr(func)
        expected_error = "Invalid column(s): %s\nValid columns are: a, b, c, d, category\n" % invalid_category_column

        self.assertEquals(actual_error, expected_error)
        self.assertEquals(actual_return, None)

        actual_output = output_file.getvalue()
        expected_output = ""

        self.assertEquals(actual_output, expected_output)

@given(
  st.text(),
  st.floats(allow_nan=False, allow_infinity=False),
  st.floats(allow_nan=False, allow_infinity=False),
  st.floats(allow_nan=False, allow_infinity=False),
  st.floats(allow_nan=False, allow_infinity=False)
  )
def test_add_cube_verticies_length(cube_str, x, y, z, point_size):
    """
    The length of the return value of add_cube_verticies should always be larger
    than the length of the cube_str passed in.
    """
    actual = add_cube_verticies(cube_str, x, y, z, point_size)
    assert len(actual) > len(cube_str)

@given(
  st.text(),
  st.integers()
  )
def test_add_cube_faces_length(cube_str, start_num):
    """
    The length of the return value of add_cube_faces should always be larger
    than the length of the cube_str passed in.
    """
    actual = add_cube_faces(cube_str, start_num)
    assert len(actual) > len(cube_str)

@given(
  st.floats(allow_nan=False, allow_infinity=False),
  st.floats(allow_nan=False, allow_infinity=False),
  st.floats(allow_nan=False, allow_infinity=False),
  st.floats(allow_nan=False, allow_infinity=False),
  st.integers()
  )
def test_add_cube_verticies_length(x, y, z, point_size, start_num):
    """
    The length of the return of cube_string should always be larger than 0.
    """
    actual = cube_string(x, y, z, point_size, start_num)
    assert len(actual) > 0

@given(
  st.lists(
      st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=3, max_size=3)
      , min_size=1),
  st.floats(allow_nan=False, allow_infinity=False),
  st.floats(allow_nan=False, allow_infinity=False),
  st.integers()
  )
def test_plot(rows, spacing, point_size, start_num):
    """
    plot should always return an expected new start_num based on the number of
    rows passed in. Also, the output should have a length greated than 0, and
    have an expected number of lines based on the number of rows.
    """
    rows = [(1.0, 1.0, 1.0), (2.0, 2.0, 2.0)]
    output_file = io.StringIO()

    actual_ret = plot(rows, spacing, point_size, output_file, start_num)
    expected_ret = 8 * len(rows) + start_num

    assert actual_ret == expected_ret

    actual_output = output_file.getvalue()

    assert len(actual_output) > 0
    assert len(actual_output.split("\n")) == len(rows) * 14 + 1

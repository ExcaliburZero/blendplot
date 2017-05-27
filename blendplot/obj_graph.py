"""
Functions for plotting datasets as 3D models in obj format for use in Blender.
"""
from sklearn import preprocessing
import pandas as pd
import sys

def add_cube_verticies(cube_str, x, y, z, point_size):
    """
    Appends the described cube verticies to the given string.

    Parameters
    ----------
    cube_str : str
        the curent string representation of the cube
    x : float
        the x position of the cube
    y : float
        the y position of the cube
    z : float
        the z position of the cube
    point_size : float
        the size of the cube
    """
    vert_permutations = [
                (1,-1,-1),
                (1,-1,1),
                (-1,-1,1),
                (-1,-1,-1),
                (1,1,-1),
                (1,1,1),
                (-1,1,1),
                (-1,1,-1)
            ]
    for perm in vert_permutations:
        cube_str += "v %s %s %s\n" % (
                    x + (point_size * perm[0]),
                    y + (point_size * perm[1]),
                    z + (point_size * perm[2])
                )
    return cube_str

def add_cube_faces(cube_str, start_num):
    """
    Appends the described cube faces to the given string.

    Parameters
    ----------
    cube_str : str
        the curent string representation of the cube
    start_num : int
        the last used vertex number
    """
    face_permutations = [
                (1,2,3,4),
                (5,8,7,6),
                (1,5,6,2),
                (2,6,7,3),
                (3,7,8,4),
                (5,1,4,8)
            ]
    for perm in face_permutations:
        cube_str += "f %s %s %s %s\n" % (
                    start_num + perm[0],
                    start_num + perm[1],
                    start_num + perm[2],
                    start_num + perm[3]
                )
    return cube_str

def cube_string(x, y, z, point_size, start_num):
    """
    Returns a string representing the specified cube in obj file formating.

    Parameters
    ----------
    x : float
        the x position of the cube
    y : float
        the y position of the cube
    z : float
        the z position of the cube
    point_size : float
        the size of the cube
    start_num : int
        the last used vertex number
    """
    cube_str = ""
    cube_str = add_cube_verticies(cube_str, x, y, z, point_size)
    cube_str = add_cube_faces(cube_str, start_num)

    return cube_str

def add_cube(x, y, z, point_size, start_num, output_file):
    """
    Writes the specified cube to the given data file.

    Parameters
    ----------
    x : float
        the x position of the cube
    y : float
        the y position of the cube
    z : float
        the z position of the cube
    point_size : float
        the size of the cube
    start_num : int
        the last used vertex number
    output_file : file
        the file to write the cube to
    """
    output_file.write(
            cube_string(x, y, z, point_size, start_num))

def plot(rows, spacing, point_size, output_file, start_num):
    """
    Plots the given 3D dataset using the given range scaling and point size to
    the given output file.

    Parameters
    ----------
    rows : 2d list
        the rows of the 3D dataset to plot
    spacing : float
        the scaling of the data range
    point_size : float
        the size to use for the data points
    output_file : file
        the file to write the plot to
    start_num : int
        the last used vertex number

    Returns
    -------
    start_num : int
        the new last used vertex number
    """
    for row in rows:
        x = row[0] * spacing
        y = row[1] * spacing
        z = row[2] * spacing
        add_cube(x, y, z, point_size, start_num, output_file)
        start_num += 8

    return start_num

def plot_file(input_filename, output_file, num_rows, columns, spacing, point_size, category_column, scale_function):
    """
    Plots the data from the given input file to the given output file and
    returns the number of points plotted.

    Parameters
    ----------
    input_filename : str
        the path to the input data file
    output_file : file
        the file to write the plot to
    num_rows : int
        the number of rows to plot, or None to plot all rows
    columns : List[str]
        the columns to plot
    spacing : float
        the scaling of the data range
    point_size : float
        the size to use for the data points
    category_column : str
        the column to categorize the points by, or None to plot data without
        categories
    scale_function : str
        the name of the data scaling function to use

    Returns
    -------
    points : int
        the number of points that were plotted, or None if the plot is unable
        to be made
    """
    original_data = pd.read_csv(input_filename, nrows = num_rows)

    missing = get_missing_columns(original_data, columns, category_column)
    if len(missing) > 0:
        missing_columns = ", ".join(missing)
        valid_columns = ", ".join(list(original_data.columns))
        error_msg = "Invalid column(s): %s\n" % missing_columns
        error_msg += "Valid columns are: %s" % valid_columns
        print(error_msg, file=sys.stderr)
        return None

    data = pd.DataFrame(original_data, columns = columns).dropna()
    data = pd.DataFrame(scale_data(data, scale_function), columns = data.columns)

    start_num = 0

    if category_column is None:
        rows = zip(data[columns[0]], data[columns[1]], data[columns[2]])

        output_file.write("o data\n")
        plot(rows, spacing, point_size, output_file, start_num)
    else:
        data[category_column] = original_data[category_column]

        categories = data[category_column].unique()
        for cat in categories:
            cat_data = data[data[category_column] == cat]
            rows = zip(cat_data[columns[0]], cat_data[columns[1]], cat_data[columns[2]])

            output_file.write("o %s\n" % cat)
            start_num = plot(rows, spacing, point_size, output_file, start_num)

    points = num_rows if num_rows is not None else len(data.index)
    return points

def get_missing_columns(data, columns, category_column):
    """
    Returns all of the given columns that are not in the given dataframe.

    Parameters
    ----------
    columns : List[str]
        the columns to look for
    category_column : str
        the category column to look for, or None if there is no category column
        being used

    Returns
    -------
    missing : List[str]
        a list of the missing columns
    """
    data_columns = set(data.columns)

    if not category_column is None:
        columns = columns + [category_column]

    missing = []
    for col in columns:
        if not col in data_columns:
            missing.append(col)

    return missing

def scale_data(original_data, scale_name):
    scale_functions = {
                "maxabs_scale": preprocessing.maxabs_scale,
                "minmax_scale": preprocessing.minmax_scale,
                "normalize": preprocessing.normalize,
                "robust_scale": preprocessing.robust_scale,
                "scale": preprocessing.scale,
                "none": lambda x: x
            }

    function = scale_functions[scale_name]
    scaled_data = function(original_data)

    return scaled_data

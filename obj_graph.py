#!/usr/bin/env python
"""
A script for plotting datasets as 3D models in obj format for use in Blender.
"""
from sklearn import preprocessing
from math import *
import cli.app
import pandas as pd
import time

@cli.app.CommandLineApp
def obj_graph(app):
    """
    Runs the cli interface form the program.

    Parameters
    ----------
    app : cli.app.CommandLineApp
        the cli information
    """
    input_filename = app.params.input_file
    output_filename = app.params.output_file
    num_rows = app.params.rows
    columns = [
                app.params.x,
                app.params.y,
                app.params.z
            ]
    spacing = app.params.spacing
    point_size = app.params.pointsize

    main(input_filename, output_filename, num_rows, columns, spacing, point_size)

obj_graph.add_param("input_file", help="data file to plot", type=str)
obj_graph.add_param("output_file", help="obj file to output to", type=str)
obj_graph.add_param("x", help="x column", type=str)
obj_graph.add_param("y", help="y column", type=str)
obj_graph.add_param("z", help="z column", type=str)

obj_graph.add_param("-r", "--rows", help="number of rows from the data file to plot", default=None, type=int)
obj_graph.add_param("--spacing", help="the scaling factor to space the data out by", default=2.0, type=float)
obj_graph.add_param("--pointsize", help="the size to use for the data points", default=0.0625, type=float)

def main(input_filename, output_filename, num_rows, columns, spacing, point_size):
    """
    Plots the data in the given input file to the given output file with the
    specified settings.

    Parameters
    ----------
    input_filename : str
        the path to the input data file
    output_filename : file
        the path of the file to write the plot to
    num_rows : int
        the number of rows to plot, or None to plot all rows
    columns : List[str]
        the columns to plot
    spacing : float
        the scaling of the data range
    point_size : float
        the size to use for the data points
    """
    output_file = open(output_filename, "w")
    start = time.time()
    points = plot_file(input_filename, output_file, num_rows, columns, spacing, point_size)
    end = time.time()
    output_file.close()

    print("Wrote plot file to %s" % output_filename)
    print("Plotted %s points in %f seconds" % (points, end - start))

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

def plot(rows, spacing, point_size, output_file):
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
    """
    start_num = 0
    for row in rows:
        x = row[0] * spacing
        y = row[1] * spacing
        z = row[2] * spacing
        add_cube(x, y, z, point_size, start_num, output_file)
        start_num += 8

def plot_file(input_filename, output_file, num_rows, columns, spacing, point_size):
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
    """
    data = pd.read_csv(input_filename, nrows = num_rows)
    data = pd.DataFrame(data, columns = columns).dropna()
    data = pd.DataFrame(preprocessing.scale(data), columns = data.columns)

    rows = zip(data[columns[0]], data[columns[1]], data[columns[2]])

    plot(rows, spacing, point_size, output_file)

    points = num_rows if num_rows != None else len(data.index)
    return points

if __name__ == "__main__":
    obj_graph.run()

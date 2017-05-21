"""Plot 3D data sets in Blender."""
from sklearn import preprocessing
from math import *
import pandas as pd
import time

def cube_string(x, y, z, scale, start_num):
    cube_str = ""

    # Add verticies
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
        cube_str += "v %s %s %s\n" % (x + (scale * perm[0]), y + (scale * perm[1]), z + (scale * perm[2]))

    # Add faces
    face_permutations = [
                (1,2,3,4),
                (5,8,7,6),
                (1,5,6,2),
                (2,6,7,3),
                (3,7,8,4),
                (5,1,4,8)
            ]
    for perm in face_permutations:
        cube_str += "f %s %s %s %s\n" % (start_num + perm[0], start_num + perm[1], start_num + perm[2], start_num + perm[3])

    return cube_str

def add_cube(x, y, z, scale, start_num, output_file):
    output_file.write(
            cube_string(x, y, z, scale, start_num))

def plot(rows, range_scaling, point_size, output_file):
    """
    Plot the given 3D dataset using the given range scaling and point size.

    Parameters
    ----------
    rows : 2d list
        the rows of the 3D dataset to plot
    range_scaling : float
        the scaling of the data range
    point_size : float
        the scaling factor to use for the data points
    """
    start_num = 0
    for row in rows:
        x = row[0] * range_scaling
        y = row[1] * range_scaling
        z = row[2] * range_scaling
        add_cube(x, y, z, point_size, start_num, output_file)
        start_num += 8

def main(input_filename, rows, columns, output_file):
    """Plot given data."""
    data = pd.read_csv(input_filename, nrows = rows)
    data = pd.DataFrame(data, columns = columns).dropna()
    data = pd.DataFrame(preprocessing.scale(data), columns = data.columns)

    rows = zip(data[columns[0]], data[columns[1]], data[columns[2]])

    scaling = 2
    point_size = 0.0625

    plot(rows, scaling, point_size, output_file)

if __name__ == "__main__":
    input_filename = "~/Documents/ogle/ogle4/lmc/RRab.csv"
    output_filename = "test.obj"
    rows = 27621
    columns = ["period", "amplitude_Iband", "magnitude_Iband"]

    output_file = open(output_filename, "w")
    start = time.time()
    main(input_filename, rows, columns, output_file)
    end = time.time()
    output_file.close()

    print(str(rows) + "," + str(end - start))

"""Plot 3D data sets in Blender."""
from sklearn import preprocessing
from mathutils import *
from math import *
import bpy
import pandas as pd
import time

def plot(rows, range_scaling, point_size):
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
    obj_scale = Vector((point_size, point_size, point_size))
    for row in rows:
        x = row[0] * range_scaling
        y = row[1] * range_scaling
        z = row[2] * range_scaling
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.active_object
        cube.scale = obj_scale
        cube.location = (x, y, z)

def main(filename, rows, columns):
    """Plot OGLE IV LMC RRab RR Lyrae data."""
    data = pd.read_csv(filename, nrows = rows)
    data = pd.DataFrame(data, columns = columns).dropna()
    data = pd.DataFrame(preprocessing.minmax_scale(data), columns = data.columns)

    rows = zip(data[columns[0]], data[columns[1]], data[columns[2]])

    scaling = 5 * 0.5
    point_size = 0.03

    plot(rows, scaling, point_size)

if __name__ == "__main__":
    filename = "~/Documents/ogle/ogle4/smc/RRab.csv"
    rows = 200
    columns = ["period", "amplitude_Iband", "magnitude_Iband"]

    start = time.time()
    main(filename, rows, columns)
    end = time.time()

    print(str(rows) + "," + str(end - start))

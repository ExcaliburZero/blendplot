"""Plot 3D data sets in Blender."""
import bpy
import pandas as pd

def normalize(df):
    """
    Normalize the given dataframe.

    https://stackoverflow.com/questions/12525722/normalize-data-in-pandas

    Parameters
    ----------
    df : data frame
        the data frame to normalize

    Returns
    -------
    data frame
        the normalized data frame
    """
    return (df - df.mean()) / (df.max() - df.min())

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
    for row in rows:
        x = row[0] * scaling
        y = row[1] * scaling
        z = row[2] * scaling
        cube = bpy.ops.mesh.primitive_cube_add()
        bpy.ops.transform.resize(value=(point_size, point_size, point_size))
        bpy.ops.transform.translate(value=(x, y, z))

def main():
    """Plot OGLE IV LMC RRab RR Lyrae data."""
    file = "~/Code/test/RRab.dat"
    data = pd.read_csv(file, delim_whitespace=True)
    data = normalize(data)

    rows = zip(data["period"], data["amplitude"], data["magnitude"])

    scaling = 5
    point_size = 0.01

    plot(rows, scaling, point_size)

main()

"""
A cli application for plotting 3D data in obj format for use in Blender.
"""
import cli.app
import sys
import time

from . import obj_graph

@cli.app.CommandLineApp
def blendplot(app):
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
    point_size = app.params.point_size
    category_column = app.params.category
    scale_function = app.params.scale_function

    main(input_filename, output_filename, num_rows, columns, spacing, point_size, category_column, scale_function)

blendplot.add_param("input_file", help="data file to plot", type=str)
blendplot.add_param("output_file", help="obj file to output to", type=str)
blendplot.add_param("x", help="x column", type=str)
blendplot.add_param("y", help="y column", type=str)
blendplot.add_param("z", help="z column", type=str)

blendplot.add_param("-r", "--rows", help="number of rows from the data file to plot", default=None, type=int)
blendplot.add_param("--spacing", help="the scaling factor to space the data out by", default=2.0, type=float)
blendplot.add_param("--point-size", help="the size to use for the data points", default=0.0625, type=float)
blendplot.add_param("-c", "--category", help="the column to use for point categorization", default=None, type=str)
blendplot.add_param("--scale-function", help="the function to use for scaling the data, valid options are \"maxabs_scale\", \"minmax_scale\", \"normalize\", \"robust_scale\", \"scale\", and \"none\"", default="scale", type=str)

def main(input_filename, output_filename, num_rows, columns, spacing, point_size, category_column, scale_function):
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
    category_column : str
        the column to categorize the points by, or None to plot data without
        categories
    scale_function : str
        the name of the data scaling function to use
    """
    valid_scale_functions = ["maxabs_scale", "minmax_scale", "normalize", "robust_scale", "scale", "none"]
    if not scale_function in valid_scale_functions:
        print("Invalid scale-function: %s" % scale_function, file=sys.stderr)

        valid_function_list = ", ".join(valid_scale_functions)
        print("Valid scale-functions are: %s" % valid_function_list, file=sys.stderr)
        sys.exit(1)

    output_file = open(output_filename, "w")
    start = time.time()
    points = obj_graph.plot_file(input_filename, output_file, num_rows, columns, spacing, point_size, category_column, scale_function)
    end = time.time()
    output_file.close()

    if points is None:
        sys.exit(1)
    else:
        print("Wrote plot file to %s" % output_filename)
        print("Plotted %s points in %f seconds" % (points, end - start))

def run():
    blendplot.run()

if __name__ == "__main__":
    run()

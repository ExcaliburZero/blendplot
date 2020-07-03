# Blendplot [![Travis CI Status](https://api.travis-ci.org/ExcaliburZero/blender-astro-visualization.svg)](https://travis-ci.org/ExcaliburZero/blender-astro-visualization) [![Coverage Status](https://coveralls.io/repos/github/ExcaliburZero/blender-astro-visualization/badge.svg?branch=master)](https://coveralls.io/github/ExcaliburZero/blender-astro-visualization?branch=master) [![Documentation Status](https://readthedocs.org/projects/blendplot/badge/?version=latest)](http://blendplot.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/blendplot.svg)](https://pypi.org/project/blendplot/)
Blendplot is a command line application for generating 3D data plots for use in Blender.

```
$ blendplot abc.csv abc.obj period amplitude_Iband magnitude_Iband -c category 
Wrote plot file to abc.obj
Plotted 37099 points in 1.531214 seconds
```

![An example of a model generated with Blendplot using data from the OGLE IV lmc survey](img/render_01.png)

## Installation
### From PyPI
```
pip install blendplot
```

### From source
To install Blendplot from source you can run the following commands.

```
git clone https://github.com/ExcaliburZero/blender-astro-visualization.git
cd blender-astro-visualization
pip install ./
```

## Usage
Blendplot allows you to generate a 3D data plot model by specifying a dataset file, the output model file (`.obj`), and the names of the three (x,y,z) columns you want to plot. Currently it only supports `.csv` input data files. The commad structure to run blendplot is as follows.

```
blendplot INPUT_FILE OUTPUT_FILE X Y Z
```

For example, to create a model from a data file `data.csv` using the columns `height`, `weight`, and `cost` and output to a file `model.obj` you would run the following command.

```
blendplot data.csv model.obj height weight cost
```

Once you have used the script to generate the model file, you can then import it into Blender by going to `File > Import > Wavefront (.obj)` and selecting the model file.

![Importing the model file into Blender](img/blender_obj_import.png)

## Documentation
For futher in-depth information on how to use Blendplot, see the documentation at the link below.

* [Blendplot - Read The Docs](https://blendplot.readthedocs.io)

## Licensing
The source code for Blendplot is available under the [MIT License](https://opensource.org/licenses/MIT), see `LICENSE` for more information.

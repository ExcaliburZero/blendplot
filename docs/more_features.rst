.. _more_features:

More Features
=============

Plotting Categories
-------------------

To plot data that is grouped into categories, you can use the -c flag and specify the name of the column to group the data points by. Each different category will be its own object in the resulting model. This will allow you to easily style the groups with different materials.

::

    blendplot data.csv model.obj height weight cost -c category

.. image:: ../img/category_objects.png
   :height: 321px
   :width: 280px
   :scale: 100 %
   :align: center

Setting Number of Rows to Plot
------------------------------

If you have a particularly large dataset, but only want to plot some of the points then you can use the ``-r`` or ``--rows`` flags to specify how many rows you want to plot. When you use the flag and specify a number of rows ``n``, then only the first ``n`` points in the dataset will be plotted. 

For example, the following command will plot only the first 20 points in the dataset.

::

    blendplot data.csv model.obj height weight cost --rows 20

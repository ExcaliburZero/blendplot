from setuptools import setup

setup( \
      name='blendplot',
      version='1.0.0',
      description='A program for plotting 3D scatter plots for use in Blender',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/ExcaliburZero/blender-astro-visualization',
      author='Christopher Wells',
      author_email='cwellsny@nycap.rr.com',
      license='MIT',
      packages=['blendplot'],
      install_requires=[
          'pyCLI',
          'sklearn',
          'scipy',
          'pandas'
      ],
      include_package_data=True,
      package_data={
          '': ['LICENSE']
      },

      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License'
      ],
      entry_points = {
          'console_scripts': [
              'blendplot = blendplot.__main__:run',
          ],              
      },
     )


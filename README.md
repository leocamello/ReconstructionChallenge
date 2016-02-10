# DroneDeploy

## Reconstruction Challenge

![Output](/out.png)

### Libraries

- Numpy
- PyOpenGL
- PyOpenGL-accelerate
- Python Imaging Library (PIL)

### How To Run

In my development environment I have been using [Conda](http://conda.pydata.org/docs/index.html) package manager. It is included in [Anaconda](https://www.continuum.io/downloads) Python distribution which already comes with Numpy.

To install PIL, PyOpenGL and PyOpenGL-accelerate:

```bash
$ conda install pil
$ conda install pyopengl
$ conda install pyopengl-accelerate
```

To run the Reconstruction Challenge script:

```bash
$ python main.py example.csv example/
```
*example.csv* is the file with the cameras information and *example/* is the directory where the images specified in the .csv are.

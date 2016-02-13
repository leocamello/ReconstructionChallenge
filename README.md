# DroneDeploy

## Reconstruction Challenge

![](/out3.png)

### Libraries

- Numpy
- PyProj
- PyOpenGL
- PyOpenGL-accelerate
- Python Imaging Library (PIL)

### How To Run

In my development environment I have been using [Conda](http://conda.pydata.org/docs/index.html) package manager. It is included in [Anaconda](https://www.continuum.io/downloads) Python distribution which already comes with Numpy.

To install PIL, PyOpenGL and PyOpenGL-accelerate:

```bash
$ conda install pil
$ conda install pyproj
$ conda install pyopengl
$ conda install pyopengl-accelerate
```

To run the Reconstruction Challenge script:

```bash
$ python main.py example.csv example/
```
*example.csv* is the file with the cameras information and *example/* is the directory where the images specified in the .csv are.

### Application

After successfully running the Reconstruction Challenge script a new window will popup showing the **mosaic** that was created.

![](/out1.png)

#### Keyboard Shortcuts

**F**: Enable or disable the frustum of the cameras. The selected camera's frustum is displayed in yellow.

![](/out2.png)

**N**: Selects the next camera

![](/out3.png)

**P**: Selects the previous camera

![](/out4.png)

**S**: Take an screenshot of the area being viewed in the window. The image file is saved as *out.png*. All screenshots for this document were taken with this feature.

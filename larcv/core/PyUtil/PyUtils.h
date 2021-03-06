#ifndef __LARCV_PYUTILS_H__
#define __LARCV_PYUTILS_H__

struct _object;
typedef _object PyObject;

#ifndef __CLING__
#ifndef __CINT__
#include <Python.h>
#endif
#endif

#include "larcv/core/DataFormat/Image2D.h"
#include "larcv/core/DataFormat/Voxel.h"

namespace larcv {
/// Utility function: call one-time-only numpy module initialization (you don't
/// have to call)
void SetPyUtil();
///
PyObject *as_ndarray(const std::vector<float> &data);
/// larcv::Image2D to numpy array converter
PyObject *as_ndarray(const Image2D &img);
/// larcv::Image2D to numpy array converter
PyObject *as_caffe_ndarray(const Image2D &img);
/// copy array
void copy_array(PyObject *arrayin, const std::vector<float> &cvec);
// void copy_array(PyObject *arrayin);//, const std::vector<float>& vec);

Image2D as_image2d_meta(PyObject *, ImageMeta meta);

Image2D as_image2d(PyObject *);

VoxelSet as_tensor3d(PyObject *, float min_threshold=0);

// allows one to avoid some loops in python
void fill_img_col(Image2D &img, std::vector<short> &adcs, const int col,const float pedestal = 0.0);
                  //const int timedownsampling, const float pedestal = 0.0);
}

#endif

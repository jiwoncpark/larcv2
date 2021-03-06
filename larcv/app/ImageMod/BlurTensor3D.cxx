#ifndef __BLURTENSOR3D_CXX__
#define __BLURTENSOR3D_CXX__

#include "BlurTensor3D.h"
#include "larcv/core/DataFormat/EventVoxel3D.h"

namespace larcv {

  static BlurTensor3DProcessFactory __global_BlurTensor3DProcessFactory__;

  BlurTensor3D::BlurTensor3D(const std::string name)
    : ProcessBase(name)
  {}

  void BlurTensor3D::configure_labels(const PSet& cfg)
  {
    _tensor3d_producer_v.clear();
    _output_producer_v.clear();
    _tensor3d_producer_v = cfg.get<std::vector<std::string> >("Tensor3DProducerList",_tensor3d_producer_v);
    _output_producer_v   = cfg.get<std::vector<std::string> >("OutputProducerList",_output_producer_v);

    if(_tensor3d_producer_v.empty()) {
      auto tensor3d_producer = cfg.get<std::string>("Tensor3DProducer","");
      auto output_producer   = cfg.get<std::string>("OutputProducer","");
      if(!tensor3d_producer.empty()) {
        _tensor3d_producer_v.push_back(tensor3d_producer);
        _output_producer_v.push_back(output_producer);
      }
    }

    if(_output_producer_v.empty()) {
      _output_producer_v.resize(_tensor3d_producer_v.size(),"");
    }
    else if(_output_producer_v.size() != _tensor3d_producer_v.size()) {
      LARCV_CRITICAL() << "Tensor3DProducer and OutputProducer must have the same array length!" << std::endl;
      throw larbys();
    }
  }

  void BlurTensor3D::configure(const PSet& cfg)
  {
    configure_labels(cfg);
    _sigma_v   = cfg.get<std::vector<double> >("SigmaXYZ");
    _numvox_v  = cfg.get<std::vector<size_t> >("NumVoxelsXYZ");
    _normalize = cfg.get<bool>("Normalize", true);
    if (_sigma_v.size() != 3) {
      LARCV_CRITICAL() << "SigmaXYZ parameter must be length 3 floating point vector!" << std::endl;
      throw larbys();
    }
    if (_numvox_v.size() != 3) {
      LARCV_CRITICAL() << "NumVoxelsXYZ parameter must be length 3 unsigned integer vector!" << std::endl;
      throw larbys();
    }

    // create smearing matrix
    _scale_vvv.resize(_numvox_v[0] + 1);
    for (auto& scale_vv : _scale_vvv) {
      scale_vv.resize(_numvox_v[1] + 1);
      for (auto& scale_v : scale_vv) {
        scale_v.resize(_numvox_v[2] + 1, 0.);
      }
    }
  }

  void BlurTensor3D::initialize()
  {}

  bool BlurTensor3D::process(IOManager& mgr)
  {

    for (size_t producer_index = 0; producer_index < _tensor3d_producer_v.size(); ++producer_index) {

      auto const& tensor3d_producer = _tensor3d_producer_v[producer_index];
      auto const& output_producer   = _output_producer_v[producer_index];

      auto const& ev_tensor3d = mgr.get_data<larcv::EventSparseTensor3D>(tensor3d_producer);
      auto& ev_output = mgr.get_data<larcv::EventSparseTensor3D>(output_producer);

      if(ev_output.meta().valid()) {
        static bool one_time_warning=true;
        if(_output_producer_v[producer_index].empty()) {
          LARCV_CRITICAL() << "Over-writing existing EventSparseTensor3D data for label "
          << output_producer << std::endl;
          throw larbys();
        }
        else if(one_time_warning) {
          LARCV_WARNING() << "Output EventSparseTensor3D producer " << output_producer
          << " already holding valid data will be over-written!" << std::endl;
          one_time_warning = false;
        }
      }

      auto const& meta = ev_tensor3d.meta();
      double scale_sum = 0.;
      for (size_t xshift = 0; xshift <= _numvox_v[0]; ++xshift) {
        for (size_t yshift = 0; yshift <= _numvox_v[1]; ++yshift) {
          for (size_t zshift = 0; zshift <= _numvox_v[2]; ++zshift) {

            double val = exp( - pow(xshift * meta.size_voxel_x(), 2) / (2. * _sigma_v[0])
                              - pow(yshift * meta.size_voxel_y(), 2) / (2. * _sigma_v[1])
                              - pow(zshift * meta.size_voxel_z(), 2) / (2. * _sigma_v[2]) );
            _scale_vvv[xshift][yshift][zshift] = val;
            scale_sum += val;
          }
        }
      }
      if (!_normalize) scale_sum = 1.;

      larcv::VoxelSet res_data;
      for (auto const& vox : ev_tensor3d.as_vector()) {

        auto const pos = meta.position(vox.id());

        double xpos = pos.x - _numvox_v[0] * meta.size_voxel_x();
        double xmax = pos.x + (_numvox_v[0] + 0.5) * meta.size_voxel_x();
        int x_ctr = 0;
        while (xpos < xmax) {
          double ypos = pos.y - _numvox_v[1] * meta.size_voxel_y();
          double ymax = pos.y + (_numvox_v[1] + 0.5) * meta.size_voxel_y();
          int y_ctr = 0;
          while (ypos < ymax) {
            double zpos = pos.z - _numvox_v[2] * meta.size_voxel_z();
            double zmax = pos.z + (_numvox_v[2] + 0.5) * meta.size_voxel_z();
            int z_ctr = 0;
            while (zpos < zmax) {

              auto const id = meta.id(xpos, ypos, zpos);
              if (id != kINVALID_VOXELID) {

                int xindex = std::abs(((int)(_numvox_v[0])) - x_ctr);
                int yindex = std::abs(((int)(_numvox_v[1])) - y_ctr);
                int zindex = std::abs(((int)(_numvox_v[2])) - z_ctr);

                float scale_factor = _scale_vvv[xindex][yindex][zindex];

                res_data.emplace(id, vox.value() * scale_factor / scale_sum, true);
              }
              zpos += meta.size_voxel_z();
              ++z_ctr;
            }
            ypos += meta.size_voxel_y();
            ++y_ctr;
          }
          xpos += meta.size_voxel_x();
          ++x_ctr;
        }
      }

      ev_output.emplace(std::move(res_data), meta);

    }
    return true;

  }

  void BlurTensor3D::finalize()
  {}

}
#endif

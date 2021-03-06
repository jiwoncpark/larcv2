#ifndef __BBOXFROMCLUSTERVOXEL3D_CXX__
#define __BBOXFROMCLUSTERVOXEL3D_CXX__

#include "BBoxFromClusterVoxel3D.h"
#include "larcv/core/DataFormat/EventParticle.h"
#include "larcv/core/DataFormat/EventVoxel3D.h"
namespace larcv {

  static BBoxFromClusterVoxel3DProcessFactory
  __global_BBoxFromClusterVoxel3DProcessFactory__;

  BBoxFromClusterVoxel3D::BBoxFromClusterVoxel3D(const std::string name)
    : ProcessBase(name) {}

  void BBoxFromClusterVoxel3D::configure(const PSet& cfg) {
    _voxel3d_producer = cfg.get<std::string>("ClusterVoxel3DProducer");
    _particle_producer = cfg.get<std::string>("ParticleProducer");
    _output_producer = _particle_producer + "_bbox";
    _output_producer = cfg.get<std::string>("OutputProducer", _output_producer);
    _voxel_threshold = cfg.get<float>("Threshold", 0.0);
    _xy = cfg.get<int>("XY", 1);
    _yz = cfg.get<int>("YZ", 1);
    _zx = cfg.get<int>("ZX", 1);
  }

  void BBoxFromClusterVoxel3D::initialize() {}

  bool BBoxFromClusterVoxel3D::process(IOManager& mgr) {
    auto const& ev_voxel3d =
      mgr.get_data<larcv::EventClusterVoxel3D>(_voxel3d_producer);
    auto const& meta3d = ev_voxel3d.meta();

    auto const& ev_part_input =
      mgr.get_data<larcv::EventParticle>(_particle_producer);

    if (ev_voxel3d.as_vector().size() < ev_part_input.as_vector().size()) {
      LARCV_CRITICAL() << "Can not match " << ev_voxel3d.as_vector().size()
                       << " particles to " << ev_part_input.as_vector().size()
                       << " cluster3d objects." << std::endl;
      throw larbys();
    }

    std::vector<larcv::Particle> particle_v;

    for (size_t i_part = 0; i_part < ev_part_input.as_vector().size(); i_part++) {
      auto new_particle = ev_part_input.as_vector().at(i_part);

      // Get the set of voxels matched to this particle, and find the
      // min/max in each coordinate.
      auto const& voxel_v = ev_voxel3d.as_vector().at(i_part);
      // BBox3D _3d_box;
      float x_min = 99999, y_min = 99999, z_min = 99999;
      float x_max = -99999, y_max = -99999, z_max = -99999;
      for (auto const& vox : voxel_v.as_vector()) {
        if (vox.value() > _voxel_threshold) {
          auto const pos = meta3d.position(vox.id());
          if (pos.x < x_min) x_min = pos.x;
          if (pos.y < y_min) y_min = pos.y;
          if (pos.z < z_min) z_min = pos.z;
          if (pos.x > x_max) x_max = pos.x;
          if (pos.y > y_max) y_max = pos.y;
          if (pos.z > z_max) z_max = pos.z;
        }
      }
      // Check to make sure values were actually filled:
      if (x_max < x_min || y_max < y_min || z_max < z_min) {
        particle_v.emplace_back(std::move(new_particle));
        continue;
      }

      // Now create the 3D and 2D bounding boxes:
      new_particle.boundingbox_3d(BBox3D(x_min, y_min, z_min, x_max, y_max, z_max));

      // XY projection:
      if (_xy) {
        new_particle.boundingbox_2d(BBox2D(x_min, y_min, x_max, y_max), 0);
      }
      // YZ projection:
      if (_yz) {
        new_particle.boundingbox_2d(BBox2D(y_min, z_min, y_max, z_max), 1);
      }
      // ZX projection:
      if (_zx) {
        new_particle.boundingbox_2d(BBox2D(z_min, x_min, z_max, x_max), 2);
      }

      particle_v.emplace_back(std::move(new_particle));
    }

    auto& ev_part_output = mgr.get_data<larcv::EventParticle>(_output_producer);
    ev_part_output.emplace(std::move(particle_v));

    return true;
  }

  void BBoxFromClusterVoxel3D::finalize() {}
}
#endif

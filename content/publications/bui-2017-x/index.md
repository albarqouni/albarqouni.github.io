---
title: 'X-Ray PoseNet: 6 DoF pose estimation for mobile X-Ray devices'
date: '2017-01-01'
draft: false
authors:
- mai-bui
- shadi-albarqouni
- Michael Schrapp
- nassir-navab
- Slobodan Ilic
publication_types:
- paper-conference
publication:
  name: 2017 IEEE Winter Conference on Applications of Computer Vision (WACV)
venue: wacv
doi: 10.1109/wacv.2017.120
abstract: Precise reconstruction of 3D volumes from X-ray projections requires precisely pre-calibrated systems where accurate knowledge of the systems geometric parameters is known ahead. However, when dealing with mobile X-ray devices such calibration parameters are unknown. Joint estimation of the systems calibration parameters and 3d reconstruction is a heavily unconstrained problem, especially when the projections are arbitrary. In industrial applications, that we target here, nominal CAD models of the object to be reconstructed are usually available. We rely on this prior information and employ Deep Learning to learn the mapping between simulated X-ray projections and its pose. Moreover, we introduce the reconstruction loss in addition to the pose loss to further improve the reconstruction quality. Finally, we demonstrate the generalization capabilities of our method in case where poses can be learned on instances of the objects belonging to the same class, allowing pose estimation
  of unseen objects from the same category, thus eliminating the need for the actual CAD model. We performed exhaustive evaluation demonstrating the quality of our results on both synthetic and real data.
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags:
- Computer Vision
- Radiology
- Deep Learning
- Pose Estimation
featured: false
links:
- type: pdf
  url: https://ieeexplore.ieee.org/abstract/document/7926703/
slidev: ''
hugoblox:
  ids:
    doi: 10.1109/wacv.2017.120
sync:
  source: legacy
  openalex: W2613277324
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2472-6737
  source_id: S4393918690
  source_type: conference
  citations: 27
---

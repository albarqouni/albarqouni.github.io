---
title: Scale-Space Autoencoders for Unsupervised Anomaly Segmentation in Brain MRI
date: '2020-01-01'
draft: false
authors:
- christoph-baur
- benedikt-wiestler
- shadi-albarqouni
- nassir-navab
publication_types:
- paper-conference
publication:
  name: Medical Image Computing and Computer Assisted Intervention – MICCAI 2020, Lecture Notes in Computer Science
venue: miccai
doi: 10.1007/978-3-030-59719-1_54
abstract: Brain pathologies can vary greatly in size and shape, ranging from few pixels (i.e. MS lesions) to large, space-occupying tumors. Recently proposed Autoencoder-based methods for unsupervised anomaly segmentation in brain MRI have shown promising performance, but face difficulties in modeling distributions with high fidelity, which is crucial for accurate delineation of particularly small lesions. Here, similar to these previous works, we model the distribution of healthy brain MRI to localize pathologies from erroneous reconstructions. However, to achieve improved reconstruction fidelity at higher resolutions, we learn to compress and reconstruct different frequency bands of healthy brain MRI using the laplacian pyramid. In a range of experiments comparing our method to different State-of-the-Art approaches on three different brain MR datasets with MS lesions and tumors, we show improved anomaly segmentation performance and the general capability to obtain much more crisp reconstructions
  of input data at native resolution. The modeling of the laplacian pyramid further enables the delineation and aggregation of lesions at multiple scales, which allows to effectively cope with different pathologies and lesion sizes using a single model.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/2006.12852
slidev: ''
hugoblox:
  ids:
    doi: 10.1007/978-3-030-59719-1_54
    arxiv: '2006.12852'
sync:
  source: legacy
  openalex: W3036829886
  scholar: ''
  locked:
  - publication
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 0302-9743
  - 1611-3349
  source_id: S106296714
  source_type: book series
  citations: 39
  teaser: pdf:https://arxiv.org/pdf/2006.12852
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

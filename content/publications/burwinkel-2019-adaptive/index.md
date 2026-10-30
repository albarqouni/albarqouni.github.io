---
title: Adaptive image-feature learning for disease classification using inductive graph networks
date: '2019-01-01'
draft: false
authors:
- Hendrik Burwinkel
- anees-kazi
- Gerome Vivar
- shadi-albarqouni
- Guillaume Zahnd
- nassir-navab
- Seyed-Ahmad Ahmadi
publication_types:
- paper-conference
publication:
  name: Medical Image Computing and Computer Assisted Intervention – MICCAI 2019, Lecture Notes in Computer Science
venue: miccai
doi: 10.1007/978-3-030-32226-7_71
abstract: Recently, Geometric Deep Learning (GDL) has been introduced as a novel and versatile framework for computer-aided disease classification. GDL uses patient meta-information such as age and gender to model patient cohort relations in a graph structure. Concepts from graph signal processing are leveraged to learn the optimal mapping of multi-modal features, e.g. from images to disease classes. Related studies so far have considered image features that are extracted in a pre-processing step. We hypothesize that such an approach prevents the network from optimizing feature representations towards achieving the best performance in the graph network. We propose a new network architecture that exploits an inductive end-to-end learning approach for disease classification, where filters from both the CNN and the graph are trained jointly. We validate this architecture against state-of-the-art inductive graph networks and demonstrate significantly improved classification scores on a modified
  MNIST toy dataset, as well as comparable classification results with higher stability on a chest X-ray image dataset. Additionally, we explain how the structural information of the graph affects both the image filters and the feature learning.
themes:
- computational-imaging
projects: []
datasets: []
tags:
- Deep Learning
- Medical Imaging
- Radiology
- Prior Knowledge
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/1905.03036
slidev: ''
hugoblox:
  ids:
    doi: 10.1007/978-3-030-32226-7_71
    arxiv: '1905.03036'
sync:
  source: legacy
  openalex: W2980174706
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
  citations: 16
  teaser: pdf:https://arxiv.org/pdf/1905.03036
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

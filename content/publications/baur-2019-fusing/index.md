---
title: Fusing unsupervised and supervised deep learning for white matter lesion segmentation
date: '2018-12-13'
draft: false
authors:
- christoph-baur
- benedikt-wiestler
- shadi-albarqouni
- nassir-navab
publication_types:
- paper-conference
publication:
  name: International Conference on Medical Imaging with Deep Learning
venue: midl
doi: ''
abstract: Unsupervised Deep Learning for Medical Image Analysis is increasingly gaining attention, since it relieves from the need for annotating training data. Recently, deep generative models and representation learning have lead to new, exciting ways for unsupervised detection and delineation of biomarkers in medical images, such as lesions in brain MR. Yet, Supervised Deep Learning methods usually still perform better in these tasks, due to an optimization for explicit objectives. We aim to combine the advantages of both worlds into a novel framework for learning from both labeled & unlabeled data, and validate our method on the challenging task of White Matter lesion segmentation in brain MR images. The proposed framework relies on modeling normality with deep representation learning for Unsupervised Anomaly Detection, which in turn provides optimization targets for training a supervised segmentation model from unlabeled data. In our experiments we successfully use the method in a Semi-supervised
  setting for tackling domain shift, a well known problem in MR image analysis, showing dramatically improved generalization. Additionally, our experiments reveal that in a completely Unsupervised setting, the proposed pipeline even outperforms the Deep Learning driven anomaly detection that provides the optimization targets.
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags:
- Medical Imaging
- Deep Learning
- Radiology
- Generative Adversarial Networks
- Anomaly Detection
featured: false
links:
- type: pdf
  url: http://proceedings.mlr.press/v102/baur19a/baur19a.pdf
- type: source
  url: http://proceedings.mlr.press/v102/baur19a/baur19a.pdf
  name: Publisher
- type: source
  url: https://proceedings.mlr.press/v102/baur19a.html
  name: Publisher
slidev: ''
hugoblox: {}
sync:
  source: legacy
  openalex: W2965587354
  scholar: CPuApzoAAAAJ:1yQoGdGgb4wC
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn: []
  source_id: ''
  source_type: ''
  citations: 44
  teaser: pdf:http://proceedings.mlr.press/v102/baur19a/baur19a.pdf
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

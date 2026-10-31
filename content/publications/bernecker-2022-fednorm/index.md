---
title: 'FedNorm: Modality-Based Normalization in Federated Learning for Multi-Modal Liver Segmentation'
date: '2022-01-01'
draft: false
authors:
- tobias-bernecker
- Annette Peters
- Christopher L Schlett
- Fabian Bamberg
- Fabian Theis
- daniel-rueckert
- jakob-weiss
- shadi-albarqouni
publication_types:
- preprint
publication:
  name: arXiv (Cornell University)
venue: arxiv
doi: 10.48550/arxiv.2205.11096
abstract: Given the high incidence and effective treatment options for liver diseases, they are of great socioeconomic importance. One of the most common methods for analyzing CT and MRI images for diagnosis and follow-up treatment is liver segmentation. Recent advances in deep learning have demonstrated encouraging results for automatic liver segmentation. Despite this, their success depends primarily on the availability of an annotated database, which is often not available because of privacy concerns. Federated Learning has been recently proposed as a solution to alleviate these challenges by training a shared global model on distributed clients without access to their local databases. Nevertheless, Federated Learning does not perform well when it is trained on a high degree of heterogeneity of image data due to multi-modal imaging, such as CT and MRI, and multiple scanner types. To this end, we propose Fednorm and its extension \fednormp, two Federated Learning algorithms that use a
  modality-based normalization technique. Specifically, Fednorm normalizes the features on a client-level, while Fednorm+ employs the modality information of single slices in the feature normalization. Our methods were validated using 428 patients from six publicly available databases and compared to state-of-the-art Federated Learning algorithms and baseline models in heterogeneous settings (multi-institutional, multi-modal data). The experimental results demonstrate that our methods show an overall acceptable performance, achieve Dice per patient scores up to 0.961, consistently outperform locally trained models, and are on par or slightly better than centralized models.
themes:
- computational-imaging
- federated-learning
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/2205.11096
hugoblox:
  ids:
    doi: 10.48550/arxiv.2205.11096
    arxiv: '2205.11096'
sync:
  source: legacy
  openalex: W4281478539
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2331-8422
  source_id: S4306400194
  source_type: repository
  citations: 17
  teaser: pdf:https://arxiv.org/pdf/2205.11096
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

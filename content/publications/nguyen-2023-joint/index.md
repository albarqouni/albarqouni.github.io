---
title: Joint self-supervised image-volume representation learning with intra-inter contrastive clustering
date: '2023-01-01'
draft: false
authors:
- Duy M. H. Nguyen
- Hoang Nguyen
- Truong TN Mai
- Tri Cao
- Binh T Nguyen
- Nhat Ho
- Paul Swoboda
- shadi-albarqouni
- Pengtao Xie
- daniel-sonntag
publication_types:
- paper-conference
publication:
  name: Proceedings of the AAAI Conference on Artificial Intelligence
venue: aaai
doi: 10.1609/aaai.v37i12.26687
abstract: 'Collecting large-scale medical datasets with fully annotated samples for training of deep networks is prohibitively expensive, especially for 3D volume data. Recent breakthroughs in self-supervised learning (SSL) offer the ability to overcome the lack of labeled training samples by learning feature representations from unlabeled data. However, most current SSL techniques in the medical field have been designed for either 2D images or 3D volumes. In practice, this restricts the capability to fully leverage unlabeled data from numerous sources, which may include both 2D and 3D data. Additionally, the use of these pre-trained networks is constrained to downstream tasks with compatible data dimensions.

  In this paper, we propose a novel framework for unsupervised joint learning on 2D and 3D data modalities. Given a set of 2D images or 2D slices extracted from 3D volumes, we construct an SSL task based on a 2D contrastive clustering problem for distinct classes. The 3D volumes are exploited by computing vectored embedding at each slice and then assembling a holistic feature through deformable self-attention mechanisms in Transformer, allowing incorporating long-range dependencies between slices inside 3D volumes. These holistic features are further utilized to define a novel 3D clustering agreement-based SSL task and masking embedding prediction inspired by pre-trained language models. Experiments on downstream tasks, such as 3D brain segmentation, lung nodule detection, 3D heart structures segmentation, and abnormal chest X-ray detection, demonstrate the effectiveness of our joint 2D and 3D SSL approach. We improve plain 2D Deep-ClusterV2 and SwAV by a significant margin and also surpass
  various modern 2D and 3D SSL approaches.'
themes:
- computational-imaging
projects: []
datasets: []
tags:
- Deep Learning
- Medical Imaging
- Self-Supervised Learning
featured: true
links:
- type: pdf
  url: https://arxiv.org/pdf/2212.01893.pdf
hugoblox:
  ids:
    doi: 10.1609/aaai.v37i12.26687
sync:
  source: legacy
  openalex: ''
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: crossref
  issn:
  - 2374-3468
  - 2159-5399
  source_id: ''
  source_type: ''
  merged:
  - nguyen-2022-joint
image:
  caption: ''
  focal_point: Smart
---

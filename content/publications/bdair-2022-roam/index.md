---
title: 'ROAM: Random layer mixup for semi-supervised learning in medical images'
date: '2022-01-01'
draft: false
authors:
- tariq-bdair
- benedikt-wiestler
- nassir-navab
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: IET Image Processing
venue: ''
doi: 10.1049/ipr2.12511
abstract: Abstract Medical image segmentation is one of the major challenges addressed by machine learning methods. However, these methods profoundly depend on a large amount of annotated data, which is expensive and time‐consuming. Semi‐supervised learning (SSL) approaches this by leveraging an abundant amount of unlabeled data. Recently, MixUp regularizer has been introduced to SSL methods by augmenting the model with new data points through linear interpolation at the input space. While this provides the model with new data, it is limited and may lead to inconsistent soft labels. It is argued that the linear interpolation at different representations provides the network with novel training signals and overcomes the inconsistency of the soft labels. This paper proposes ROAM as an SSL method that explores the manifold and performs linear interpolation on randomly selected layers to generate virtual data that has never been seen before, which encourages the network to be less confident
  for interpolated points. Hence it avoids overfitting, enhances the generalization, and shows less sensitivity to the domain shift. Extensive experiments are conducted on publicl datasets on whole‐brain and lung segmentation. ROAM achieves state‐of‐the‐art results in fully supervised (89.5%) and semi‐supervised (87.0%) settings with relative improvements up to 2.40% and 16.50%, respectively.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1049/ipr2.12511
slidev: ''
hugoblox:
  ids:
    doi: 10.1049/ipr2.12511
sync:
  source: legacy
  openalex: W4225415191
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 1751-9659
  - 1751-9667
  source_id: S83215360
  source_type: journal
  citations: 11
  merged:
  - bdair-2020-roam
image:
  caption: ''
  focal_point: Smart
---

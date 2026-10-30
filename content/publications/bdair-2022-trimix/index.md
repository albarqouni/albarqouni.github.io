---
title: 'TriMix: Virtual embeddings and self-consistency for self-supervised learning'
date: '2022-01-01'
draft: false
authors:
- tariq-bdair
- Hossam Abdelhamid
- nassir-navab
- shadi-albarqouni
publication_types:
- preprint
publication:
  name: arXiv (Cornell University)
venue: arxiv
doi: 10.48550/arxiv.2206.06023
abstract: Self-supervised Learning (SSL) has recently gained much attention due to the high cost and data limitation in the training of supervised learning models. The current paradigm in the SSL is to utilize data augmentation at the input space to create different views of the same images and train a model to maximize the representations between similar images and minimize them for different ones. While this approach achieves state-of-the-art (SOTA) results in various downstream tasks, it still lakes the opportunity to investigate the latent space augmentation. This paper proposes TriMix, a novel concept for SSL that generates virtual embeddings through linear interpolation of the data, thus providing the model with novel representations. Our strategy focuses on training the model to extract the original embeddings from virtual ones, hence, better representation learning. Additionally, we propose a self-consistency term that improves the consistency between the virtual and actual embeddings.
  We validate TriMix on eight benchmark datasets consisting of natural and medical images with an improvement of 2.71% and 0.41% better than the second-best models for both data types. Further, our approach outperformed the current methods in semi-supervised learning, particularly in low data regimes. Besides, our pre-trained models showed better transfer to other datasets.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/2206.06023
slidev: ''
hugoblox:
  ids:
    doi: 10.48550/arxiv.2206.06023
    arxiv: '2206.06023'
sync:
  source: legacy
  openalex: W4283075640
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2331-8422
  source_id: S4306400194
  source_type: repository
  citations: 0
  teaser: pdf:https://arxiv.org/pdf/2206.06023
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

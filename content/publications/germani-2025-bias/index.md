---
title: Bias and generalizability of foundation models across datasets in breast mammography
date: '2025-01-01'
draft: false
authors:
- elodie-germani
- ilayda-tuerk
- Fatima Zeineddine
- charbel-mourad
- shadi-albarqouni
publication_types:
- paper-conference
publication:
  name: International conference on medical image computing and computer-assisted intervention
venue: miccai
doi: 10.48550/arxiv.2505.10579
abstract: Over the past decades, computer-aided diagnosis tools for breast cancer have been developed to enhance screening procedures, yet their clinical adoption remains challenged by data variability and inherent biases. Although foundation models (FMs) have recently demonstrated impressive generalizability and transfer learning capabilities by leveraging vast and diverse datasets, their performance can be undermined by spurious correlations that arise from variations in image quality, labeling uncertainty, and sensitive patient attributes. In this work, we explore the fairness and bias of FMs for breast mammography classification by leveraging a large pool of datasets from diverse sources-including data from underrepresented regions and an in-house dataset. Our extensive experiments show that while modality-specific pre-training of FMs enhances performance, classifiers trained on features from individual datasets fail to generalize across domains. Aggregating datasets improves overall
  performance, yet does not fully mitigate biases, leading to significant disparities across under-represented subgroups such as extreme breast densities and age groups. Furthermore, while domain-adaptation strategies can reduce these disparities, they often incur a performance trade-off. In contrast, fairness-aware techniques yield more stable and equitable performance across subgroups. These findings underscore the necessity of incorporating rigorous fairness evaluations and mitigation strategies into FM-based models to foster inclusive and generalizable AI.
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags: []
featured: true
links:
- type: pdf
  url: https://arxiv.org/pdf/2505.10579
slidev: ''
hugoblox:
  ids:
    doi: 10.48550/arxiv.2505.10579
    arxiv: '2505.10579'
sync:
  source: legacy
  openalex: W4417299760
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2331-8422
  source_id: S4306400194
  source_type: repository
  citations: 1
image:
  caption: ''
  focal_point: Smart
---

---
title: The OOD Blind Spot of Unsupervised Anomaly Detection
date: '2021-01-01'
draft: false
authors:
- matthaeus-heer
- Janis Postels
- Xiaoran Chen
- Ender Konukoglu
- shadi-albarqouni
publication_types:
- paper-conference
publication:
  name: Medical Imaging with Deep Learning
venue: midl
doi: ''
abstract: Deep unsupervised generative models are regarded as a promising alternative to supervised counterparts in the field of MRI-based lesion detection. They denote a principled approach for detecting unseen types of anomalies without relying on large amounts of expensive ground truth annotations. To this end, deep generative models are trained exclusively on data from healthy patients and detect lesions as Out-of-Distribution (OOD) data at test time (ie low likelihood). While this is a promising way of bypassing the need for costly annotations, this work demonstrates that it also renders this widely used unsupervised anomaly detection approach particularly vulnerable to non-lesion-based OOD data (eg data from different sensors). Since models are likely to be exposed to such OOD data in production, it is crucial to employ safety mechanisms to filter for such samples and run inference only on input for which the model is able to provide reliable results. We first show extensively that
  conventional, unsupervised anomaly detection mechanisms fail when being presented with true OOD data. Secondly, we apply prior knowledge to disentangle lesion-based OOD from their non-lesion-based counterparts.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: source
  url: https://proceedings.mlr.press/v143/heer21a.html
  name: Publisher
hugoblox: {}
sync:
  source: legacy
  openalex: ''
  scholar: CPuApzoAAAAJ:Dip1O2bNi0gC
  locked: []
  citations: 22
image:
  caption: ''
  focal_point: Smart
---

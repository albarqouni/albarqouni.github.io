---
title: Federated disentangled representation learning for unsupervised brain anomaly detection
date: '2022-10-01'
draft: false
authors:
- cosmin-bercea
- benedikt-wiestler
- daniel-rueckert
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: Nature Machine Intelligence
venue: nature-mi
doi: 10.1038/s42256-022-00515-2
abstract: Recent advances in Deep Learning (DL) and the increased use of brain MRI have provided a great opportunity and interest in automated anomaly segmentation to support human interpretation and improve clinical workflow. However, medical imaging must be curated by trained clinicians, which is time-consuming and expensive. Further, data is often scattered across multiple institutions, with privacy regulations limiting its access. Here, we present FedDis (Federated Disentangled representation learning for unsupervised brain pathology segmentation) to collaboratively train an unsupervised deep convolutional neural network on 1532 healthy MR scans from four different institutions, and evaluate its performance in identifying abnormal brain MRIs including multiple sclerosis (MS), vascular lesions, low-grade tumors (LGG), and high-grade tumors/glioblastoma (HGG/GB) on a total of ~538 scans from 6 different institutions and datasets. To mitigate the statistical heterogeneity between the different
  institutes, we disentangle the parameter space into global, i.e., shape and local, i.e., appearance. We train the shape parameters jointly from four institutes to learn a global model of the healthy anatomical brain structure. The appearance parameters are trained locally on every institute and allow for personalization of the global domain-invariant features with client-specific information, such as scanner or acquisition parameter. We have shown that our collaborative approach, FedDis, improves anomaly segmentation results by 99.74% for MS, 83.33% for vascular lesions,and 40.45% for tumors over locally trained models without the need for annotations or sharing private local data. We found out that FedDis is especially beneficial for clients that share both healthy and anomaly data coming from the same institute, improving their local anomaly detection performance by up to 227% for MS lesions and 77% for brain tumors.
themes:
- computational-imaging
- federated-learning
projects:
- federated-learning
- feddis
datasets: []
tags:
- Medical Imaging
- Deep Learning
- Federated Learning
featured: true
featured_pin: true
links:
- type: pdf
  url: https://doi.org/10.1038/s42256-022-00515-2
- name: URL
  url: https://doi.org/10.1038/s42256-022-00515-2
  icon: hero/link
hugoblox:
  ids:
    doi: 10.1038/s42256-022-00515-2
sync:
  source: legacy
  openalex: W4293237729
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2522-5839
  source_id: S2912241403
  source_type: journal
  citations: 99
  merged:
  - bercea-2021-federated
  - cite-key
image:
  caption: ''
  focal_point: Smart
---

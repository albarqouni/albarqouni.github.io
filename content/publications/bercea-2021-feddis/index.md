---
title: 'FedDis: Disentangled Federated Learning for Unsupervised Brain Pathology Segmentation'
date: '2021-01-01'
draft: false
authors:
- cosmin-bercea
- benedikt-wiestler
- daniel-rueckert
- shadi-albarqouni
publication_types:
- preprint
publication:
  name: arXiv (Cornell University)
venue: arxiv
doi: 10.48550/arxiv.2103.03705
abstract: In recent years, data-driven machine learning (ML) methods have revolutionized the computer vision community by providing novel efficient solutions to many unsolved (medical) image analysis problems. However, due to the increasing privacy concerns and data fragmentation on many different sites, existing medical data are not fully utilized, thus limiting the potential of ML. Federated learning (FL) enables multiple parties to collaboratively train a ML model without exchanging local data. However, data heterogeneity (non-IID) among the distributed clients is yet a challenge. To this end, we propose a novel federated method, denoted Federated Disentanglement (FedDis), to disentangle the parameter space into shape and appearance, and only share the shape parameter with the clients. FedDis is based on the assumption that the anatomical structure in brain MRI images is similar across multiple institutions, and sharing the shape knowledge would be beneficial in anomaly detection. In
  this paper, we leverage healthy brain scans of 623 subjects from multiple sites with real data (OASIS, ADNI) in a privacy-preserving fashion to learn a model of normal anatomy, that allows to segment abnormal structures. We demonstrate a superior performance of FedDis on real pathological databases containing 109 subjects; two publicly available MS Lesions (MSLUB, MSISBI), and an in-house database with MS and Glioblastoma (MSI and GBI). FedDis achieved an average dice performance of 0.38, outperforming the state-of-the-art (SOTA) auto-encoder by 42% and the SOTA federated method by 11%. Further, we illustrate that FedDis learns a shape embedding that is orthogonal to the appearance and consistent under different intensity augmentations.
themes:
- computational-imaging
- federated-learning
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/2103.03705
slidev: ''
hugoblox:
  ids:
    doi: 10.48550/arxiv.2103.03705
    arxiv: '2103.03705'
sync:
  source: legacy
  openalex: W3134472684
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2331-8422
  source_id: S4306400194
  source_type: repository
  citations: 30
  teaser: pdf:https://arxiv.org/pdf/2103.03705
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

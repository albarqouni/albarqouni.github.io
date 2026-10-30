---
title: Semi-Supervised Federated Peer Learning for Skin Lesion Classification
date: '2022-01-01'
draft: false
authors:
- tariq-bdair
- nassir-navab
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: Machine Learning for Biomedical Imaging
venue: melba
doi: 10.59275/j.melba.2022-8g82
abstract: Globally, Skin carcinoma is among the most lethal diseases. Millions of people are diagnosed with this cancer every year. Sill, early detection can decrease the medication cost and mortality rate substantially. The recent improvement in automated cancer classification using deep learning methods has reached a human-level performance requiring a large amount of annotated data assembled in one location, yet, finding such conditions usually is not feasible. Recently, federated learning (FL) has been proposed to train decentralized models in a privacy-preserved fashion depending on labeled data at the client-side, which is usually not available and costly. To address this, we propose FedPerl, a semi-supervised federated learning method. Our method is inspired by peer learning from educational psychology and ensemble averaging from committee machines. FedPerl builds communities based on clients' similarities. Then it encourages communities' members to learn from each other to generate
  more accurate pseudo labels for the unlabeled data. We also proposed the peer anonymization (PA) technique to anonymize clients. As a core component of our method, PA is orthogonal to other methods without additional complexity, and reduces the communication cost while enhances performance. Finally, we propose a dynamic peer learning policy that controls the learning stream to avoid any degradation in the performance, especially for the individual clients. Our experimental setup consists of 71,000 skin lesion images collected from 5 publicly available datasets. We test our method in four different scenarios in SSFL. With few annotated data, FedPerl is on par with a state-of-the-art method in skin lesion classification in the standard setup while outperforming SSFLs and the baselines by 1.8% and 15.8%, respectively. Also, it generalizes better to an unseen client while being less sensitive to noisy ones.
themes:
- computational-imaging
- federated-learning
projects: []
datasets: []
tags: []
featured: false
links:
- name: URL
  url: https://melba-journal.org/papers/2022:011.html
  icon: hero/link
slidev: ''
hugoblox:
  ids:
    doi: 10.59275/j.melba.2022-8g82
sync:
  source: legacy
  openalex: ''
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: crossref
  issn:
  - 2766-905X
  source_id: ''
  source_type: ''
image:
  caption: ''
  focal_point: Smart
---

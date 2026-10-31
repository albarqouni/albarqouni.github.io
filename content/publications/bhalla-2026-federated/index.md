---
title: Federated CT foundation models for multi-center detection of lymph node metastasis in pancreatic cancer
date: '2026-04-09'
draft: false
authors:
- parinishtha-bhalla
- david-gaviria
- patrick-kupczyk
- Ali Seif Amir Hosseini
- Lena Conradi
- Uli Fehrenbach
- Matthaeus Felsenstein
- Dou Ma
- alexander-semaan
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: Scientific Reports
venue: sci-rep
doi: 10.1038/s41598-026-47631-2
abstract: Pancreatic ductal adenocarcinoma (PDAC) remains one of the most lethal malignancies, with prognosis strongly influenced by the presence of lymph node metastasis (LNM). However, preoperative LNM assessment from computed tomography (CT) is limited by low sensitivity, high inter-observer variability, and substantial heterogeneity across imaging protocols. This retrospective multi-center study (546 patients from three institutions) introduces a privacy-preserving deep learning framework that integrates large-scale CT foundation model pre-training with heterogeneity-aware federated optimization to improve LNM detection in PDAC. A CT Vision Foundation Model, pre-trained on 148,000 volumetric CT scans using contrastive self-supervised learning, is fine-tuned to generate transferable 3D representations for patient-level LNM classification. To enable decentralized model training while mitigating inter-institutional variability, we extend federated aggregation to jointly account for label-distribution
  discrepancies and representation-level divergence across clients. The centralized model achieved a balanced accuracy of 0.601 and a diagnostic odds ratio (DOR) of 3.45, outperforming classical machine learning baselines and prior PDAC LNM approaches. Under federated settings, the proposed heterogeneity-aware strategy consistently outperformed standard FedAvg, recovering a substantial proportion of the centralized model's performance while preserving strict data privacy. In particular, it improved balanced accuracy by 12.6% over FedAvg and demonstrated superior discriminative ability across all participating cohorts. These findings indicate that combining foundation model pre-training with discrepancy-aware federated learning enhances generalization, robustness, and clinical relevance for multi-center PDAC LNM detection. The proposed framework offers a scalable and privacy-preserving pathway for deploying deep learning models across distributed healthcare systems.
themes:
- computational-imaging
- federated-learning
projects:
- pdac-fl
- federated-learning
datasets: []
tags: []
featured: true
links: []
hugoblox:
  ids:
    doi: 10.1038/s41598-026-47631-2
sync:
  source: legacy
  openalex: W7152401128
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2045-2322
  source_id: S196734849
  source_type: journal
  citations: 2
image:
  caption: ''
  focal_point: Smart
---

---
title: PDAC-CTFM — Scientific Report Paper
summary: This work introduces a privacy-preserving federated deep learning framework for preoperative lymph node metastasis (LNM) detection in pancreatic ductal adenocarcinoma (PDAC). We integrate large-scale CT foundation model pre-training with a heterogeneity-aware federated aggregation strategy to enable…
date: '2026-04-05'
lastmod: '2026-04-10'
repository: https://github.com/albarqounilab/PDAC-CTFM
homepage: ''
language: Python
stars: 0
license: ''
topics: []
code_type: research
course: ''
publications:
- bhalla-2026-federated
themes:
- computational-imaging
- federated-learning
projects:
- pdac-fl
datasets: []
authors:
- shadi-albarqouni
modality: []
sync:
  source: github
  repo: albarqounilab/PDAC-CTFM
  locked:
  - publications
image:
  caption: Teaser figure of the accompanying paper.
  focal_point: Center
---
### Overview

This work introduces a privacy-preserving federated deep learning framework for preoperative lymph node metastasis (LNM) detection in pancreatic ductal adenocarcinoma (PDAC). We integrate large-scale CT foundation model pre-training with a heterogeneity-aware federated aggregation strategy to enable collaborative training across three German institutions without sharing raw patient data.

**Key contributions:**
- Fine-tuning of the [CT Vision Foundation Model (CT-FM)](https://huggingface.co/project-lighter/ct_fm_segresnet) on multi-center PDAC CT data for LNM classification.
- A heterogeneity-aware federated aggregation strategy (PDAC-CTFMOurs) that jointly accounts for label-distribution imbalance and representation-level divergence across clients.
- Multi-center evaluation on 546 patients from three institutions (UKB Bonn, Charité Berlin, UMG Göttingen).

**Main results (aggregated test set):**

| Model | Balanced Acc. | DOR | AUPRC |
|---|---|---|---|
| PDAC-CTFMFedAvg | 0.4607 | 0.2500 | 0.6968 |
| PDAC-CTFMOurs | **0.5866** | **2.1010** | 0.6752 |
| PDAC-CTFMCentral (upper bound) | 0.6010 | 3.4541 | 0.7376 |

Our federated method outperforms all FL baselines (FedAvg, FedDisco, FedBN, FedALA) by **+12.6% balanced accuracy** over FedAvg while preserving data privacy.

### 2. Federated Learning — Proposed Method (Heterogeneity-Aware FedDisco)

Runs PDAC-CTFMOurs with default hyperparameters (*a*=0.1, *b*=0.1, *γ*=10). To sweep hyperparameters, edit the `a_values`, `b_values`, `gamma_values` lists at the bottom of the script:

```python

### Using the code

The repository README covers installation, data, demo data (synthetic), using real data, federated learning setup. See [the repository on GitHub](https://github.com/albarqounilab/PDAC-CTFM#readme) for step-by-step instructions.

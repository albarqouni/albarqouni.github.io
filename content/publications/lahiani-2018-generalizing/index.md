---
title: Generalizing multistain immunohistochemistry tissue segmentation using one-shot color deconvolution deep neural networks
date: '2019-01-01'
draft: false
authors:
- amal-lahiani
- Jacob Gildenblat
- Irina Klaman
- nassir-navab
- Eldad Klaiman
publication_types:
- article-journal
publication:
  name: IET Image Processing
venue: ''
doi: 10.1049/iet-ipr.2018.6513
abstract: A key challenge in cancer immunotherapy biomarker research is quantification of pattern changes in microscopic whole slide images of tumour biopsies. Drug development requires a correlative analysis of various biomarkers. To enable that, tissue slides are manually annotated by pathologists, which is a tedious and error‐prone task. Automation of this annotation process can improve accuracy and consistency while reducing workload and cost. The authors present a deep learning method to automatically segment digitised slide images with multiple stainings into compartments of tumour, healthy tissue, necrosis, and background. The method is based on using a fully convolutional neural network including a colour deconvolution segment learned end‐to‐end and helping the network to converge faster and deal with the dataset staining variability. They evaluate the performance of the proposed method using the F1 score, which is the harmonic mean between precision and recall. They report a testing
  F1 score of 0.88, 0.9, 0.8, and 0.99 for tumour, tissue, necrosis, and background, respectively. They address the task in the context of drug development where multiple stains exist and look into solutions for generalisations over these image populations. They also apply visualisation techniques to help understand the network decisions and gain more trust from pathologists.
themes:
- computational-imaging
- responsible-ai
projects:
- roche-virtual-staining
datasets: []
tags:
- Histology
- Medical Imaging
featured: false
links: []
hugoblox:
  ids:
    doi: 10.1049/iet-ipr.2018.6513
    arxiv: '1805.06958'
sync:
  source: legacy
  openalex: W2964016962
  scholar: ''
  locked:
  - publication_types
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 1751-9659
  - 1751-9667
  source_id: S83215360
  source_type: journal
  citations: 12
  teaser: pdf:https://arxiv.org/pdf/1805.06958
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

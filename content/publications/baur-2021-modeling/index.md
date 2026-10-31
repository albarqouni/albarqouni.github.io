---
title: Modeling Healthy Anatomy with Artificial Intelligence for Unsupervised Anomaly Detection in Brain MRI
date: '2021-01-01'
draft: false
authors:
- christoph-baur
- benedikt-wiestler
- Mark Muehlau
- Claus Zimmer
- nassir-navab
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: 'Radiology: Artificial Intelligence'
venue: radiology-ai
doi: 10.1148/ryai.2021190169
abstract: 'PURPOSE: To develop an unsupervised deep learning model on MR images of normal brain anatomy to automatically detect deviations indicative of pathologic states on abnormal MR images. MATERIALS AND METHODS: In this retrospective study, spatial autoencoders with skip-connections (which can learn to compress and reconstruct data) were leveraged to learn the normal variability of the brain from MR scans of healthy individuals. A total of 100 normal, in-house MR scans were used for training. Subsequently, as the model was unable to reconstruct anomalies well, this characteristic was exploited for detecting and delineating various diseases by computing the difference between the input data and their reconstruction. The unsupervised model was compared with a supervised U-Net- and threshold-based classifier trained on data from 50 patients with multiple sclerosis (in-house dataset) and 50 patients from The Cancer Imaging Archive. Both the unsupervised and supervised U-Net models were
  tested on five different datasets containing MR images of microangiopathy, glioblastoma, and multiple sclerosis. Precision-recall statistics and derivations thereof (mean area under the precision-recall curve, Dice score) were used to quantify lesion detection and segmentation performance. RESULTS: The unsupervised approach outperformed the naive thresholding approach in lesion detection (mean F1 scores ranging from 17% to 62% vs 6.4% to 15% across the five different datasets) and performed similarly to the supervised U-Net (20%-64%) across a variety of pathologic conditions. This outperformance was mostly driven by improved precision compared with the thresholding approach (mean precisions, 15%-59% vs 3.4%-10%). The model was also developed to create an anomaly heatmap display. CONCLUSION: Brain/Brain Stem Computer Aided Diagnosis (CAD), Convolutional Neural Network (CNN), Experimental Investigations, Head/Neck, MR-Imaging, Quantification, Segmentation, Stacked Auto-Encoders, Technology
  Assessment, Tissue Characterization © RSNA, 2021.'
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links: []
hugoblox:
  ids:
    doi: 10.1148/ryai.2021190169
sync:
  source: legacy
  openalex: W3132972512
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 2638-6100
  source_id: S4210219523
  source_type: journal
  citations: 44
image:
  caption: ''
  focal_point: Smart
---

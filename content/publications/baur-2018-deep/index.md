---
title: Deep autoencoding models for unsupervised anomaly segmentation in brain MR images
date: '2019-01-01'
draft: false
authors:
- christoph-baur
- benedikt-wiestler
- shadi-albarqouni
- nassir-navab
publication_types:
- paper-conference
publication:
  name: 'Brainlesion: Glioma, Multiple Sclerosis, Stroke and Traumatic Brain Injuries — BrainLes 2018 workshop @ MICCAI, Lecture Notes in Computer Science'
venue: ''
doi: 10.1007/978-3-030-11723-8_16
abstract: Reliably modeling normality and differentiating abnormal appearances from normal cases is a very appealing approach for detecting pathologies in medical images. A plethora of such unsupervised anomaly detection approaches has been made in the medical domain, based on statistical methods, content-based retrieval, clustering and recently also deep learning. Previous approaches towards deep unsupervised anomaly detection model patches of normal anatomy with variants of Autoencoders or GANs, and detect anomalies either as outliers in the learned feature space or from large reconstruction errors. In contrast to these patch-based approaches, we show that deep spatial autoencoding models can be efficiently used to capture normal anatomical variability of entire 2D brain MR images. A variety of experiments on real MR data containing MS lesions corroborates our hypothesis that we can detect and even delineate anomalies in brain MR images by simply comparing input images to their reconstruction.
  Results show that constraints on the latent space and adversarial training can further improve the segmentation performance over standard deep representation learning.
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags:
- Deep Learning
- Medical Imaging
- Radiology
- Generative Adversarial Networks
- Anomaly Detection
featured: false
links:
- type: pdf
  url: https://arxiv.org/abs/1804.04488
slidev: ''
hugoblox:
  ids:
    doi: 10.1007/978-3-030-11723-8_16
sync:
  source: legacy
  openalex: W2796762894
  scholar: ''
  locked:
  - publication
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 0302-9743
  - 1611-3349
  source_id: S106296714
  source_type: book series
  citations: 489
---

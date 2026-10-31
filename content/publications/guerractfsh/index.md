---
title: 'CTFSH: Full Head CT Anomaly Detection with Unsupervised Learning'
date: '1970-01-01'
draft: true
authors:
- Michele Guerra
- abhijeet-parida
- daniel-rueckert
- Mehmet Yigitsoy
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: ''
venue: ''
doi: ''
abstract: Unsupervised Anomaly Detection (UAD) is an inexpensive and effective method to bring value to the clinical workflow for pathology detection, especially in the emergency room setting, where quick prioritization of Computed Tomography (CT) scans is necessary. While there are numerous works dealing with UAD for medical images, most of them focus on Magnetic Resonance Imaging (MRI) and 2D slices of the brain. This work’s aim is to build a comparison between two commonly used baselines for UAD of volumetric CT scans. In addition to this, we borrowed two recent contributions to the field of Computer Vision in order to improve the reconstruction quality of our networks. These contributions effectively increased the AUROC for anomaly detection from 0.7 to 0.77 for one of our baselines. In order to guarantee that the anomaly detection algorithm is effective for all diseases, including fractures, we tested our models both on skull-stripped scans and unstripped scans. Leaving the skull in
  the CT volumes allowed the algorithm to efficiently classify fractures. To the best of our knowledge, this is the first work to show a comparison regarding the usage of skull-stripping. To facilitate further research in UAD for Head CT, we publish supplementary labels for the publicly available CQ500 dataset. The code for this study can be found in a GitHub repository athttps://github.com/pederismo/CTFSH
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: source
  url: https://openreview.net/forum?id=9qZUArz732o
  name: Publisher
hugoblox: {}
sync:
  source: legacy
  openalex: ''
  scholar: CPuApzoAAAAJ:kh2fBNsKQNwC
  locked: []
  citations: 0
image:
  caption: ''
  focal_point: Smart
---

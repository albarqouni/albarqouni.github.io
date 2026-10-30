---
title: 'Liver lesion localisation and classification with convolutional neural networks: a comparison between conventional and spectral computed tomography'
date: '2020-01-01'
draft: false
authors:
- Nadav Shapira
- Julia Fokuhl
- Manuel Schultheiß
- Stefanie Beck
- Felix K Kopp
- Daniela Pfeiffer
- Julia Dangelmaier
- Gregor Pahn
- Andreas P Sauter
- Bernhard Renger
- Alexander A Fingerle
- Ernst J Rummeny
- shadi-albarqouni
- nassir-navab
- Peter B Noël
publication_types:
- article-journal
publication:
  name: Biomedical Physics & Engineering Express
venue: ''
doi: 10.1088/2057-1976/ab6e18
abstract: "Abstract\n               \n                  Purpose: To evaluate the benefit of the additional available information present in spectral CT datasets, as compared to conventional CT datasets, when utilizing convolutional neural networks for fully automatic localisation and classification of liver lesions in CT images. Materials and Methods: Conventional and spectral CT images (iodine maps, virtual monochromatic images (VMI)) were obtained from a spectral dual-layer CT system. Patient diagnosis were known from the clinical reports and classified into healthy, cyst and hypodense metastasis. In order to compare the value of spectral versus conventional datasets when being passed as input to machine learning algorithms, we implemented a weakly-supervised convolutional neural network (CNN) that learns liver lesion localisation without pixel-level ground truth annotations. Regions-of-interest are selected automatically based on the localisation results and are used to train a second\
  \ CNN for liver lesion classification (healthy, cyst, hypodense metastasis). The accuracy of lesion localisation was evaluated using the Euclidian distances between the ground truth centres of mass and the predicted centres of mass. Lesion classification was evaluated by precision, recall, accuracy and F1-Score. Results: Lesion localisation showed the best results for spectral information with distances of 8.22 ± 10.72 mm, 8.78 ± 15.21 mm and 8.29 ± 12.97 mm for iodine maps, 40 keV and 70 keV VMIs, respectively. With conventional data distances of 10.58 ± 17.65 mm were measured. For lesion classification, the 40 keV VMIs achieved the highest overall accuracy of 0.899 compared to 0.854 for conventional data. Conclusion: An enhanced localisation and classification is reported for spectral CT data, which demonstrates that combining machine-learning technology with spectral CT information may in the future improve the clinical workflow as well as the diagnostic accuracy."
themes:
- computational-imaging
projects: []
datasets: []
tags:
- Deep Learning
- Medical Imaging
- Radiology
- Weakly-Supervised Learning
featured: false
links:
- type: pdf
  url: https://iopscience.iop.org/article/10.1088/2057-1976/ab6e18
slidev: ''
hugoblox:
  ids:
    doi: 10.1088/2057-1976/ab6e18
sync:
  source: legacy
  openalex: ''
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: crossref
  issn:
  - 2057-1976
  source_id: ''
  source_type: ''
---

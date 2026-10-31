---
title: Precise proximal femur fracture classification for interactive training and surgical planning.
date: '2020-01-01'
draft: false
authors:
- amelia-jimenez-sanchez
- anees-kazi
- shadi-albarqouni
- Chlodwig Kirchhoff
- Peter Biberthaler
- nassir-navab
- Sonja Kirchhoff
- Diana Mateus
publication_types:
- article-journal
publication:
  name: Int. J. Comput. Assist. Radiol. Surg.
venue: ijcars
doi: 10.1007/s11548-020-02150-x
abstract: Purpose Demonstrate the feasibility of a fully automatic computer-aided diagnosis (CAD) tool, based on deep learning, that localizes and classifies proximal femur fractures on X-ray images according to the AO classification. The proposed framework aims to improve patient treatment planning and provide support for the training of trauma surgeon residents. Material and methods A database of 1347 clinical radiographic studies was collected. Radiologists and trauma surgeons annotated all fractures with bounding boxes and provided a classification according to the AO standard. In all experiments, the dataset was split patient-wise in three with the ratio 70%:10%:20% to build the training, validation and test sets, respectively. ResNet-50 and AlexNet architectures were implemented as deep learning classification and localization models, respectively. Accuracy, precision, recall and $$F_1$$ F 1 -score were reported as classification metrics. Retrieval of similar cases was evaluated in
  terms of precision and recall. Results The proposed CAD tool for the classification of radiographs into types “A,” “B” and “not-fractured” reaches a $$F_1$$ F 1 -score of 87% and AUC of 0.95. When classifying fractures versus not-fractured cases it improves up to 94% and 0.98. Prior localization of the fracture results in an improvement with respect to full-image classification. In total, 100% of the predicted centers of the region of interest are contained in the manually provided bounding boxes. The system retrieves on average 9 relevant images (from the same class) out of 10 cases. Conclusion Our CAD scheme localizes, detects and further classifies proximal femur fractures achieving results comparable to expert-level and state-of-the-art performance. Our auxiliary localization model was highly accurate predicting the region of interest in the radiograph. We further investigated several strategies of verification for its adoption into the daily clinical routine. A sensitivity analysis
  of the size of the ROI and image retrieval as a clinical use case were presented.
themes:
- computational-imaging
projects: []
datasets: []
tags: []
featured: false
links:
- type: pdf
  url: https://arxiv.org/pdf/1902.01338
hugoblox:
  ids:
    doi: 10.1007/s11548-020-02150-x
    arxiv: '1902.01338'
sync:
  source: legacy
  openalex: ''
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: crossref
  issn:
  - 1861-6410
  - 1861-6429
  source_id: ''
  source_type: ''
  teaser: pdf:https://arxiv.org/pdf/1902.01338
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

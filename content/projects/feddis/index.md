---
title: 'FedDis: Federated disentangled representation learning for brain anomaly detection'
project_type: collaboration
summary: 'This research line addressed one of the central methodological challenges in collaborative medical AI: how to learn clinically meaningful representations across institutions without sharing patient data and without relying on pixel-level pathology annotations.'
date: '2020-06-01'
start: 2020-06
end: 2022-12
funders: []
pis:
- shadi-albarqouni
co_pis: []
authors:
- shadi-albarqouni
- cosmin-bercea
- daniel-rueckert
- benedikt-wiestler
partners:
- tum
- imperial
work_packages: []
themes:
- federated-learning
- computational-imaging
datasets: []
tags: []
featured: false
image:
  caption: 'FedDis: federated disentangled representation learning ([Bercea et al., Nature Machine Intelligence 2022](/publications/bercea-2022-federated/)).'
  focal_point: Center
---

This research line addressed one of the central methodological challenges in collaborative medical AI: how to learn clinically meaningful representations across institutions without sharing patient data and without relying on pixel-level pathology annotations. In the context of brain MRI, unsupervised anomaly detection is particularly attractive because lesion annotation is expensive, heterogeneous, and often unavailable, while privacy and governance constraints limit centralized multi-site learning.

Together with the collaborators, we developed *FedDis*, a federated disentangled representation-learning framework for unsupervised brain anomaly detection. The key methodological idea was to separate the representation space into *global shape* components, learned collaboratively across institutions, and *local appearance* components, trained locally to capture client-specific intensity and scanner characteristics. This disentanglement strategy was designed to address statistical heterogeneity across sites while preserving the privacy-preserving benefits of federated learning.

The resulting system was trained collaboratively on **1,532 healthy MRI scans from four institutions** and evaluated on **538 pathological volumes from six institutions**, covering multiple sclerosis, vascular lesions, and brain tumors. Compared with locally trained unsupervised models, the approach achieved substantial improvements in anomaly segmentation performance, including marked gains for multiple sclerosis, vascular lesions, and tumors, while requiring neither pathology annotations nor raw data sharing. The work was published in ***Nature Machine Intelligence*** and became one of the most visible methodological outputs of my collaborative research in federated medical imaging.

### Perspective

This project established an important methodological foundation for my later work on federated and collaborative learning, benchmark development, and multi-institutional validation in medical imaging. Conceptually, it shaped my subsequent research agenda by demonstrating that privacy-preserving learning across hospital networks must address not only optimization and communication constraints, but also representation-level heterogeneity across institutions. The insights from this project continue to inform my current and planned work on collaborative validation, foundation models under distribution shift, and trustworthy medical AI infrastructures such as OMI.

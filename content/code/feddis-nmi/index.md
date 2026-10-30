---
title: FedDis-NMI — The source code of FedDis
summary: Code for “Federated disentangled representation learning for unsupervised brain anomaly detection”. Recent advances in Deep Learning (DL) and the increased use of brain MRI have provided a great opportunity and interest in automated anomaly segmentation to support human interpretation and improve cl…
date: '2022-06-01'
lastmod: '2022-06-03'
repository: https://github.com/albarqounilab/FedDis-NMI
homepage: ''
language: Python
stars: 21
license: ''
topics:
- deep-learning
- federated-learning
- medical-imaging
code_type: research
course: ''
publications:
- bercea-2022-federated
- bercea-2021-feddis
themes:
- computational-imaging
- federated-learning
projects:
- feddis
datasets: []
authors:
- shadi-albarqouni
modality: []
sync:
  source: github
  repo: albarqounilab/FedDis-NMI
  locked:
  - publications
image:
  caption: Figure from the [FedDis-NMI README](https://github.com/albarqounilab/FedDis-NMI).
  focal_point: Center
---
### About the method

From the abstract of [Federated disentangled representation learning for unsupervised brain anomaly detection](/publications/bercea-2022-federated/):

> Recent advances in Deep Learning (DL) and the increased use of brain MRI have provided a great opportunity and interest in automated anomaly segmentation to support human interpretation and improve clinical workflow. However, medical imaging must be curated by trained clinicians, which is time-consuming and expensive. Further, data is often scattered across multiple institutions, with privacy regulations limiting its access. Here, we present FedDis (Federated Disentangled representation learning for unsupervised brain pathology segmentation) to collaboratively train an unsupervised deep convolutional neural network on 1532 healthy MR scans from four different institutions, and evaluate its performance in identifying abnormal brain MRIs including multiple sclerosis (MS), vascular lesions, low-grade tumors (LGG), and high-grade tumors/glioblastoma (HGG/GB) on a total of ~538 scans from 6 different institutions and datasets. To mitigate the statistical heterogeneity between the different institutes, we disentangle the parameter space into global, i.e., shape and local, i.e., appearance. We train the shape parameters jointly from four institutes to learn a global model of the healthy anatomical brain structure. The appearance parameters are trained locally on every institute and allow for personalization of the global domain-invariant features with client-specific information, such as scanner or acquisition parameter. We have shown that our collaborative approach, FedDis, improves anomaly segmentation results by 99.74% for MS, 83.33% for vascular lesions,and 40.45% for tumors over locally trained models without the need for annotations or sharing private local data. We found out that FedDis is especially beneficial for clients that share both healthy and anomaly data coming from the same institute, improving their local anomaly detection performance by up to 227% for MS lesions and 77% for brain tumors.

### Using the code

The repository README covers requirements, data, usage. See [the repository on GitHub](https://github.com/albarqounilab/FedDis-NMI#readme) for step-by-step instructions.

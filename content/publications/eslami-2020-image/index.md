---
title: Image-to-Images Translation for Multi-Task Organ Segmentation and Bone Suppression in Chest X-Ray Radiography
date: '2020-01-01'
draft: false
authors:
- Mohammad Eslami
- Solale Tabarestani
- shadi-albarqouni
- Ehsan Adeli
- nassir-navab
- Malek Adjouadi
publication_types:
- article-journal
publication:
  name: IEEE Transactions on Medical Imaging
venue: ieee-tmi
doi: 10.1109/tmi.2020.2974159
abstract: Chest X-ray radiography is one of the earliest medical imaging technologies and remains one of the most widely-used for diagnosis, screening, and treatment follow up of diseases related to lungs and heart. The literature in this field of research reports many interesting studies dealing with the challenging tasks of bone suppression and organ segmentation but performed separately, limiting any learning that comes with the consolidation of parameters that could optimize both processes. This study, and for the first time, introduces a multitask deep learning model that generates simultaneously the bone-suppressed image and the organ-segmented image, enhancing the accuracy of tasks, minimizing the number of parameters needed by the model and optimizing the processing time, all by exploiting the interplay between the network parameters to benefit the performance of both tasks. The architectural design of this model, which relies on a conditional generative adversarial network, reveals
  the process on how the well-established pix2pix network (image-to-image network) is modified to fit the need for multitasking and extending it to the new image-to-images architecture. The developed source code of this multitask model is shared publicly on Github as the first attempt for providing the two-task pix2pix extension, a supervised/paired/aligned/registered image-to-images translation which would be useful in many multitask applications. Dilated convolutions are also used to improve the results through a more effective receptive field assessment. The comparison with state-of-the-art algorithms along with ablation study and a demonstration video are provided to evaluate efficacy and gauge the merits of the proposed approach.
themes:
- computational-imaging
projects: []
datasets: []
tags:
- Deep Learning
- Medical Imaging
- Radiology
- Generative Adversarial Networks
featured: false
links:
- type: pdf
  url: https://arxiv.org/abs/1906.10089
hugoblox:
  ids:
    doi: 10.1109/tmi.2020.2974159
    arxiv: '1906.10089'
sync:
  source: legacy
  openalex: W2952587392
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 0278-0062
  - 1558-254X
  source_id: S58069681
  source_type: journal
  citations: 108
  teaser: pdf:https://arxiv.org/pdf/1906.10089
image:
  caption: Figure 1 of the paper.
  focal_point: Center
---

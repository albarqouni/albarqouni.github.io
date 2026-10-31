---
title: When regression meets manifold learning for object recognition and pose estimation
date: '2018-01-01'
draft: false
authors:
- mai-bui
- Sergey Zakharov
- shadi-albarqouni
- Slobodan Ilic
- nassir-navab
publication_types:
- paper-conference
publication:
  name: 2018 IEEE International Conference on Robotics and Automation (ICRA)
venue: ''
doi: 10.1109/icra.2018.8460654
abstract: In this work, we propose a method for object recognition and pose estimation from depth images using convolutional neural networks. Previous methods addressing this problem rely on manifold learning to learn low dimensional viewpoint descriptors and employ them in a nearest neighbor search on an estimated descriptor space. In comparison we create an efficient multi-task learning framework combining manifold descriptor learning and pose regression. By combining the strengths of manifold learning using triplet loss and pose regression, we could either estimate the pose directly reducing the complexity compared to NN search, or use learned descriptor for the NN descriptor matching. By in depth experimental evaluation of the novel loss function we observed that the view descriptors learned by the network are much more discriminative resulting in almost 30% increase regarding relative pose accuracy compared to related works. On the other hand, regarding directly regressed poses we obtained
  important improvement compared to simple pose regression. By leveraging the advantages of both manifold learning and regression tasks, we are able to improve the current state-of-the-art for object recognition and pose retrieval that we demonstrate through in depth experimental evaluation.
themes:
- computational-imaging
- responsible-ai
projects: []
datasets: []
tags:
- Computer Vision
- Deep Learning
- Pose Estimation
- Powerful Representation
- Prior Knowledge
featured: false
links:
- type: pdf
  url: https://ieeexplore.ieee.org/abstract/document/8460654/
hugoblox:
  ids:
    doi: 10.1109/icra.2018.8460654
sync:
  source: legacy
  openalex: W2804855082
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 1050-4729
  - 2577-087X
  source_id: S4210217939
  source_type: conference
  citations: 29
---

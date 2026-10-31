---
title: Digital staining of white blood cells with confidence estimation
date: '2023-01-01'
draft: false
authors:
- agnieszka-tomczak
- slobodan-ilic
- Gaby Marquardt
- Thomas Engel
- nassir-navab
- shadi-albarqouni
publication_types:
- article-journal
publication:
  name: IEEE Transactions on Medical Imaging
venue: ieee-tmi
doi: 10.1109/tmi.2023.3314695
abstract: Chemical staining of the blood smears is one of the crucial components of blood analysis. It is an expensive, lengthy and sensitive process, often prone to produce slight variations in colour and seen structures due to a lack of unified protocols across laboratories. Even though the current developments in deep generative modeling offer an opportunity to replace the chemical process with a digital one, there are specific safety-ensuring requirements due to the severe consequences of mistakes in a medical setting. Therefore digital staining system would profit from an additional confidence estimation quantifying the quality of the digitally stained white blood cell. To this aim, during the staining generation, we disentangle the latent space of the Generative Adversarial Network, obtaining separate representation s of the white blood cell and the staining. We estimate the generated image’s confidence of white blood cell structure and staining quality by corrupting these representations
  with noise and quantifying the information retained between multiple outputs. We show that confidence estimated in this way correlates with image quality measured in terms of LPIPS values calculated for the generated and ground truth stained images. We validate our method by performing digital staining of images captured with a Differential Inference Contrast microscope on a dataset composed of white blood cells of 24 patients. The high absolute value of the correlation between our confidence score and LPIPS demonstrates the effectiveness of our method, opening the possibility of predicting the quality of generated output and ensuring trustworthiness in medical safety-critical setup.
themes:
- computational-imaging
- responsible-ai
projects:
- digital-staining
- computational-hematology
datasets: []
tags: []
featured: true
links:
- type: pdf
  url: https://ieeexplore.ieee.org/document/10248032
hugoblox:
  ids:
    doi: 10.1109/tmi.2023.3314695
sync:
  source: legacy
  openalex: ''
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: crossref
  issn:
  - 0278-0062
  - 1558-254X
  source_id: ''
  source_type: ''
image:
  caption: ''
  focal_point: Smart
---

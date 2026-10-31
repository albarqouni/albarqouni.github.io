---
title: 'AI for Hematology: Trustworthy digital staining and classification of white blood cells'
project_type: collaboration
acronym: AI for Hematology
summary: Academia–industry collaboration with Siemens AG and TU Munich that replaced the chemical staining of blood smears with a digital one — generative models that stain, segment and classify white blood cells, and that estimate how far each synthetic image can be trusted.
date: '2020-01-01'
start: 2020-01
end: 2023-12
funders: []
role: Scientific Lead
pis:
- nassir-navab
co_pis:
- name: slobodan-ilic
  org: siemens
authors:
- shadi-albarqouni
- agnieszka-tomczak
- slobodan-ilic
- nassir-navab
partners:
- tum
- siemens
work_packages: []
themes:
- computational-imaging
- responsible-ai
datasets: []
tags:
- hematology
- digital staining
- generative models
- uncertainty
featured: false
image:
  caption: 'Illustration of digital staining: an unstained blood smear (Mikael Häggström, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:White_blood_cell_on_blood_smear,_unstained.jpg), CC0) and a stained neutrophil ([Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Neutrophil_in_a_blood_smear.jpg), CC BY-SA 3.0); different cells, not model output. Teaser CC BY-SA 3.0.'
  focal_point: Center
---
Chemical staining of blood smears is a routine but expensive, slow and sensitive step of blood analysis, and the lack of unified protocols makes colours and visible structures vary between laboratories. Deep generative models can replace the chemical process with a digital one — but in a medical setting a convincing synthetic image is not enough: it has to keep the cell's diagnostic structures, and the system has to know when its output cannot be trusted.

### What we did

- **Digital staining that preserves the cell.** A multi-task, multi-domain generative network translates unstained into stained white-blood-cell images while learning nucleus and cytoplasm segmentation and direct reconstruction as auxiliary tasks, so that inter-cellular structures survive the translation. Injecting the target-domain label into the generator gives a domain-agnostic latent space that also supports automated leukocyte classification. Validated on leukocytes from 24 patients, with state-of-the-art staining and classification performance ([IEEE TMI 2020](/publications/tomczak-2020-multi/)).
- **Reading reliability from the latent space.** Corrupting a GAN's bottleneck representation with noise and comparing the resulting outputs reveals how robust that representation is — predicting uncertain regions of a synthetic image and flagging samples unfit for downstream tasks ([MICCAI 2022](/publications/tomczak-2022-can/)).
- **Confidence for every stained cell.** Disentangling the latent space into separate representations of the cell and of the stain yields separate confidence estimates for structure and staining quality; the estimated confidence correlates with perceptual image quality (LPIPS) and identifies unreliable synthetic cells ([IEEE TMI 2023](/publications/tomczak-2023-digital/)).

### Our role

Methodological lead on generative modelling and uncertainty estimation, and co-supervision — with Slobodan Ilic (Siemens AG) and Nassir Navab (TU Munich) — of Agnieszka Tomczak's industrial PhD, completed at TU Munich in 2023.

### Perspective

The project turned digital staining from an image-translation exercise into a question of trust, and laid the groundwork for our later work on uncertainty estimation and reliable medical image generation.

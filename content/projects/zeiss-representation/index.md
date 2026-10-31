---
title: 'Disentangled, fair and discriminative representations for ophthalmic imaging'
project_type: funded
acronym: ZEISS Representation Learning
summary: Industry project with Carl Zeiss Meditec on representation learning for medical imaging — microaneurysm segmentation for diabetic-retinopathy screening, interpretable disentangled representations, and representations that are invariant to sensitive attributes for fair and privacy-preserving AI.
date: '2018-01-01'
start: 2018-01
end: 2021-12
status: ''
funders:
- zeiss
grant_number: ''
funding_url: ''
role: Scientific Lead (Postdoc at TUM CAMP)
pis:
- nassir-navab
co_pis:
- name: Dr. Abouzar Eslami
  org: zeiss
authors:
- shadi-albarqouni
- hasan-sarhan
- nassir-navab
partners:
- zeiss
- tum
work_packages: []
themes:
- responsible-ai
datasets: []
tags:
- ophthalmology
- diabetic retinopathy
- representation learning
- disentanglement
- fairness
featured: false
image:
  caption: 'Multi-scale microaneurysm segmentation on a fundus image — green: true positives, red: missed, cyan: false positives ([Sarhan et al., MICCAI 2019](/publications/sarhan-2019-multi/)).'
  focal_point: Center
---
Data-driven models only reach clinical practice if what they learn is discriminative enough for subtle findings, compact and interpretable enough to be inspected, and free of information it should not rely on. Together with Carl Zeiss Meditec, the project addressed all three through representation learning, starting from retinal imaging for diabetic-retinopathy screening.

### What we did

- **Finding the smallest lesions.** Microaneurysms are the earliest visible sign of diabetic retinopathy and occupy only a few pixels of a fundus image. A two-stage approach segments them on multiple scales with a region-proposal fully convolutional network, then refines the candidates with a patch-wise network trained with an embedding triplet loss and selective sampling of hard patches — a 30% relative improvement over a plain fully convolutional network ([MICCAI 2019](/publications/sarhan-2019-multi/); extended in [IET Image Processing](/publications/sarhan-2021-microaneurysms/)).
- **Interpretable latent spaces.** An adversarial variational autoencoder with a total-correlation constraint enforces independent latent factors while keeping reconstruction fidelity, improving disentanglement by 81.5% and making the representation useful for clustering and for classification with few labels ([DART @ MICCAI 2019](/publications/sarhan-2019-learning/)).
- **Fairness by orthogonal disentanglement.** Splitting the representation into a target code and a sensitive code, enforcing orthogonality between them and maximising the entropy of the target code with respect to the sensitive attribute yields representations that are invariant to it — state of the art on three of five benchmarks ([ECCV 2020](/publications/sarhan-2020-fairness/)) — and carries over to privacy-preserving medical applications such as autism detection and healthcare insurance ([DART/DCL @ MICCAI 2020](/publications/sarhan-2020-fairness-2/)).

### Our role

Scientific lead of the project as postdoc at TUM CAMP under Nassir Navab, and co-supervision — with Abouzar Eslami (Carl Zeiss Meditec) — of Hasan Sarhan's industrial PhD, completed at TU Munich in 2024.

### Perspective

The work on disentangled and orthogonal representations became a building block of our later research on fairness, privacy and federated learning in medical imaging.

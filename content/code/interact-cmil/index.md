---
title: INTERACT-CMIL
summary: 'Code for “INTERACT-CMIL: Multi-Task Shared Learning and Inter-Task Consistency for Conjunctival Melanocytic Intraepithelial Lesion Grading”. Accurate grading of Conjunctival Melanocytic Intraepithelial Lesions (CMIL) is essential for treatment and melanoma prediction but remains difficult due to sub…'
date: '2025-11-17'
lastmod: '2025-12-02'
repository: https://github.com/albarqounilab/INTERACT-CMIL
homepage: ''
language: Jupyter Notebook
stars: 0
license: ''
topics: []
code_type: research
course: ''
publications:
- ikinci-2026-interact
themes:
- computational-imaging
projects:
- interact-cmil
datasets: []
authors:
- shadi-albarqouni
modality: []
sync:
  source: github
  repo: albarqounilab/INTERACT-CMIL
  locked: []
image:
  caption: Teaser figure of the accompanying paper.
  focal_point: Center
---
### About the method

From the abstract of [INTERACT-CMIL: Multi-Task Shared Learning and Inter-Task Consistency for Conjunctival Melanocytic Intraepithelial Lesion Grading](/publications/ikinci-2026-interact/):

> Accurate grading of Conjunctival Melanocytic Intraepithelial Lesions (CMIL) is essential for treatment and melanoma prediction but remains difficult due to subtle morphological cues and interrelated diagnostic criteria. We introduce INTERACT-CMIL, a multi-head deep learning framework that jointly predicts five histopathological axes; WHO4, WHO5, horizontal spread, vertical spread, and cytologic atypia, through Shared Feature Learning with Combinatorial Partial Supervision and an Inter-Dependence Loss enforcing crosstask consistency. Trained and evaluated on a newly curated, multicenter dataset of 486 expert-annotated conjunctival biopsy patches from three university hospitals, INTERACT-CMIL achieves consistent improvements over CNN and foundation-model (FM) baselines, with relative macro $\mathrm{F}_{1}$ gains up to $55.1 \%(\text{WHO} 4)$ and 25.0% (vertical spread). The framework provides coherent, interpretable multicriteria predictions aligned with expert grading, offering a reproducible computational benchmark for CMIL diagnosis and a step toward standardized digital ocular pathology.

---
title: 'INTERACT-CMIL: Interpretable multi-task grading of conjunctival melanocytic lesions'
project_type: collaboration
summary: This project addresses the grading of conjunctival melanocytic intraepithelial lesions (CMIL), rare precursors of conjunctival melanoma characterized by complex, interdependent histopathological criteria and substantial inter-observer variability.
date: '2024-01-01'
start: 2024-01
end: ''
funders: []
pis:
- shadi-albarqouni
co_pis: []
authors:
- shadi-albarqouni
- mert-ikinci
- martina-herwigcarl
- luna-toma
partners:
- ukb
- ukt
- uker
work_packages: []
themes:
- computational-imaging
- responsible-ai
datasets:
- cmil-histopathology
tags: []
featured: false
image:
  caption: Conjunctival biopsies with predicted and ground-truth grades ([Ikinci et al., 2026](/publications/ikinci-2026-interact/)).
  focal_point: Center
---

**Collaborators:** *University Hospital Tübingen, University Hospital Erlangen*

This project addresses the grading of conjunctival melanocytic intraepithelial lesions (CMIL), rare precursors of conjunctival melanoma characterized by complex, interdependent histopathological criteria and substantial inter-observer variability.
Together with clinical partners, we curated a multi-center, expert-annotated histopathology dataset comprising 486 conjunctival biopsy image patches labeled along five clinically defined grading axes.
Methodologically, we developed *INTERACT-CMIL*, a multi-task deep learning framework modeling inter-criterion dependencies via selective multi-head supervision and an inter-task consistency loss.

The proposed approach outperformed CNN and pathology foundation-model baselines (macro-F1 up to 85%), producing coherent and interpretable predictions aligned with expert grading standards. Methodological development and evaluation were coordinated within my group in close collaboration with the clinical partners.

### Perspective

The project established a reproducible computational benchmark for CMIL grading and contributed to the standardization of digital ocular pathology. A related follow-up project on AI-assisted eyelid tumor analysis received a University of Bonn Prototype Grant, supporting translational development and clinical feasibility studies.

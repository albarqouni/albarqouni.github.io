---
title: Federated foundation models for multi-center CT staging of pancreatic cancer
project_type: collaboration
summary: This project addresses preoperative staging of pancreatic ductal adenocarcinoma (PDAC), where lymph node metastasis is a major prognostic factor but CT-based assessment suffers from low sensitivity and high inter-observer variability.
date: '2023-05-01'
start: 2023-05
end: ''
funders: []
pis:
- shadi-albarqouni
co_pis: []
authors:
- shadi-albarqouni
- david-gaviria
- parinishtha-bhalla
- patrick-kupczyk
- alexander-semaan
partners:
- ukb
- charite
- umg
- unimelb
work_packages: []
themes:
- computational-imaging
- federated-learning
datasets:
- pdac-ct
tags: []
featured: false
image:
  caption: Contrast-enhanced abdominal CT from the [PDAC dataset](/datasets/pdac-ct/).
  focal_point: Center
---

**Collaborators:** *University Medical Center Göttingen, Charité – Universitätsmedizin Berlin, Peter MacCallum Cancer Centre*

This project addresses preoperative staging of pancreatic ductal adenocarcinoma (PDAC), where lymph node metastasis is a major prognostic factor but CT-based assessment suffers from low sensitivity and high inter-observer variability.
Together with partners across three German centers, we established a retrospective multi-center cohort of 546 patients to enable evaluation under real-world heterogeneity while preserving data privacy.
Methodologically, we combined CT foundation model transfer learning (pre-training on 148,000 volumetric CT scans) with heterogeneity-aware federated optimization. The resulting system improved federated performance by +12.6% balanced accuracy over FedAvg and recovered most of the centralized reference performance (centralized BA 0.601; DOR 3.45).

### Perspective

The project establishes a sustainable multi-center collaboration for privacy-preserving oncologic imaging in Germany. Ongoing work extends the framework toward multimodal integration and more robust harmonization strategies, and a joint DFG proposal with the clinical partners has been submitted to further advance federated foundation models for PDAC staging and translation.

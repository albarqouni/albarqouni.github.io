---
title: Eyelid Tumor Triage using Uncertainty-Aware and Explainable Artificial Intelligence
date: '2026-09-25'
draft: false
authors:
- ashkan-shakarami
- shadi-albarqouni
- Frank G. Holz
- Karin U Loeffler
- martina-herwigcarl
publication_types:
- abstract
publication:
  name: 124th DOG Congress (Deutsche Ophthalmologische Gesellschaft), Berlin, 24–27 September 2026
venue: dog
doi: ''
abstract: 'Objectives: Early differentiation between benign and malignant eyelid tumors is clinically essential yet challenging due to subtle clinical and morphological features. As many eyelid lesions are first evaluated outside specialized centers, the primary goal is referral support and triage rather than definitive diagnosis. We developed and evaluated an AI-based clinical decision support system to assist assessment and estimate malignancy risk from documentation of periocular lesions to facilitate referral to ocular oncology specialists. Methods: This retrospective single-center cohort included consecutive patients from the University Eye Hospital Bonn archive (2020–2025). Ground truth was histopathology. The dataset comprised 956 patients (472 benign, 484 malignant) with 1,449 images from benign and 1,408 from malignant lesions; patients contributed one to multiple images (median 3, IQR 2–4). Splitting was strictly patient-level: 20% hold-out test and 80% stratified 5-fold cross-validation. Images were standardized using a face-landmarker guided periocular extraction pipeline. A ResNet50 backbone with augmentation and MixUp/CutMix was fine-tuned for binary classification. Class weights were applied to mitigate imbalance. Performance metrics were Accuracy (Acc), AUC, Sensitivity (Sen), and F1-score (F1), reported in percent (mean ± SD). Predictive uncertainty was estimated via MC Dropout; Grad-CAM provided lesion-focused explainability. Results: The model achieved Acc 78.12 ± 0.97, AUC 86.06 ± 0.82, Sen 83.71 ± 7.52, and F1 79.35 ± 2.09. MC Dropout yielded clinically meaningful uncertainty estimates. Uncertainty was lowest for correct predictions (TP 6.79 ± 4.12; TN 6.78 ± 4.97) and higher for errors, especially false negatives (FP 9.20 ± 4.27; FN 12.01 ± 3.39), indicating increased uncertainty in misclassified malignant cases, which is a system alert for re-checking those images. Grad-CAM localized the tumor reliably within the periocular region, consistent with the clinically visible lesion. Conclusions: A patient-level, uncertainty-aware approach with face-landmarker guided periocular standardization reliably differentiates benign from malignant eyelid tumors. Unlike conventional image-classification models providing only categorical outputs, our system integrates risk estimation, uncertainty quantification, and lesion-focused visual explainability, enhancing referral-oriented triage allowing for safer clinical decision-making.'
themes:
- responsible-ai
projects:
- eyelid-tumor-ai
- uncertainty
datasets: []
tags:
- abstract
featured: false
links:
- type: source
  url: https://dog-kongress.de/
  name: DOG Congress
hugoblox: {}
sync:
  source: manual
  openalex: ''
  scholar: ''
  locked: [title, date, authors, publication, publication_types, venue, abstract, projects]
image:
  caption: ''
  focal_point: Smart
---

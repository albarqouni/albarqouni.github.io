---
title: 'KI-gestützte Diagnostik von Tumoren am Auge: Dignitätseinordnung von Lidtumoren mittels KI zur optimierten Patienteneinbestellung'
project_type: funded
acronym: Eyelid Tumour AI
summary: Prototyping grant of the University of Bonn (Transfer Center enaCom) to develop an app that supports the assessment and classification of eyelid tumours — faster diagnosis, better-targeted referral and better surgical care.
date: '2025-01-01'
start: 2025-01
end: ''
status: ''
funders:
- unibonn-funds
grant_number: Prototypisierungsgrant (Transfer Center enaCom)
funding_url: https://www.uni-bonn.de/de/forschung-lehre/transfer/transfercenter-enacom/foerdermoeglichkeiten/prototypisierungsgrants
role: co-PI
pis:
- martina-herwigcarl
co_pis:
- name: shadi-albarqouni
  org: ukb
authors:
- martina-herwigcarl
- shadi-albarqouni
- ashkan-shakarami
partners:
- ukb
- uni-bonn
work_packages: []
themes:
- responsible-ai
datasets: []
tags:
- ophthalmology
- eyelid tumours
- uncertainty
- explainability
- translation
featured: false
image:
  caption: 'Illustration of the planned app: photograph, periocular standardisation, malignancy risk with uncertainty, referral. Interface mock-up; eyelid photograph (chalazion) from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Chalazion.JPG), public domain.'
  focal_point: Center
---
*Ein Team unter Leitung von Prof. Dr. Martina Christina Herwig-Carl (Klinik für Augenheilkunde, Universitätsklinikum Bonn) entwickelt eine App, die bei der Einschätzung und Klassifizierung von Augenlidtumoren unterstützt. Dies soll eine schnellere Diagnostik und eine bessere operative Versorgung ermöglichen.*

Eyelid lesions are common, and telling benign from malignant tumours early is essential — yet many are first seen outside specialised centres, where subtle clinical and morphological features make the call difficult. The question there is less a definitive diagnosis than *who needs to be referred, and how urgently*.

### What we do

- **Referral-oriented malignancy risk from routine photographs.** A face-landmarker-guided pipeline standardises the periocular region, and a fine-tuned ResNet-50 estimates malignancy risk with patient-level evaluation on 956 patients from the University Eye Hospital Bonn archive (2020–2025), histopathology as ground truth — AUC 86% and sensitivity 84% ([DOG 2026](/publications/shakarami-2026-eyelid/)).
- **Knowing when to look again.** Monte Carlo dropout gives each prediction an uncertainty that is highest for misclassified — especially missed malignant — cases, turning it into an alert to re-check those images; Grad-CAM shows that the model attends to the visible lesion.
- **From model to app.** Funded as a prototyping grant by the Transfer Center enaCom of the University of Bonn, the work is being turned into an app that supports the assessment and triage of eyelid tumours in clinical practice.

### Our role

Co-PI: methodological lead on uncertainty-aware and explainable AI, with Ashkan Shakarami (postdoctoral fellow, Department of Ophthalmology) developing the models.

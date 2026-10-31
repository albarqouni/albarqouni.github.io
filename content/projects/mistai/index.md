---
title: 'MISTAI: Medical Intelligence & Skills Training in AI'
acronym: MISTAI
summary: Bilateral UKB–Dnipro State Medical University project, funded by the NRW Ministry of Culture and Science, building an AI pipeline and training programme in computational pathology for muscle-invasive bladder cancer.
date: '2026-07-01'
start: 2026-07
end: 2026-12
status: ''
funders:
- mkw-nrw
grant_number: ''
funding_url: ''
role: PI
pis:
- shadi-albarqouni
co_pis:
- name: Prof. Dr. Verena Tischler
  org: ukb
- name: nina-bondarenko
  org: dnipro-state-medical-university
authors:
- shadi-albarqouni
- nina-bondarenko
partners:
- ukb
- dnipro-state-medical-university
work_packages:
- id: WP1
  title: Setup & infrastructure
  summary: Data-sharing protocol, cloud workspace, federated nodes at both sites, and a validated slide-processing pipeline (July 2026).
  lead: ukb
  our_role: Lead
- id: WP2
  title: Data collection, preparation & annotation
  summary: Retrospective bladder-cancer cohort from DSMU, H&E and IHC slides digitised in Bonn, quality control, stain normalisation and joint annotation (July – September 2026).
  lead: dnipro-state-medical-university
  our_role: Partner
- id: WP3
  title: Foundation-model fine-tuning & AI development
  summary: Fine-tuning pathology foundation models (GigaPath, Virchow, CHIEF), spatial tumour-infiltrating-lymphocyte analysis, cross-site federated experiments and a QuPath plugin for pathologists (September – November 2026).
  lead: ukb
  our_role: Lead
- id: WP4
  title: Exchange visit & Computational Pathology Workshop
  summary: One-week visit of the DSMU team to Bonn, co-located with an open Computational Pathology Workshop (December 2026).
  lead: ukb
  our_role: Lead
- id: WP5
  title: Education module, dissemination & reporting
  summary: Computational pathology teaching module for DSMU, conference presentations, an open-access manuscript and follow-on proposals (November – December 2026).
  lead: dnipro-state-medical-university
  our_role: Partner
themes:
- computational-imaging
- responsible-ai
- federated-learning
datasets: []
tags:
- Digital Pathology
- Foundation Models
- Bladder Cancer
- Capacity Building
featured: false
project_type: funded
---
The war in Ukraine has severely disrupted medical research and teaching. Digital pathology and AI offer a way to keep both going without depending on physical infrastructure. **MISTAI** is a bilateral cooperation between the **University Hospital Bonn** and **Dnipro State Medical University (DSMU)**, funded by the **Ministry of Culture and Science of North Rhine-Westphalia (MKW NRW)**.

### Goals

- **Shared data infrastructure:** digitise and validate at least 100 H&E and IHC whole-slide images from a DSMU cohort of muscle-invasive bladder cancer (MIBC), on a joint secure platform.
- **AI diagnostic pipeline:** fine-tune state-of-the-art pathology foundation models on the combined Bonn–Dnipro data, including spatial analysis of tumour-infiltrating lymphocytes from routine H&E slides, inspired by the UC-TIL approach.
- **Clinical tool:** a QuPath plugin that lets pathologists run the trained model directly in their existing workflow.
- **Capacity building:** weekly remote collaboration, a one-week exchange visit to Bonn, and a Computational Pathology teaching module for the DSMU curriculum.
- **Follow-on work:** a joint DFG/BMBF proposal outline and a MICCAI challenge concept.

### Partners

Bonn contributes high-resolution slide scanners, AI infrastructure and expertise in computational medical imaging (Prof. Shadi Albarqouni) and translational lung and tumour pathology (Prof. Verena Tischler). DSMU contributes a clinically distinct bladder-cancer cohort and long-standing pathology expertise (Assoc. Prof. Nina Bondarenko, Department of Pathological Anatomy).

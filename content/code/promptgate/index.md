---
title: PromptGate
summary: PromptGate tackles open-set federated active learning, where each client holds a private unlabeled pool contaminated with out-of-distribution (OOD) samples and artifacts. The goal is to spend a limited annotation budget on in-distribution (ID) candidates while keeping client data private.
date: '2026-06-20'
lastmod: '2026-06-25'
repository: https://github.com/albarqounilab/PromptGate
homepage: ''
language: Python
stars: 0
license: MIT
topics: []
code_type: research
course: ''
publications:
- nesturi-2026-promptgate
themes:
- computational-imaging
- federated-learning
projects: []
datasets: []
authors:
- shadi-albarqouni
modality: []
sync:
  source: github
  repo: albarqounilab/PromptGate
  locked: []
image:
  caption: Figure from the [PromptGate README](https://github.com/albarqounilab/PromptGate).
  focal_point: Center
---
### Overview

![PromptGate overview](resources/PromptGate_Teaser.png)

PromptGate tackles **open-set federated active learning**, where each client holds a private unlabeled pool contaminated with out-of-distribution (OOD) samples and artifacts. The goal is to spend a limited annotation budget on in-distribution (ID) candidates while keeping client data private.

At the core is a **VLM gate** built on a frozen BiomedCLIP backbone (image + text encoders). Cosine similarity between image features and prompt embeddings yields **VLM-gated pseudo-labels** that separate the unlabeled pool into **ID candidates** and **OOD / artifacts**, so the active-learning oracle is only queried on likely-ID samples.

Gating is driven by **client-adaptive learnable prompts**, which decompose into:
- **Global tokens** — shared across clients via FedAvg.
- **Local tokens** — kept private and never leave the site.
- **Mixed tokens** — combine global and local context (with a Class-Specific-Context / CSC variant), replacing the static text-prompt baseline.

A few shots of ID/OOD labeled data tune these prompts via **CoOp**. The downstream **task model** runs each active-learning round (inference → training), and its parameters are shared via FedAvg, while a clinician oracle labels the queried ID candidates. PromptGate is agnostic to the acquisition rule and is evaluated with **Random, Entropy, FEAL, PAL, LfOSA, and OpenPath**.

---

### Using the code

The repository README covers environment setup, install the remaining requirements, datasets & attribution, out-of-distribution (ood) setup, usage. See [the repository on GitHub](https://github.com/albarqounilab/PromptGate#readme) for step-by-step instructions.

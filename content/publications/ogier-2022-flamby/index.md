---
title: 'Flamby: Datasets and benchmarks for cross-silo federated learning in realistic healthcare settings'
date: '2022-01-01'
draft: false
authors:
- Jean Ogier Du Terrail
- Samy-Safwan Ayed
- Edwige Cyffers
- Felix Grimberg
- Chaoyang He
- Regis Loeb
- Paul Mangold
- Tanguy Marchand
- Othmane Marfoq
- Erum Mushtaq
- Boris Muzellec
- Constantin Philippenko
- Santiago Silva
- Maria Telenczuk
- shadi-albarqouni
- Salman Avestimehr
- Aurélien Bellet
- Aymeric Dieuleveut
- Martin Jaggi
- Sai Praneeth Karimireddy
- Marco Lorenzi
- Giovanni Neglia
- Marc Tommasi
- Mathieu Andreux
publication_types:
- article-journal
publication:
  name: Advances in Neural Information Processing Systems
venue: neurips
doi: 10.52202/068431-0384
abstract: Federated Learning (FL) is a novel approach enabling several clients holding sensitive data to collaboratively train machine learning models, without centralizing data. The cross-silo FL setting corresponds to the case of few (2-50) reliable clients, each holding medium to large datasets, and is typically found in applications such as healthcare, finance, or industry. While previous works have proposed representative datasets for cross-device FL, few realistic healthcare cross-silo FL datasets exist, thereby slowing algorithmic research in this critical application. In this work, we propose a novel cross-silo dataset suite focused on healthcare, FLamby (Federated Learning AMple Benchmark of Your cross-silo strategies), to bridge the gap between theory and practice of cross-silo FL. FLamby encompasses 7 healthcare datasets with natural splits, covering multiple tasks, modalities, and data volumes, each accompanied with baseline training code. As an illustration, we additionally
  benchmark standard FL algorithms on all datasets. Our flexible and modular suite allows researchers to easily download datasets, reproduce results and re-use the different components for their research. FLamby is available at www.github.com/owkin/flamby.
themes:
- federated-learning
- computational-imaging
projects:
- federated-learning
datasets: []
tags:
- Medical Imaging
- Deep Learning
featured: true
links:
- type: pdf
  url: https://infoscience.epfl.ch/bitstreams/6151cb52-ccd3-439e-a7bc-b693b2531716/download
- type: code
  url: www.github.com/owkin/flamby
slidev: ''
hugoblox:
  ids:
    doi: 10.52202/068431-0384
    arxiv: '2210.04620'
sync:
  source: legacy
  openalex: W7133183237
  scholar: ''
  locked: []
  verified: '2026-10-29'
  verified_by: openalex
  issn:
  - 1049-5258
  source_id: S4363606243
  source_type: conference
  merged:
  - du-2022-flamby
  - terrail-2022-flamby
  citations: 80
image:
  caption: The seven FLamby datasets (thumbnails from Table 1 of the paper).
  focal_point: Center
---

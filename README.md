# Albarqouni Lab website (Computational Medical Imaging Research, CoMI)

Hugo Blox (Academic v6) site for the Computational Medical Imaging Research (CoMI) Lab — publications synced from Google Scholar, funded projects,
teaching per semester, community events on a globe, datasets, demos and code, all linked through **three research
themes** (Computational Medical Imaging · Affordable & Responsible AI · Federated Learning), **people** and **funded projects**.

## Run locally

```bash
pnpm install                      # Tailwind + Pagefind
hugo server                       # needs Hugo extended ≥ 0.162 and Go ≥ 1.21
```

A project-local toolchain lives in `.tools/` (git-ignored): `PATH=$PWD/.tools/bin:$PWD/.tools/go/bin:$PATH hugo server`.

## How everything is linked

One front-matter field connects a page to everything else — no manual cross-listing:

| field          | values                                   | effect |
|----------------|------------------------------------------|--------|
| `authors:`     | team slugs or names (`shadi-albarqouni`) | page appears on that person's profile (`/authors/<slug>/`) |
| `themes:`      | `computational-imaging`, `responsible-ai`, `federated-learning` | page appears on the theme page and theme filters |
| `projects:`    | funded-project slugs (`sanad`, `omi`, …) | page appears on the project page (publications, news, events, courses) |
| `datasets:`    | dataset slugs                            | publication ↔ dataset |
| `place:`       | key in `data/places.yaml`                | pins the event on the map and the home-page globe |
| `funders:` / `partners:` | keys in `data/organizations.yaml` | logos, partner map, globe arcs |
| `venue:`       | key in `data/venues.yaml`                | quartile / impact factor / acceptance-rate badges |

## Content sections

| section | path | notes |
|---|---|---|
| Publications | `content/publications/<slug>/index.md` | created/enriched by `scripts/sync_publications.py`; teaser = `featured.*`; `slidev:` = interactive explainer URL |
| Funded projects | `content/projects/<slug>/index.md` | period, funders, partners, PIs, co-PIs, `work_packages`, team |
| Teaching | `content/teaching/<course>/_index.md` + `<course>/<ws2627 \| ss27>/index.md` | course = stable info; one sub-page per semester |
| Community | `content/community/<slug>/` | `category: talk \| conference \| meeting \| event`; all images in the folder become the gallery |
| Media | `content/media/<slug>/` | press coverage, interviews, videos; `image_credit` + `image.caption: "Photo: …"` |
| Themes | `content/themes/<slug>/_index.md` | taxonomy term pages; `keywords` drive automatic theme suggestions |
| Datasets / Demos / Code | `content/{datasets,demos,code}/<slug>/` | demos can embed a Hugging Face Space (`demo_url`, `embed: true`); without `demo_url`, `status: Coming soon` shows a placeholder badge; `weight` orders demos. Code pages of the GitHub org are generated (see Automation) |
| Positions | `content/positions/<slug>/` | `position_id`, `deadline`, `status: open \| closed`; includes the application form |
| Team | `data/authors/<slug>.yaml` + `assets/media/authors/<slug>.jpg` | `group:` controls the team page section (`data/groups.yaml`) |

## Automation

| what | how |
|---|---|
| Publications | `.github/workflows/sync-publications.yml` — weekly; opens a PR. Locally: `python3 scripts/sync_publications.py --dry-run` |
| Code repositories | `.github/workflows/sync-code.yml` — weekly; every public, non-fork repo of `lab.github_org` gets a page in `content/code/` (summary, README overview, teaser, linked papers, stars); opens a PR. Locally: `python3 scripts/sync_code_repos.py [--only REPO]`; list fields (or `body`, `image`) in `sync.locked` to keep manual edits |
| Alumni positions | `.github/workflows/alumni-now.yml` — yearly (15 Jan); updates `now:` of alumni from their ORCID or GitHub record and lists leads from their latest papers (OpenAlex) in `docs/alumni-now.md`; opens a PR. Locally: `python3 scripts/alumni_now.py --dry-run`. Add `now_locked: true` to keep a hand-written line |
| Citations | live per-paper counts from OpenAlex in the browser; Scholar totals snapshot in `data/scholar.json` |
| Publication audit | `python3 scripts/audit_publications.py --apply` — verifies every paper against OpenAlex/Crossref/Semantic Scholar/arXiv (title + year + author must match), fixes DOI, publisher link, venue, abstract; report in `docs/publication-audit.md` |
| Teaser figures | `.tools/venv/bin/python scripts/fetch_teasers.py` — saves "Figure 1" (arXiv HTML, or cropped above the "Fig. 1" caption in the open-access PDF) as `featured.png`; featured papers show the venue logo instead |
| CV import (one-off) | `python3 scripts/import_cv_cooperations.py ~/Downloads/CV` — research collaborations + funding details from the LaTeX CV |
| Venue statistics | `.github/workflows/update-venues.yml` every July → `scripts/update_venues.py`: OpenAlex citedness + conference acceptance rates (automatic), SJR quartiles (with a SCImago CSV), and a list of Impact Factors to re-check in JCR (`docs/venue-report.md`) |
| New semester | `.github/workflows/new-semester.yml` on 1 Mar / 1 Sep, or `./scripts/new-semester.sh [WS2627] [course…]` |
| Migration from the old site | `python3 scripts/migrate_from_old.py ../albarqouni_web` (read-only on the old site) |

## Application form (open positions)

Fields and email subject are defined in `data/application_form.yaml`. Submissions go through
[Web3Forms](https://web3forms.com) straight to the PI's inbox — **the website stores nothing**.
Setup once: create an access key at web3forms.com for `shadi.albarqouni@ukbonn.de` and paste it into
`config/_default/params.yaml → lab.web3forms_key`.

## Team editing

See [docs/EDITING.md](docs/EDITING.md). Team members edit via `/admin` (Decap CMS) with their GitHub account;
every change becomes a pull request that the PI approves.

## Deploy

GitHub Pages via `.github/workflows/deploy.yml` on every push to `main`.

## Branding

CoMI palette (`assets/css/hbx/blocks/lab/style.css`): navy `#173869`, teal `#2D9D9B`, light grey `#C5C5C5`,
with University of Bonn blue `#004E9F` and yellow `#FCBA00`. Logos live in `assets/media/brand/`, partner/funder
logos in `assets/media/logos/` (keyed like `data/organizations.yaml`). The home-page banner is driven by
`data/pillars.yaml` (tabs, stats, photos from `assets/media/act/`, globe pins).

## API keys (GitHub → Settings → Secrets)

* `OPENALEX_API_KEY` — free key from openalex.org (anonymous use shares a tiny daily budget per IP and is exhausted quickly).
* `S2_API_KEY` — optional Semantic Scholar key (abstract fallback).
* Variable `OPENALEX_MAILTO` — contact e-mail for the OpenAlex polite pool.

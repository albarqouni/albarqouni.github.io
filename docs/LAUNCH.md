# Launch checklist — replacing albarqouni.github.io

**Nothing has been pushed.** Do these steps only when you decide to go live.

## What protects SEO and analytics

| Concern | How it is handled |
|---|---|
| Same address | The new site deploys to `https://albarqouni.github.io/` (the user-site repo `albarqouni/albarqouni.github.io`), never a sub-path. |
| Profile & team | `/authors/shadi-albarqouni/` keeps its URL and title (“Shadi Albarqouni \| Albarqouni Lab”); `/authors/admin/` redirects to it. `/team/` keeps URL and title (“Join our Team \| Albarqouni Lab”). Every member keeps `/authors/<name>/`. |
| All other old URLs (1,020) | `legacy/` holds 484 redirect pages (canonical + meta-refresh + noindex) and 266 old files (PDFs, videos, BibTeX, slides) at their original paths; 536 URLs are served directly by the new site. Regenerate with `python3 scripts/make_legacy_redirects.py ../../albarqouni_web/public`. |
| Regression guard | CI runs `scripts/check_legacy_urls.py` after every build; the deploy fails if any old URL stops resolving. |
| Google Analytics | GA4 `G-2YWNN9YME7` (property 399488622, same as today) loads **only after opt-in** in the consent banner (§ 25 TDDDG). Expect fewer recorded visits than before — visitors who decline are no longer counted. |
| Legal pages | `/impressum/` (UKB as publisher, § 18 MStV: Prof. Albarqouni) and `/privacy/` (Datenschutzerklärung). **Have both reviewed by the UKB data protection officer / Unternehmenskommunikation before launch.** |
| Third parties | Fonts, globe and map libraries are self-hosted; remaining outside requests: OpenStreetMap tiles (map pages), OpenAlex (citation counts), Google Analytics (after consent), Web3Forms (application form). |
| Google Scholar | Publication pages carry Highwire `citation_*` tags and schema.org `ScholarlyArticle`. |
| Structured data | `ResearchOrganization` (home), `Person` (profiles), `ScholarlyArticle` (papers). |

## Go-live steps (in order)

1. ✅ GA4 ID and Search Console verification are configured. Get the Impressum and privacy policy approved by UKB (data protection officer).
2. Back up the current live site: `git -C ../../albarqouni_web/public tag pre-relaunch-backup` (the old repo stays untouched otherwise).
3. Push this project as a **new `main` branch** of `albarqouni/albarqouni.github.io` (the old built site stays on `master`
   untouched). The *Build* workflow checks it (pull requests and pushes to `main`); review the result.
4. In the `albarqouni.github.io` repo: Settings → General → default branch **`main`**; Settings → Pages → Source:
   **GitHub Actions** (the *Deploy* workflow publishes every push to `main`). The team editor (`/admin/`) also commits to `main`.
5. Set up the team login once (docs/EDITING.md → “Team login”) and protect `main` (pull-request review by Code Owners).
6. Within the first hour: open 20–30 old URLs (Google results, old links) and confirm they land on the right page; check GA4 Realtime.
7. Search Console: submit `https://albarqouni.github.io/sitemap.xml`; use URL Inspection on the profile, team and a few papers;
   watch the *Pages* report for 404s during the following weeks. (No “Change of address” — the domain is unchanged.)

## Rollback

Settings → Pages → Source: **Deploy from a branch → `master` / root** brings the old site back immediately; `master` is never modified.

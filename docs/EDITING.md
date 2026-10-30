# Editing the website (team members)

You can update **your profile, news, community photos/events and your courses**. Every change becomes a pull
request; it goes live after the PI approves it.

## Option A — web editor (no git needed)

1. Go to **https://albarqouni.github.io/admin/** and log in with GitHub.
2. Pick a collection (Team profiles, News, Community & events, Teaching).
3. Edit, then *Save* → *Set status: Ready* — this opens a pull request.

Tips
- Use slugs for people: `firstname-lastname` (see `data/authors/`). Tag yourself in `authors` so the item shows on your profile.
- Link the funded project and research theme so the item shows on those pages too.
- For community events set `category` (talk / conference / meeting / event) and `place` (key from `data/places.yaml`; ask to add a new city).
- Photos: name the main one `featured.jpg`; every other image in the folder appears in the gallery.

## Option B — GitHub / local

Fork → edit Markdown/YAML → pull request. `hugo server` previews locally (see README).

## Admin setup (one-time, PI)

1. The website's repository is `albarqouni/albarqouni.github.io` (already set in `static/admin/config.yml → backend.repo`).
2. Set up the **team login** (below), so members can sign in at `/admin/`.
3. Branch protection on `main`: require pull-request review + *Require review from Code Owners* (`.github/CODEOWNERS`).
4. Settings → Pages → Source: GitHub Actions.

## Team login — GitHub sign-in relay (one-time, ~20 minutes)

GitHub Pages cannot complete a GitHub login by itself, so the editor at `/admin/` talks to a tiny free relay
([decap-proxy](https://github.com/sterlingwes/decap-proxy), a Cloudflare Worker). It only exchanges the login
code for a token; it stores nothing.

**What you need:** your GitHub account (`albarqouni`) and a free Cloudflare account, plus Node.js on your computer.

1. **Create the Cloudflare Worker URL first.** Sign up at <https://dash.cloudflare.com> (free plan). Your workers get
   addresses of the form `https://<worker-name>.<your-subdomain>.workers.dev`; the subdomain is shown under
   *Workers & Pages*. With the worker name `decap-oauth`, the relay URL will be
   `https://decap-oauth.<your-subdomain>.workers.dev` — call it **RELAY_URL**.
2. **Register the website as a GitHub OAuth app.** Open <https://github.com/settings/applications/new> (signed in as
   `albarqouni`) and enter:
   - Application name: `Albarqouni Lab website editor`
   - Homepage URL: **RELAY_URL**
   - Authorization callback URL: **RELAY_URL**`/callback`

   Click *Register application*, then *Generate a new client secret*. Keep the **Client ID** and **Client secret**.
3. **Deploy the relay** (in a terminal):
   ```bash
   git clone https://github.com/sterlingwes/decap-proxy && cd decap-proxy
   cp wrangler.toml.sample wrangler.toml      # then set  name = "decap-oauth"  in wrangler.toml
   npx wrangler login                         # opens the browser to connect your Cloudflare account
   npx wrangler secret put GITHUB_OAUTH_ID    # paste the Client ID
   npx wrangler secret put GITHUB_OAUTH_SECRET  # paste the Client secret
   npx wrangler deploy
   ```
   Opening **RELAY_URL** in a browser should now show “Hello 👋”.
4. **Tell the site where the relay is.** In `static/admin/config.yml` set `backend.base_url:` to **RELAY_URL**
   (no `/auth` or `/callback` at the end; `auth_endpoint: /auth` is already set).
5. **Test** after the site is live: open `https://albarqouni.github.io/admin/`, click *Login with GitHub*, approve the
   app once, and the collections (Team profiles, Media, Community, …) appear. A “repository not found” error means
   `backend.repo` is wrong or the repository is private.

Team members need nothing but a GitHub account: with `open_authoring` the editor forks the repository for them and
opens a pull request that you review.

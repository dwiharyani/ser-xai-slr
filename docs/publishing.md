# Publishing the website

The ZIP is a GitHub-ready source repository, not an already published GitHub project. Follow the README to push to a new public repository and select **Settings → Pages → Source → GitHub Actions**. Repository creation and the first deployment happen in your account.

The workflow validates public data, regenerates figures, checks that synthesis artifacts have not changed, installs exact npm-lockfile versions, builds and uploads `dist`, then deploys on main. Pull requests run validation and build only. The `github-pages` environment can be protected with GitHub's usual rules. The workflow needs Pages and id-token write permissions only for deployment.

Use Node 22.12+ and Python 3.12. The Vite base is relative; paths work at `username.github.io/repository/` and at a root domain. Every page uses a hash route, so `.../repository/#quality` is reload-safe on GitHub Pages. If you opt into an absolute base, set `BASE_PATH=/repository/` during the build.

The source GitHub URL is injected with `VITE_REPOSITORY_URL`. Without it, the header links to the local downloads section rather than a fabricated repository. To add a final paper DOI, update `CITATION.cff` when the publication is available. The manuscript PDF is not included in the website.

If Pages deployment fails before Pages was enabled, enable GitHub Actions as the publishing source and rerun the workflow. If npm ci fails after changing dependencies, regenerate and commit package-lock.json with npm install. A data validation failure should be investigated rather than bypassed: it may signal changed counts, a missing ID or an invalid score.

References: https://vite.dev/guide/static-deploy and https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

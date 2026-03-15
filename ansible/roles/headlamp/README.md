# Headlamp role

Installs [Headlamp](https://headlamp.dev/) (Kubernetes management UI) via Helm in a dedicated namespace. No built-in ingress; expose via Caddy at e.g. `headlamp-enclava.flowforge.sh` with basic auth.

## Requirements

- K3s cluster with `KUBECONFIG` on the control node
- Caddy role configured with a route for the Headlamp host and optional basic auth (`headlamp_ui_basic_auth_username` / `headlamp_ui_basic_auth_password` in secrets)

## What this role does

- Adds Headlamp Helm repo and installs `headlamp/headlamp` in the `headlamp` namespace (latest chart version)
- Disables chart ingress (Caddy reverse-proxies with TLS and basic auth)
- Service is `headlamp.headlamp.svc.cluster.local:80` for Caddy backend
- **Auto-login** (when `headlamp_auto_login_enabled: true`): deploys a small service at **`/internal-login`** that is **only reachable from internal IPs** (see `headlamp_auto_login_internal_cidrs`). From the internal network (or VPN so your client IP is in those CIDRs), open `https://headlamp-enclava.flowforge.sh/internal-login` after basic auth to get the token set and be redirected to Headlamp with no token prompt. Public access to `/internal-login` is redirected to `/` so the token page is never exposed. If traffic goes through Cloudflare, Caddy may see the proxy IP; ensure internal users reach from a network where the client IP is in `headlamp_auto_login_internal_cidrs`.
- **Default cluster access** (when `headlamp_admin_sa_enabled: true`, default): creates a **headlamp-admin** ServiceAccount in the Headlamp namespace, binds it to **cluster-admin**, and uses its token for auto-login so internal users get full cluster access by default (no manual token paste). Set `headlamp_admin_sa_enabled: false` to use the Headlamp app’s own SA token instead (more restricted).
- **Plugins**: `headlamp_watch_plugins: true` (default) so Headlamp watches the plugins dir for updates.

## Variables

See `defaults/main.yml`. Override in group_vars: `headlamp_chart_version`, `headlamp_namespace`, `headlamp_release_name`, `headlamp_auto_login_enabled`, `headlamp_admin_sa_enabled`, `headlamp_watch_plugins`.

## Caddy integration

In `group_vars/all.yml` add a route and (optionally) set basic auth in your secrets file:

```yaml
caddy_routes:
  - host: "headlamp-enclava.flowforge.sh"
    backend: "http://headlamp.headlamp.svc.cluster.local:80"
    zone: "flowforge.sh"
```

Secrets (e.g. SOPS): `headlamp_ui_basic_auth_username`, `headlamp_ui_basic_auth_password` so Caddy can protect the UI.

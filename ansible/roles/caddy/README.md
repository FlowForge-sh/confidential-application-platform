# Caddy role

Deploys **edge Caddy** as the public ingress gateway. It supports:
- **L4 SNI passthrough** (target mode) to tenant ingress and shared ops ingress.
- Optional legacy **edge TLS termination** for `external_caddy_http` compatibility.

## Requirements

- **Cloudflare tokens (per zone)** in `secrets.sops.yaml` as `cloudflare_tokens`: a map of DNS zone → API token (each token: Zone:Zone:Read + Zone:DNS:Edit for that zone). See `inventory/group_vars/secrets.sops.schema.yaml`.
- **Caddy image with Cloudflare DNS plugin.** Build from `files/Dockerfile` (uses `caddy_version`, e.g. 2.10.0) and set `caddy_image` in group_vars to your image.
- **DNS:** Point your domain(s) to the Caddy LoadBalancer IP (playbook prints it). Use Cloudflare in **DNS-only** (grey cloud) if you want TLS end-to-end to Caddy.

## What this role does

- Creates namespace `caddy`, edge Secret from `cloudflare_tokens`, edge ConfigMap/PVC/Deployment/Service.
- When `ops_ingress_enabled: true`, also deploys shared in-cluster `ops-ingress` (ConfigMap + Secret + PVC + Deployment + Service) for ops hostnames.
- **Edge Caddyfile** (in `templates/configmap.yaml.j2`): L4 SNI routes from `sni_routes` + discovered tenant SNI ConfigMaps. Optional HTTP/TLS site blocks are generated only for legacy `caddy_routes`.
- **ops-ingress Caddyfile** (in `templates/ops-ingress-configmap.yaml.j2`): terminates TLS for `ops_ingress_routes` and proxies to Hubble/Longhorn/Headlamp/Flux/Vault backends.
- **Pod labels/annotations** (on the Caddy Deployment’s pod template): `caddy.tls.resolvers`, `caddy.tls.dns`, `caddy.tls.dns.api_token`, and `caddy.hosts` (annotation) so Caddy setup is visible and label-driven where needed.
- Firewall: allow 443 on masters when `firewall_allow_ingress_ports: true` (default).

## Variables

- **caddy_namespace**: Kubernetes namespace (default: `caddy`).
- **caddy_version**: Caddy version used when building from `files/Dockerfile` (default: `2.10.0`).
- **caddy_image**: Image with Cloudflare DNS plugin; set to your image built from `files/Dockerfile` (default: `caddy-dns-cloudflare:latest`).
- **caddy_acme_email**: Email for Let's Encrypt ACME account.
- **sni_routes**: Static L4 passthrough routes at edge (`host` -> `backend_tls`).
- **caddy_routes**: Legacy edge HTTP routes (keep empty in pure SNI mode).
- **ops_ingress_enabled**: Deploy shared ops-ingress backend (default false).
- **ops_ingress_routes**: List of `{ host, backend, zone }` served by shared ops-ingress.
- **ops_ingress_zone_wildcards**: Optional explicit host list per zone for ops-ingress cert issuance.
- **caddy_data_storage_class**: Optional StorageClass for the cert-data PVC (empty = cluster default).
- **cloudflare_tokens**: Set by the playbook from `secrets.sops.yaml` (zone → token); required.
- **Optional basic auth** (set in secrets): `hubble_ui_basic_auth_username`/`hubble_ui_basic_auth_password`, `longhorn_ui_basic_auth_username`/`longhorn_ui_basic_auth_password`, `headlamp_ui_basic_auth_username`/`headlamp_ui_basic_auth_password` for the corresponding Caddy hosts.
- **Headlamp basic auth loop fix:** If the browser keeps re-prompting for basic auth after the Headlamp token page (e.g. redirect to `/c/main/token`), add `headlamp_gate_cookie_secret` to secrets (e.g. `openssl rand -hex 24`). Caddy will set a session cookie on first successful basic auth so redirects (which can drop the `Authorization` header) still allow access.

## Building your own image

The role expects an image built from `files/Dockerfile` (Caddy + Cloudflare DNS plugin). Optional build arg: `CADDY_VERSION` (default in Dockerfile: 2.10.0; override with `caddy_version` if you pass it).

```bash
# From repo root
docker build -t your-registry/caddy-dns-cloudflare:latest -f ansible/roles/caddy/files/Dockerfile .
# Optional: pin Caddy version
docker build --build-arg CADDY_VERSION=2.10.0 -t your-registry/caddy-dns-cloudflare:latest -f ansible/roles/caddy/files/Dockerfile .
docker push your-registry/caddy-dns-cloudflare:latest
```

Set in group_vars: `caddy_image: "your-registry/caddy-dns-cloudflare:latest"`. Runtime config (ACME email, per-zone Cloudflare tokens, resolvers 1.1.1.1) is provided by the role via Caddyfile and Secret, not the image.

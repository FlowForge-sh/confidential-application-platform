# Flux CD Ansible Role

Installs [Flux CD](https://fluxcd.io/) (GitOps) and configures a **single manifests repo** with Kustomize + SOPS decryption. Optionally deploys the **Flux UI (Capacitor)** for a browser-based dashboard.

## What the role does

1. **Flux controllers** – Installs the Flux CLI and controllers (source-controller, kustomize-controller, etc.) in `flux-system`.
2. **SOPS decryption** – When `flux_sops_age_key_file` is set (in group_vars), the playbook copies that key to the master; the role creates the `sops-age` secret so Kustomization can decrypt SOPS-encrypted manifests.
3. **GitRepository + Kustomization** – Creates them from `flux_manifests_repo_url`, `flux_manifests_repo_branch`, and `flux_manifests_repo_path` so Flux reconciles your manifests repo with SOPS decryption.
4. **Flux UI (Capacitor)** – When `flux_ui_enabled: true`, deploys [Capacitor](https://github.com/gimlet-io/capacitor) from OCI. Access via Caddy at `flux-enclava.flowforge.sh` or `kubectl port-forward -n flux-system svc/capacitor 9000:9000`.

## Configuration (group_vars/all.yml)

| Variable | Description |
|----------|-------------|
| `flux_manifests_repo_url` | Git URL of your manifests repo (e.g. `https://github.com/your-org/enclave-manifests`). |
| `flux_manifests_repo_branch` | Branch to sync (default `main`). |
| `flux_manifests_repo_path` | Path inside the repo to the `kustomization.yaml` (e.g. `.` or `tenants/overlays/flowforge`). |
| `flux_sops_age_key_file` | Path on the **control node** to the age private key (default: repo root `private-age-key.txt`). Playbook copies it to the master; role creates `sops-age` secret then the key is removed from the master. |
| `flux_ui_enabled` | Set `true` to deploy Capacitor (Flux UI). |
| `flux_version` | Flux CLI/controller version (e.g. `2.8.1`). |

## Manifests repo layout

Your separate repo should contain:

- A `kustomization.yaml` at `flux_manifests_repo_path` (e.g. at repo root or under `tenants/overlays/...`).
- SOPS-encrypted files (e.g. `secrets-env.sops.yaml`) and a `.sops.yaml` that references your age **public** key.
- The same age key pair: **public** key in the repo for `sops --encrypt`; **private** key provided via `flux_sops_age_key_file` so this role can create the `sops-age` secret.

## References

- [Flux installation](https://fluxcd.io/flux/installation/)
- [Flux: Manage Kubernetes secrets with SOPS](https://fluxcd.io/flux/guides/mozilla-sops/) (age)
- [Capacitor – Flux UI](https://github.com/gimlet-io/capacitor)

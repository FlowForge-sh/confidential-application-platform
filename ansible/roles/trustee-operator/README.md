# Trustee Operator + Trustee (KBS) Role

Installs the [Trustee Operator](https://github.com/confidential-containers/trustee-operator) and deploys **production Trustee (Key Broker Service)** for CoCo attestation, as documented in the trustee-operator repo. Full integration with the existing CoCo setup: attestation is ready by default.

## What is KBS?

**KBS = Key Broker Service.** In Confidential Containers (CoCo), the implementation is **Trustee**.

- **Role**: Attestation and key delivery for CoCo workloads. TEE pods attest to the KBS and receive keys (e.g. for image decryption or app secrets).
- **Trustee Operator**: Manages Trustee (KBS) in the cluster. This role installs the operator and deploys one production KBS instance (ConfigMaps, Secrets, KbsConfig) per the repo’s [microservices sample](https://github.com/confidential-containers/trustee-operator/tree/main/config/samples/microservices).
- **CoCo integration**: CoCo’s attestation agent uses the in-cluster Trustee (KBS) by default. No extra configuration needed for attestation.

## When this role runs

Only when **CoCo** and **Trustee** are enabled: `enable_confidential_containers` and `enable_trustee_operator`.

## SNP measurement rollover

For Kata/QEMU/firmware upgrades, use the dedicated rollover playbook and runbook:

- Playbook: `ansible/playbooks/apply-trustee-snp-rollover.yml`
- Runbook: `docs/TRUSTEE-SNP-MEASUREMENT-ROLLOVER.md`

This supports:

- `merge` mode for temporary `old + new` measurement allowlists during rolling upgrades
- `replace` mode to remove stale measurements after rollout convergence

## What this role does

1. Clones the trustee-operator repo (tag from `trustee_operator_version`).
2. Installs the operator with `kubectl apply -k config/default` (CRDs + controller in `trustee-operator-system`).
3. Waits for the controller to be Running.
4. Deploys **production Trustee (KBS)**:
   - Generates Ed25519 auth keys (openssl).
   - Applies `config/samples/microservices` (KbsConfig + ConfigMaps/Secrets: KBS, AS, RVPS, attestation policy, resource policy, reference values).
   - Applies strict attestation and strict resource policy templates (measurement/TCB allowlists + strict per-resource path + attested image/init-data + namespace/service-account identity binding).
   - Applies storage-secret manifests directly from in-memory template rendering (no temporary plaintext secret files on disk).
   - Waits for the Trustee (KBS) deployment to be Running.

CoCo attestation uses this KBS out of the box (in-cluster service in `trustee-operator-system`).

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `trustee_operator_version` | v0.5.0 | Git tag to clone |
| `trustee_operator_image_tag` | v0.5.0 | Controller image tag |
| `trustee_operator_namespace` | trustee-operator-system | Operator and KBS namespace |
| `trustee_operator_clone_path` | /tmp/trustee-operator | Clone path |
| `trustee_operator_wait_timeout` | 120 | Seconds to wait for operator |
| `trustee_kbs_deployment_mode` | microservices | microservices \| all-in-one |
| `trustee_kbs_wait_timeout` | 180 | Seconds to wait for KBS deployment |
| `trustee_snp_allowed_measurements` | (repo default list) | Approved SEV-SNP launch measurement(s) (hex) |
| `trustee_snp_allowed_tcb_bootloader` | (repo default list) | Approved SNP bootloader SVN values |
| `trustee_snp_allowed_tcb_microcode` | (repo default list) | Approved SNP microcode SVN values |
| `trustee_snp_allowed_tcb_snp` | (repo default list) | Approved SNP firmware SVN values |
| `trustee_snp_allowed_tcb_tee` | (repo default list) | Approved SNP TEE SVN values |
| `trustee_snp_allowed_container_images` | (repo default list) | Approved attested container image references from init-data claims |
| `trustee_snp_allowed_init_data_hashes` | (repo default list) | Approved init-data SHA-256 digests used when runtime token paths omit parsed `init_data_claims` |
| `trustee_kbs_resource_bindings` | (repo default map) | Per-resource repository/tag bindings plus allowed images, init-data hashes, namespaces, and service accounts enforced by KBS resource policy |
| `trustee_kbs_storage_secrets` | (env/vault supplied) | Per-resource storage seeds; initial creation requires 64-hex values from vault/secure env, while later re-runs may omit a seed only if the Secret already exists in-cluster |

The rendered attestation policy is fail-closed for SNP key release: attestation must match approved launch measurements, approved TCB allowlists, and approved workload identity from init-data (parsed image claims and/or allowlisted init-data digest).  
The rendered KBS resource policy is also fail-closed on requested resource path and requester workload identity (allowed images/init-data digests plus attested namespace/service-account claims).
Tenant overlays should still enforce path-scoped KBS egress via Cilium L7 rules as an independent network-layer control.

## KBS service URL

Trustee (KBS) is exposed in-cluster via `kbs-service` (e.g. `http://kbs-service.trustee-operator-system.svc.cluster.local:8080`). For image encryption or custom workloads, use the KBS service in `trustee-operator-system`; see [IMAGE-ENCRYPTION.md](../../../docs/IMAGE-ENCRYPTION.md).

## Requirements

- Runs on the primary master (patched kubeconfig at `/root/.kube/config`).
- `git`, `kubectl`, and `openssl`.

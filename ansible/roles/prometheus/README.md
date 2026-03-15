# Prometheus role

Installs **Prometheus Operator** and exporters only (no kube-prometheus-stack, no Grafana/Alertmanager). If you had the full kube-prometheus-stack before, **wipe the monitoring namespace manually** (uninstall the stack, delete the namespace, recreate it) before running this role; see comment in `tasks/main.yml`.

## Metrics sources

| Source | How |
|--------|-----|
| **node-exporter** | Helm chart with ServiceMonitor |
| **kube-state-metrics** | Helm chart with ServiceMonitor |
| **blackbox-exporter** | Helm chart with ServiceMonitor |
| **cAdvisor** | Additional scrape: kubelet `:10250/metrics/cadvisor` |
| **kubelet** | Additional scrape: kubelet `:10250/metrics` |
| **Cilium/Hubble** | Cilium ServiceMonitor (playbook re-applies Cilium with `cilium_enable_service_monitor: true`) |
| **Caddy** | No ServiceMonitor (Caddy does not expose Prometheus metrics by default) |
| **Longhorn** | ServiceMonitor applied by Longhorn role (longhorn-manager) |

**Optional / not included:** containerd-prom-exporter (separate DaemonSet if needed), Kata/CoCo runtime metrics (exposed by operators when enabled). etcd metrics can be added via static scrape to the master node if required.

## RCA: kubelet / node-exporter / cAdvisor failing

**Root cause:** Prometheus runs in the cluster and scrapes **node IPs** (kubelet `:10250`, node-exporter `:9100`). That traffic goes pod → node; if the **host firewall (UFW)** does not allow 10250/tcp and 9100/tcp on the **internal interface**, connections are refused or time out.

**Fixes applied:**

1. **Firewall (firewall role)**  
   Allow on the internal interface only: **10250/tcp** (kubelet metrics + cAdvisor) and **9100/tcp** (node-exporter). Same pattern as 6443, 8472, 4244.

2. **K3s and cAdvisor**  
   K3s uses the standard kubelet; it exposes `/metrics` and `/metrics/cadvisor` on **10250** (same as upstream). No separate cAdvisor exporter is needed.

3. **Additional scrape config relabel**  
   Use **`__meta_kubernetes_node_address_InternalIP`** (capital `I` in `InternalIP`). Using `internalip` produced empty `__address__` and "dial tcp :10250: connection refused".

4. **Stack kubelet ServiceMonitor**  
   The operator chart deploys `prometheus-operator-kube-p-kubelet`, which produced targets with empty address. The role deletes that ServiceMonitor and relies on the additional scrape config for kubelet/cadvisor only.

If one node still times out (e.g. worker), check that 10250 and 9100 are allowed on that node’s internal interface and that pod→node traffic is not blocked elsewhere (e.g. Cilium policy).

## Order

Runs **after** the Cilium (CNI) role. The playbook then re-applies Cilium with `cilium_enable_service_monitor: true` so Cilium’s ServiceMonitors exist.

## Remote write credentials

Either:

1. **SOPS-encrypted file** in group_vars: set `monitoring_credentials_sops_file` to the path to a SOPS-encrypted YAML (e.g. `inventory/group_vars/all/monitoring_remote_write.yml.enc`) with:
   - `url`: full remote write URL (e.g. `https://grafana-ironsight.flowforge.sh/prometheus/api/v1/write`)
   - `username`: basic auth user
   - `password`: basic auth password

2. **Vars** (group_vars or `-e`): set `prometheus_remote_write_url`, `prometheus_remote_write_username`, `prometheus_remote_write_password`.

## Variables

- `prometheus_namespace`: namespace (default: `monitoring`).
- `prometheus_operator_release_name`, `prometheus_operator_chart_version`: operator Helm release.
- `prometheus_remote_write_secret_name`: K8s secret name for remote write basic auth (default: `prometheus-remote-write-basic-auth`).
- `monitoring_credentials_sops_file`: path to SOPS-encrypted credentials file (optional).

## Toggle

Controlled by `enable_monitoring` in group vars (default: `true`).

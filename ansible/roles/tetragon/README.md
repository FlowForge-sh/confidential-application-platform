# Tetragon role

Installs [Tetragon](https://tetragon.io/) (eBPF-based security observability and runtime enforcement) on all cluster nodes via the Cilium Helm chart. Exports metrics to Prometheus and events to Loki (via Promtail pod logs).

## Requirements

- K3s cluster with containerd at `/run/k3s/containerd/containerd.sock`
- Prometheus Operator (ServiceMonitor CRD) for metrics
- Promtail (optional) for event logs: Tetragon exports JSON events to stdout by default; Promtail collects pod logs from all namespaces, so events appear in Loki under `namespace="kube-system"`, `app_kubernetes_io_name="tetragon"` (export-stdout container).

## What this role does

- Adds Cilium Helm repo and installs `cilium/tetragon` in `kube-system`
- Installs the **tetra** CLI on the control node (`/usr/local/bin/tetra`) for querying Tetragon (e.g. `tetra getevents`, `tetra status`). Version is set by `tetragon_tetra_cli_version` (default `v1.6.0`; override in group_vars).
- Enables CRI for pod/container association (K3s containerd socket)
- Enables Prometheus metrics (ports 2112 agent, 2113 operator) and ServiceMonitor so the cluster Prometheus Agent scrapes them
- Enables process credentials visibility (for SUID, file capabilities, fileless/deleted binary observability)
- Applies observability TracingPolicies from the [Tetragon policy library](https://tetragon.io/docs/policy-library/observability/): privileges-raise, bpf, modules, library, sshd, egress (with cluster/service CIDR from group_vars)

## Metrics

- **Tetragon agent**: port 2112
- **Tetragon operator**: port 2113

ServiceMonitors are created when `tetragon_prometheus_service_monitor_enabled` and `tetragon_operator_prometheus_service_monitor_enabled` are true (default).

## Event export to Loki

Default: **stdout** export. The Tetragon DaemonSet includes an export-stdout sidecar that writes JSON events to stdout. Promtail collects these as normal pod logs. In Loki, query for example:

- `{namespace="kube-system", app_kubernetes_io_name="tetragon"}` and filter by container name for the export container.

Optional: set `tetragon_export_mode: file` and `tetragon_export_host_path` to write events to a host path; then configure Promtail (e.g. `promtail_scrape_tetragon_file: true`) to scrape that file for a dedicated `job="tetragon"` stream.

## Observability policies applied

| Policy | Description |
|--------|-------------|
| privileges-raise | Setuid/capset/user-namespace privilege escalation |
| bpf | eBPF program loads and BPFFS interactions |
| modules | Kernel module loading |
| library | Shared library loading |
| sshd | Omitted (policy uses API not in Tetragon 1.6; add when compatible) |
| egress | Outbound connections outside cluster/service CIDR |

Binary execution in `/tmp`, sudo, SUID/file-caps/fileless/deleted binaries use default process execution visibility (no separate TracingPolicy); enable process credentials in the role (default) for full visibility.

## Variables

See `defaults/main.yml`. Key overrides: `tetragon_chart_version`, `tetragon_tetra_cli_version` (tetra CLI binary on control node), `tetragon_cri_socket_host_path`, `tetragon_export_mode`, `tetragon_apply_observability_policies`.

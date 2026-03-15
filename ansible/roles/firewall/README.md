# Firewall role (iptables)

Configures a **source-based** firewall with iptables. Internal cluster ports are allowed only from the private network (vSwitch) and pod CIDR, not from the public internet.

## Why source-based, not interface-based

Allowing by interface (e.g. "allow on enp7s0") does **not** restrict by source: it allows traffic that **arrives on** that interface from **anywhere**. This role uses rules like `-s CIDR -p proto --dport X -j ACCEPT` so only traffic from allowed CIDRs is accepted for internal ports.

## Control plane (masters): internet-facing ports

From the **internet**, only these ports are open on the control plane:

- **22/tcp** — SSH. Restrict to admin IP(s) in production: set `firewall_ssh_allowed_cidrs: ["YOUR_IP/32"]`.
- **443/tcp** — HTTPS (Caddy ingress), when `firewall_allow_ingress_ports: true`.

HTTP (80) is **not** opened on masters by default; the playbook sets `firewall_allow_http_ingress: false` so the control plane exposes only 22 and 443 to the internet. All other host ports (6443, 10250, VXLAN, metrics, etc.) are allowed only from `firewall_internal_cidrs` (vSwitch + cluster CIDR), not from the internet.

## Public (when enabled)

- **80/tcp** — Only if `firewall_allow_http_ingress: true` (e.g. HTTP-01 ACME); not used on control plane by default.

## Private (from vSwitch + cluster CIDR only)

Allowed only from `firewall_internal_cidrs` (default: `firewall_private_network_cidr` + `cluster_cidr`):

- 6443/tcp — Kubernetes API  
- 10250/tcp — kubelet  
- 8472/udp, 4789/udp — Cilium VXLAN  
- 51871/udp — Cilium WireGuard  
- 4240/tcp — Cilium health API  
- 4244/tcp — Hubble gRPC  
- 9100/tcp — node-exporter  
- 9962, 9963, 9965/tcp — Cilium/Hubble metrics  
- ICMP — node-to-node health probes (internal CIDRs only)

## Variables (see defaults/main.yml)

- **firewall_private_network_cidr** — vSwitch / node network (e.g. Hetzner private `10.0.0.0/16`). Override to match where `private_ip` lives.
- **firewall_internal_cidrs** — List of CIDRs for internal ports; default `[firewall_private_network_cidr, cluster_cidr]`.
- **firewall_ssh_allowed_cidrs** — If non-empty, SSH allowed only from these CIDRs (e.g. `["203.0.113.50/32"]`). Empty = allow 22 from anywhere.
- **firewall_allow_ingress_ports** — When true, allow 443 from anywhere (masters with Caddy). Set false on workers.
- **firewall_allow_http_ingress** — When true, allow 80 from anywhere (default false).
- **firewall_iptables_persist** — When true (default), install a systemd unit that re-applies iptables on boot.

## How it works

The role deploys `/usr/local/bin/firewall-ansible-iptables.sh`, which:

1. Creates and fills the **ANSIBLE-FIREWALL** chain with the allow rules (internal CIDRs, SSH, 443/80).
2. Sets INPUT policy to DROP, flushes INPUT, then appends: ESTABLISHED/RELATED accept, loopback accept, jump to ANSIBLE-FIREWALL.

Re-runs are idempotent (script flushes and rebuilds the chain and INPUT). With `firewall_iptables_persist` enabled, a systemd oneshot runs the script at boot after `network-pre.target`.

## Production hardening

- Set `firewall_private_network_cidr` to your actual vSwitch CIDR.
- Set `firewall_ssh_allowed_cidrs: ["YOUR_ADMIN_IP/32"]`.
- Keep only 443 (and optionally 22 restricted) public; do not open 80 unless required.

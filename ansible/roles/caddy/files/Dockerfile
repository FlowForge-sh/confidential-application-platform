# Caddy with Cloudflare DNS plugin (ops ACME DNS-01) and caddy-l4 (tenant SNI passthrough).
# Built on the control plane by the Ansible role.
# Update process: bump CADDY_VERSION/CADDY_L4_VERSION in caddy/defaults/main.yml, re-run the role.
ARG CADDY_VERSION=2.10.0
ARG CADDY_L4_VERSION=latest
FROM caddy:${CADDY_VERSION}-builder AS builder

# caddy-l4: L4 SNI passthrough for tenant hostnames
# caddy-dns/cloudflare: ACME DNS-01 for ops hostnames (cert issuance only, not tenant certs)
RUN xcaddy build \
    --with github.com/mholt/caddy-l4@${CADDY_L4_VERSION} \
    --with github.com/caddy-dns/cloudflare@master

FROM caddy:${CADDY_VERSION}-alpine

COPY --from=builder /usr/bin/caddy /usr/bin/caddy

---
name: mmo-ecommerce-multichannel
description: Use when MMO ecommerce operations need multi-store listing sync, master SKU management, order routing, inventory deduplication, and automated fulfillment across Shopee, TikTok Shop, Lazada, and similar platforms.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Run multi-store ecommerce automation that treats inventory as a single source of truth across all channels.

## Mandatory scope checks
- define Master SKU registry: one Merchant SKU maps to all platform-specific SKU variants
- define real-time inventory sync: deduct from master pool on any channel sale, propagate to all others within SLA
- define buffer stock policy per SKU per platform: minimum reserve to prevent oversell during flash sales
- define listing bulk-upload workflow: field mapping, image processing, platform-specific requirements
- define order routing: auto-confirm, label generation, logistics partner connection
- define exception handling: oversell recovery, out-of-stock notification, return and refund routing

## Evidence contract
- include SKU mapping registry showing coverage across all active stores
- include inventory sync test: sale on platform A → stock update on platform B within SLA
- include order routing trace for one complete fulfillment cycle

## Role
- mmo-ecommerce-ops

## Layer
- layer-4-specialists-and-standalones

## Inputs
- store inventory across all platforms (Shopee, TikTok Shop, Lazada, Shopify, etc.)
- platform API credentials and endpoint capabilities
- logistics partner integration endpoints and supported label formats

## Outputs
- multi-channel ecommerce automation plan: SKU master design, sync rules, order routing, fulfillment automation, and operational runbook

## Reference skills and rules
- Always use official marketplace APIs for inventory sync — scraping-based sync desynchronizes under flash sale load.
- Buffer stock is mandatory for any SKU involved in flash sales, voucher campaigns, or live-stream selling.
- Master SKU is the single source of truth — mutations must go through the master registry, not individual platform portals.
- Test oversell prevention explicitly before any high-traffic campaign.
- Open `references/mmo-ecommerce-multichannel-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-ecommerce-multichannel-good-output.md` and `examples/mmo-ecommerce-multichannel-bad-output.md` to calibrate output quality.
- Use `evals/mmo-ecommerce-multichannel-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-ecommerce-multichannel-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- mmo-http-api-automation
- mmo-cloud-operations-automation
- mmo-lowcode-automation
- automation-ops
- qa-governor

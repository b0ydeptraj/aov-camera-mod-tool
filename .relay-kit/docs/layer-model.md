# layer-model

This repo follows a 4-layer hub-and-spoke topology so orchestration and execution are separate concerns.

## layer-1-orchestrators
Coordinate the whole system, choose the active lane, and keep shared state current.

- workflow-router
- bootstrap
- team
- cook

## layer-2-workflow-hubs
Run repeatable multi-step workflows and hand off to the right specialist or utility provider.

- brainstorm-hub
- scout-hub
- plan-hub
- debug-hub
- fix-hub
- test-hub
- review-hub

## layer-3-utility-providers
Stateless capabilities and analysis helpers. These should be called by hubs or orchestrators rather than acting as long-lived owners of work.

- research
- doc-pointers
- sequential-thinking
- problem-solving
- multimodal-evidence
- browser-inspector
- repo-map
- memory-search
- release-readiness
- accessibility-review
- skill-gauntlet
- signal-calibration
- impact-radar
- runtime-doctor
- migration-guard
- token-economy
- context-continuity
- handoff-context
- mermaid-diagrams
- ux-structure
- media-tooling

## layer-4-specialists-and-standalones
Role specialists, native support skills, and domain standalones that actually produce architecture, stories, code, and quality evidence.

- analyst
- pm
- architect
- scrum-master
- developer
- qa-governor
- go-service-engineering
- next-product-frontend
- growth-marketing
- market-research
- automation-ops
- vietnamese-product-localization
- mmo-reup-automation
- mmo-account-operations
- mmo-browser-fleet-automation
- mmo-social-marketing-automation
- mmo-lowcode-automation
- mmo-mobile-app-automation
- mmo-cloud-operations-automation
- mmo-http-api-automation
- execution-loop
- project-architecture
- dependency-management
- api-integration
- data-persistence
- testing-patterns

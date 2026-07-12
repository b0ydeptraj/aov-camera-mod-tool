# hub-mesh

Workflow hubs are allowed to call across the mesh when the current lane hits ambiguity, risk, or missing evidence.

## Cross-hub references

### brainstorm-hub
Can hand off to:
- plan-hub
- workflow-router

### scout-hub
Can hand off to:
- plan-hub
- debug-hub
- review-hub
- workflow-router

### plan-hub
Can hand off to:
- brainstorm-hub
- scout-hub
- fix-hub
- review-hub
- workflow-router

### debug-hub
Can hand off to:
- fix-hub
- test-hub
- scout-hub
- workflow-router

### fix-hub
Can hand off to:
- debug-hub
- test-hub
- review-hub
- workflow-router

### test-hub
Can hand off to:
- debug-hub
- fix-hub
- review-hub
- workflow-router

### review-hub
Can hand off to:
- plan-hub
- debug-hub
- fix-hub
- test-hub
- workflow-router

## Recommended support map

### brainstorm-hub
- analyst
- pm
- research
- market-research
- growth-marketing
- mmo-social-marketing-automation
- mmo-reup-automation
- ux-structure

### scout-hub
- project-architecture
- dependency-management
- api-integration
- data-persistence
- testing-patterns
- doc-pointers
- repo-map
- memory-search
- impact-radar
- runtime-doctor
- token-economy
- context-continuity
- handoff-context

### plan-hub
- analyst
- pm
- architect
- scrum-master
- research
- market-research
- growth-marketing
- mmo-reup-automation
- mmo-account-operations
- mmo-social-marketing-automation
- mmo-lowcode-automation
- mmo-cloud-operations-automation
- mmo-http-api-automation
- impact-radar
- token-economy
- context-continuity
- ux-structure
- mermaid-diagrams

### debug-hub
- developer
- testing-patterns
- problem-solving
- sequential-thinking
- browser-inspector
- multimodal-evidence
- memory-search
- runtime-doctor

### fix-hub
- developer
- go-service-engineering
- next-product-frontend
- mmo-account-operations
- mmo-browser-fleet-automation
- mmo-mobile-app-automation
- mmo-http-api-automation
- execution-loop
- project-architecture
- api-integration
- data-persistence
- accessibility-review
- token-economy
- handoff-context

### test-hub
- qa-governor
- testing-patterns
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
- multimodal-evidence
- release-readiness
- accessibility-review
- skill-gauntlet
- signal-calibration
- impact-radar
- runtime-doctor
- migration-guard
- token-economy
- context-continuity
- media-tooling

### review-hub
- qa-governor
- testing-patterns
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
- project-architecture
- doc-pointers
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
- mermaid-diagrams

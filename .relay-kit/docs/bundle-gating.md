# bundle-gating

Runtime gating keeps lower bundles from spraying higher-level artifacts by accident.

| Bundle | Contracts emitted | Docs emitted | References emitted |
|---|---|---|---|
| core | core base only | core docs only | support references |
| orchestration | core base + orchestration extras | core + orchestration docs | support references |
| utility-providers | none by default | utility and topology docs | none |
| discipline-utilities | none by default | discipline docs only | none |
| runtime | core base + orchestration extras + runtime extras | core + orchestration + runtime docs | support references |
| baseline | runtime scope + approved discipline utilities | runtime docs | support references |
| enterprise | baseline scope + full discipline utilities | runtime + discipline + enterprise docs | support references |

Use temporary output directories when you need to prove gating behavior without contamination from prior generated files.

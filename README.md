# Polyfork assets

Optional, independent `polyfork-assets` Skill for searching and inspecting
Polyfork assets, acquiring one confirmed public free GLB, and reusing a verified
project-local cache without another HTTP request. No SDK or MCP installation.

## Use

Read [the Skill](skill/polyfork-assets/SKILL.md) and the current provider terms
before acquiring an asset. From a reviewed checkout, an optional installer can
discover `skill/polyfork-assets`; installation is a separate user action.

```text
python skill/polyfork-assets/scripts/polyfork_assets.py search --query camper --limit 3
python skill/polyfork-assets/scripts/polyfork_assets.py inspect camper-van-8d10e2
python skill/polyfork-assets/scripts/polyfork_assets.py fetch camper-van-8d10e2 --project-dir <existing-private-project>
```

The cache stays in the authorized private project, not this repository. Repeat
fetch verifies its hash and returns zero HTTP requests / zero downloads. Paid,
login-required or unconfirmed items fail closed. No bulk download, module
execution, persistent MCP grant or asset redistribution is implemented.

## Develop

Tool versions live in `vx.toml`; tasks live only in lowercase `justfile`.

```text
vx just check
vx just discover
```

`check` runs offline regression and layout tests, including acquisition/cache
reuse against synthetic fixtures. `discover` runs the pinned installer in
**list-only** mode; it does not install a Skill. Neither command downloads a
Polyfork asset. Python helpers use only the standard library. Blender is optional
and is never installed or launched by these tasks or CI.

[Prior native validation](skill/polyfork-assets/references/native-validation.md)
records one Blender 5.1.1 import/export/reopen test; it does not attest GUI,
animation, other DCCs or a complete rendered scene. Migration tests do not repeat
that native acceptance or establish fresh provider entitlement.

## Source and rights

Original code and instructions are MIT; retain [LICENSE](LICENSE). Polyfork
models/modules/imagery are not included and retain their
[custom terms](https://polyfork.dev/licensing). Free access does not mean open
source or redistribution permission. This project is an independent integration,
not a claim of provider affiliation.

[Source history](docs/source-history.json) pins the original agent-plugins commit
and each migrated Git blob. This repository is the single implementation; the
agent-plugins marketplace only references it.

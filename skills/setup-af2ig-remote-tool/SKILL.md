---
name: setup-af2ig-remote-tool
description: "Set up, validate, or troubleshoot AlphaFold 2 initial-guess (dl_binder_design) as a ToolUniverse remote tool; use for deployment or runtime issues, with optional Connect relay."
---

# Set up AF2 initial guess (dl_binder_design) as a remote tool

> Validation status (2026-10-01): af2ig — the `af2_initial_guess` step of nrbennet/dl_binder_design at commit `cafa3853`, AlphaFold 2 `model_1_ptm` re-predicting a designed binder–target complex from the complex itself as the structural initial guess — ran on the NVIDIA GB10 (aarch64, cc 12.1, driver 580.173.02) under the optimization kit's `off` mode. **Read what this is before reading anything else: "ig" is INITIAL GUESS, the input is a STRUCTURE and not a sequence, and the number it exists to produce is `pae_interaction` (angstroms; the field's working threshold is below 10).** All five `tu remote setup` steps are green and the acceptance suite passed: an ascending ladder, a mixed-shape phase, four consecutive identical requests, and a separate clean-worker run at the row the budget is declared on — an ascending ladder of 100 / 200 / 400 residues, a mixed-shape phase, four consecutive identical requests, a separate clean-worker run at 800 residues (the row the budget is declared on), and a two-rebuild engine test. **29 held-worker requests, 29 structures, 0 failures**, every one asserted to have written a `*_af2pred.pdb`. **THERE ARE NO PADDING BUCKETS HERE, which is the opposite of AlphaFold 3 and changes which half of the test carries the evidence**: this model compiles one XLA program per *exact* total residue count, so four identical requests exercise one program and the shape change is the whole test. Residency is worth **26x at its best rung and 1.7x at the row the budget is declared on** -- 95.0 s cold against 3.6 s held at 100 residues, and 272.1 s against ~163 s at 800. Plan with the second number; the first is the best case, and it is largest where a request is cheapest. Declared budget **6.0 GiB at 800 residues**, which is also the tool's input ceiling; the ladder is 0.5 / 1.0 / 2.0 / 6.0 GiB at 100 / 200 / 400 / 800 residues (reported), over a working set of 0.49 / 0.62 / 1.23 / 4.36 GiB (actual). Two cautions below are specific to this provider: its **VRAM figure is quantised** in a way a torch provider's is not, and its environment carries one named deviation from the kit's lock (`tensorflow` for `tensorflow-cpu`, because no aarch64 wheel of the latter exists). Public publication, cross-user isolation, concurrency, recovery and scientific quality are untested; keep this deployment private.

## Prerequisites

- Run from the ToolUniverse repository root on Linux with Python 3.12.3.
- A CUDA GPU is required. This provider holds its model resident between requests; CPU is not a target.
- Keep provider data, weights, caches, and credentials outside Git.
- Bind to loopback. A non-loopback bind requires TOOLUNIVERSE_API_TOKEN; never put it in arguments or results.

Run the standard-library contract check before downloading large dependencies:

~~~bash
python scripts/remote_validation/setup_skill_preflight.py --implementation af2ig
~~~

After exporting provider resources, add `--check-provider-env`. After the
server starts, add `--live` to verify the exact MCP tool set without running
the model. Before sharing, add `--check-connect-prereqs`; this reports only
whether a key is set and never prints its value.

## What this model is, and what it is not

This matters more here than for the folding providers beside it, because the
slug does not say it and the obvious guess is wrong.

- It is **not** AlphaFold 2 structure prediction from sequence. There is no
  sequence-only route and adding one would be a different model.
- The input is **one PDB file holding a complex**. Chain 1 is the binder and
  every chain after it is the target — dl_binder_design's own convention.
  Getting the order backwards does not fail; it silently scores the wrong
  interface. A single-chain file is predicted as a monomer and the interface
  scores come back null.
- **No MSA is built and no service is contacted.** The "alignment" is the query
  sequence by itself (`make_msa_features(msas=[[seq]])`, `max_msa_clusters =
  5`) and the template is generated from the input coordinates. There is
  nothing to precompute, nowhere to send a request, and no MSA server to
  configure — unlike colabfold, where that is the central question.
- **The seed is upstream's and is fixed.** `jax.random.PRNGKey(0)` and
  `random_seed=0` are literals in the driver; there is no seed argument, so
  this tool exposes none. One input has one answer.
- `num_recycle` and `initial_guess` are **compile-time**: they are baked into
  `model_config` before the jitted function is built, so changing either
  rebuilds the held model. The reply says `config_rebuilt` when that happened.

## Create the two environments

This provider is on the remote-tool standard, so it has two environments, not
one: the MCP server runs in ToolUniverse's, and the model runs in its own,
built from a pinned lock. They cannot import each other, and that is the point.

~~~bash
python3 -m venv .venvs/af2ig
. .venvs/af2ig/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install fastmcp
~~~

The model half lives at the path `TOOLUNIVERSE_AF2IG_PYTHON` names, and nothing
above creates it. The kit pins **CPython 3.11.5**; create an empty interpreter
there first and let `tu remote setup --only environment` fill it from
`src/tooluniverse/remote/af2ig/environment/requirements.lock` with `--no-deps`,
so no version is silently resolved to something else:

~~~bash
python3.11 -m venv ~/af2ig-venv
~~~

Two things about this lock are worth knowing before it runs.

**The jax line is two years old and drives this card.** jax / jaxlib /
jax-cuda12-plugin / jax-cuda12-pjrt **0.5.3** was expected to be the blocker
for an AlphaFold-2-era kit on a Blackwell-class part, and it is not. `jaxlib`
publishes `manylinux2014_aarch64` wheels from 0.4.18 onward; 0.5.3 publishes
four of them and both CUDA companions publish aarch64 wheels too. Measured in
the model interpreter: `jax.default_backend()` is `gpu`, the device is
`CudaDevice(id=0)` with `device_kind` "NVIDIA GB10" and `compute_capability`
"12.1", a 2048×2048 float32 matmul is correct, and there is no PTX JIT message.
**An old pinned framework version is a question to measure against the index
and the card, never a conclusion to draw from the version number.**

**One line of the lock moved, and it is named.** `tensorflow-cpu` 2.21.0
publishes eight wheels and every one is x86-64 or Windows; there is no aarch64
wheel of that distribution at any version. The lock substitutes `tensorflow`
2.21.0 — the same release, whose `manylinux_2_27_aarch64` wheel is the CPU-only
build, because TensorFlow ships no aarch64 GPU artifact at all. The property
the kit pinned `-cpu` *for* is that TensorFlow must not touch the card while
JAX holds it, so that property is asserted rather than argued:
`[env] verify` checks `tf.config.list_physical_devices('GPU') == []`. The kit's
own `check_pins.py --gpu` therefore reports `tensorflow-cpu: not installed`,
and `[kit] install` permits **that one line and no other** — any second unmet
pin re-raises the kit's refusal with its exit code. It does not pass
`AF2IG_OPT_FORCE`, which would have suppressed every pin failure at once.

The rest is built by `tu remote setup`, which reads
`src/tooluniverse/remote/af2ig/provider.toml` and runs five steps: preflight,
environment, kit, weights, smoke. Each refuses by name and carries its fix.

~~~bash
export TOOLUNIVERSE_AF2IG_PYTHON=~/af2ig-venv/bin/python
export AF2_PARAMS=~/.af2ig
tu remote setup af2ig
~~~

Run one step at a time with `--only preflight|environment|kit|weights|smoke`
while bringing a machine up. The smoke step is the one that matters: it holds
the model, sends one request, asserts the provider produced what its manifest
says a successful run produces, and records the measured peak VRAM to
`~/.cache/tooluniverse/measured/af2ig.json`. A host schedules on that file.
Expect roughly 120 s on an idle card (114.5 s of it the request itself, peak reserved 1.0 GiB) for the smoke — almost all of it one XLA
compilation, not the fold.

Package/network-dependent commands must be rerun in a clean environment before marking this skill complete.

## Two paths this provider lays out that pip does not

**The patched upstream tree.** `AF2IG_DIR` names
`dl_binder_design/af2_initial_guess` inside a tree the **kit step produces**:
the pinned `cafa3853` archive unpacked and the kit's thirteen-diff series
applied. It is not an installed distribution, and `predict_pdb.py` — the
PyRosetta-free front end the whole provider runs through — is *created* by
patch `00_pdb_frontend_envport.diff` and exists nowhere else. The install puts
it at `~/.cache/tooluniverse/af2ig-stock/...` and the launcher defaults there,
so `AF2IG_DIR` only has to be exported if you keep the tree somewhere else.

It is laid out **outside** the kit checkout on purpose. `bash run.sh install`
unpacks it *inside*, and `step_kit` refuses a checkout with untracked content
it does not recognise — which it would do on the second run of a step the
standard requires to be idempotent. The install therefore does out of tree
exactly what `run.sh install` does in tree, with the kit's own archive, the
kit's own patch series and the kit's own `check_pins.py --checkout` verdict
(68/68 pinned files), and the checkout stays byte-identical to its pin.

**The weights.** `AF2_PARAMS` names the directory that **holds** `params/`, not
the `params/` directory and not the file; that is the kit's own convention and
getting it wrong is the commonest start-up refusal. The one file is
`params/params_model_1_ptm.npz`, 373,103,340 bytes, declared in the manifest
with its sha256. The kit's own fetcher streams DeepMind's
`alphafold_params_2022-12-06.tar` (5.6 GB, 16 members, CC BY 4.0) and keeps
only that member, so the other 5.2 GB never lands on disk. No URL is restated
in ToolUniverse. **One HEAD request against that URL was the first action taken
on this kit** — 89 ms, HTTP 200, `content-length: 5587968000`, which is the
kit's own declared byte count exactly. A complete and installable kit can have
no model to run; checking costs less than a tenth of a second.

## The one kit lever this provider engages, and why

`[kit] mode = "off"` -- no kit mode is resolved, the kit's CLI never runs,
nothing of `af2ig_opt` is imported, and nothing replaces upstream's loader,
which is what entitles the worker to hold the weights. On top of that, exactly
one of the kit's lever flags is passed to upstream's driver, and it is an
element of `[runtime] worker_args` in the manifest rather than a default, so the
argv you can read is the argv that runs:

~~~
-host_outputs      the kit's L6
~~~

It is there because of a measurement that overturned the estimate it replaced.
The place to read it is upstream's own per-design timers, not the wall clock. On
a **warm** 195-residue request under stock, `t_model` is 14-17 s and `t_output`
is 45-57 s; at 400 residues `t_output` is 88 s. The output step is numpy and
scipy walking a tree of jax **device** arrays and pulling each one lazily, op by
op -- on a held worker it is three times the model. Measured, fresh worker each:

| | cold | held |
| --- | --- | --- |
| stock | 311.0 s | 70.1 / 60.6 / 75.5 s |
| `-host_outputs` | 231.5 s | 13.3 / 12.8 s |

**And it is exact, which was checked rather than taken on trust.** Two ordinary
runs cannot check it: two *processes* disagree with each other anyway in the 5th
significant figure, because XLA's default autotuning picks algorithms by timing
them. Under the kit's own deterministic recipe (`--det 1`, i.e.
`XLA_FLAGS=--xla_gpu_autotune_level=0`) three routes produce one file --
`sha256 81d69b99410824b7fad9ca5a9b9134d8e52f789580fe5202d1ce74ca8e70dc89` --
and they are the kit's own `run.sh pred --mode off --det 1`, this worker stock,
and this worker with the flag.

**What is declined, and why each is a measurement rather than a preference.**
L7 `-precompile`, L13 `-program_cache`, L15 `-prefetch`, L16
`-overlap_output` and U1 `-sort_by_length` all overlap work *across the inputs
of one campaign*; a resident worker serves one request at a time by contract, so
there is no next input to prefetch and no later design to write behind. L8, L10
and L11 go through the shared core's Pallas kernels, whose float32 tile tables
cover compute capability 8.0 and 9.0 only -- the kit's own README says the
triangle kernels are skipped on a capability without a row, and this card is
12.1. And L1 `-device_params`, the one that looks most obviously worth having,
is declined on a number: the per-call host-to-device transfer it removes is
355.7 MiB over 338 arrays and costs **2.4-6.2 ms** on this card's unified
memory, where there is no bus to cross.

## Residency, and the two numbers to quote

| | cold | held | gain |
| --- | --- | --- | --- |
| 100 residues | 95.0 s | 3.6 s | **26x** |
| 195 residues (the smoke) | 142.4 s | 6.3 s | 23x |
| **800 residues (the declared row)** | 272.1 s | 163.1 s | **1.7x** |

The multiple is largest where a request is cheapest, so a provider quoting only
its best rung tells a host the opposite of what it needs: the expensive requests
are the ones being scheduled around. What residency keeps, largest first: the
XLA executables (one per exact residue count, 90-270 s each to build, and
nothing persists them across a restart unless you point `AF2IG_JIT_ROOT`
somewhere lasting), XLA's per-process autotuning results, the 355.7 MiB
parameter tree, and TensorFlow's feature pipeline warm. **The weights are the
smallest of those** -- a fresh process reads them in 2.4-4.3 s -- so unlike the
large-checkpoint providers this one's residency argument is almost entirely the
compiler's. For the per-request-process comparison, the honest reference is the
kit's own CLI: `bash run.sh pred --mode off` on the same single input takes
281.0 s end to end, every time.

**Residency does not change the answer, and here that is falsifiable** because
upstream fixes the seed. Four identical 195-residue requests gave one sha256; a
100-residue request replayed after a 200-residue one gave the same file as the
cold 100; and a `num_recycle` 3 -> 5 -> 3 round trip, which rebuilds the held
model twice, came back byte-identical to where it started.

Wall times above are from a **contended** card (a sibling provider's build held
2.8-10.6 GB at 95% utilisation throughout), so they are upper bounds; the peaks
reproduced identically across two complete runs of the suite. The one idle
comparison: the 195-residue cold request is 114.5 s idle against 142.4 s
contended.

## Start and verify locally

~~~bash
python -m tooluniverse.remote.af2ig.af2ig_tool
~~~

The Streamable HTTP endpoint is http://127.0.0.1:8053/mcp. In a second activated shell run:

~~~bash
python - <<'PY'
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8053/mcp") as client:
        print([tool.name for tool in await client.list_tools()])

asyncio.run(main())
PY
~~~

Confirm discovery contains af2ig_predict; stop on empty, duplicate, or schema-drifted discovery.

## Authorize once, then share with one short command

After installing dependencies, exporting the provider resources above, and
installing the pinned relay SDK described under Connect below, run from the
repository root. Log in only once per machine (and again after key rotation):

~~~bash
tu remote login
# Or import an existing protected 0600 file without sourcing it:
tu remote login --env-file /path/to/tooluniverse-service.env
~~~

Then each private share is one short command:

~~~bash
tu remote share af2ig
~~~

By default, `tu remote login` requests a short-lived device code, opens the
TU Platform approval page, and polls until the signed-in user approves. No key
copy/paste is required. On a headless machine, add `--no-browser` and open the
printed link elsewhere. The CLI exchanges the approval for a computer-only key,
verifies `/remote-servers/preflight`, stores it in a local 0600 config file, and
never displays it.

The share command runs environment and TU Platform preflights, starts or reuses
the exact loopback endpoint, validates discovery, and keeps the relay in the
foreground until Ctrl-C. It automatically uses the reviewed Python, name, and
worker count. Override them only when needed:

~~~bash
tu remote share af2ig --name my-af2ig-remote --workers 1
~~~

Use `tu remote check af2ig` for a non-sharing readiness check and
`tu remote run af2ig` for a local-only foreground server.

In an interactive terminal, sharing automatically starts the same browser flow
when the key is missing, expired, or revoked. A malformed or revoked explicit
`TOOLUNIVERSE_SERVICE_KEY` fails fast instead of being silently replaced; unset
or correct it, then run `tu remote login`. Non-interactive jobs also fail fast.
Use `tu remote logout` to remove only the local copy. Use `tu remote logout --revoke` to revoke the computer-only platform connection first; the server record remains offline for owner inspection.

## Connect to ToolUniverse Connect

The `tuplatform-connect` relay is not yet published on PyPI. Install the reviewed public wheel below; its SHA-256 is pinned. Interactive sharing uses browser device authorization, so no key copy/paste or GitHub access is required.

~~~bash
python -m pip install fastmcp pyyaml "tuplatform-connect @ https://connect.aiscientist.tools/downloads/tuplatform_connect-0.3.0-py3-none-any.whl#sha256=3fad5eee5ecf7887a693d93ccd1aa112dc0955617a885d1fc3daded0030f9ae0"
tu doctor --forward http://127.0.0.1:8053/mcp --json
tu serve --share --forward http://127.0.0.1:8053/mcp --name validation-af2ig --workers 1
~~~

Prefer browser device authorization. For CI or migration, supply
`TOOLUNIVERSE_SERVICE_KEY` only through a protected environment or use
`tu remote login --manual-key`; never put a key in shell arguments.

This implementation was added after the authenticated 2026-08-16 Platform
matrix and was not part of it. That matrix imported each implementation it
covered as unpublished owner drafts and invoked them through
`/expert-sessions/{id}/test`; this provider was imported as no such draft and
invoked through no such route. It has not been exercised through the Platform
at all: the evidence above is local, on one card, through the loopback
endpoint. Public publication, independent-caller authorization/isolation,
saturation, and persistent supervision are untested.

## Run a verified example

Operation: af2ig_predict

The input is a STRUCTURE, which is what makes this provider unlike the folding
ones beside it. `src/tooluniverse/remote/af2ig/smoke/input.pdb` is the kit's own
smallest public input — barstar (87 residues, chain A, the binder role) against
barnase (108 residues, chain B) from PDB 1BRS, 195 residues in all, wwPDB CC0.

The example below is a **ten-residue excerpt of each of those two chains,
N/CA/C/O only**, which is enough for upstream's parser and its template
builder. It is short enough to put in a document and it runs; its scores are
not a design worth interpreting. The scientifically meaningful call is the
195-residue smoke file in the snippet after it.

The complete runnable request is in [the verified example JSON](references/af2ig-example.json). Read it only when running this example.

Load the packaged JSON example and invoke it through the live local MCP
endpoint:

~~~bash
python - <<'PY'
import asyncio
import json
from fastmcp import Client

async def main():
    with open("skills/setup-af2ig-remote-tool/references/af2ig-example.json") as example:
        arguments = json.load(example)
    async with Client("http://127.0.0.1:8053/mcp") as client:
        result = await client.call_tool("af2ig_predict", arguments)
        print(result)

asyncio.run(main())
PY
~~~

The scientifically meaningful call, with the shipped 195-residue complex:

~~~bash
python - <<'PY'
import asyncio
from fastmcp import Client

async def main():
    pdb = open("src/tooluniverse/remote/af2ig/smoke/input.pdb").read()
    async with Client("http://127.0.0.1:8053/mcp") as client:
        result = await client.call_tool(
            "af2ig_predict", {"structure": pdb, "return_structure": False}
        )
        print(result)

asyncio.run(main())
PY
~~~

Expected success shape: `pae_interaction` as a number, a `scores` object
carrying upstream's own nine columns (`plddt_total`, `plddt_binder`,
`plddt_target`, `pae_binder`, `pae_target`, `pae_interaction`,
`binder_aligned_rmsd`, `target_aligned_rmsd`, `time`), a `structure_path` on
the host, and `weights_held_by = "worker"`. The predicted PDB text is opt-in
(`return_structure`) because it is hundreds of kilobytes; the scores come back
either way, and they are the thing a filter reads. Check scientific meaning,
output bounds, invalid-input behavior, and absence of paths, secrets, and
traces.

**This example was executed, not written down.** Through the live endpoint on
port 8053: discovery returned `['af2ig_predict']`, and the call returned

~~~
pae_interaction 21.4196   plddt_binder 80.72   plddt_target 64.48
binder_aligned_rmsd 5.26  target_aligned_rmsd 56.54
n_residues 20  n_chains 2  binder_length 10  monomer false
kit_mode "off"  weights_held_by "worker"  peak_reserved_gib 0.5
~~~

in **85.4 s cold and 1.1 s on the held replay**, and with
`return_structure=true` a 12,127-byte PDB of 152 lines. Those scores are what a
20-residue pair of chain fragments deserves (a 56 A target RMSD says the two
fragments did not stay together) and they are not a design verdict; the shipped
195-residue complex is the call to judge the provider by.

Running it is also what found a defect worth naming, because it is the kind a
reader cannot see: the reply used to carry a `structure_path`, and that path
pointed inside the per-request temporary directory the server deletes before it
answers. The field is gone. `return_structure` is now the only route to the
bytes, and the schema says so.

## Tune GPU and concurrency

- Use one worker. The resident worker serves one request at a time by design; a second in-flight request queues on its lock rather than doubling peak VRAM.
- Read `vram_budget_gb` from the provider manifest and the measured file before co-tenanting anything else on the card. The figure is declared at the envelope it was measured at, and the tool refuses a complex above that envelope rather than letting it arrive as an out-of-memory.
- **A JAX provider's VRAM number is not the same kind of number as a torch provider's.** `peak_pool_bytes` — the analogue of torch's `max_memory_reserved` — moves in **powers of two**, so this provider's figure is a rounded-up allocator high-water mark being compared against a torch provider's near-exact one. Schedule on it as a ceiling, and do not read the gap between two rungs as headroom. (`peak_bytes_reserved` reads 0 on this stack and is a trap; the worker returns it verbatim beside the real one so you can see that.)
- `XLA_PYTHON_CLIENT_PREALLOCATE=false` is set by the launch and is load-bearing for scheduling, not for correctness: left at its default JAX takes 75% of the device up front and the reported peak becomes a measurement of that, not of the model. On the last JAX provider that was 91.22 GiB against a real 2.0 — 45x. A co-tenant arrangement that loses this variable loses the whole card.
- `OMP_NUM_THREADS=1` is also set by the launch, and the reason is this provider's own rather than copied: AlphaFold's feature pipeline runs inside TensorFlow in the same process, and TensorFlow brings up an intra-op thread pool in a worker that already has CUDA initialised. Nothing in the request path forks, so this is the cheapest guarantee that the state boltzgen stalled in cannot arise — not a fix for an observed stall.
- **THE COST IS PER EXACT LENGTH, NOT PER BUCKET, and that decides what to benchmark.** This model does not pad: `L = len(seq)` and the jit cache is keyed on shapes that are a pure function of it, so a complex one residue longer is a fresh XLA compilation of the whole forward pass. A campaign of one design length is the case this provider is fastest at, which is also the case binder design actually produces. A benchmark of a single cold call measures a compiler.
- Measure cold start, then **at least four consecutive identical requests**, then a mixed-shape sequence (small, small, large, small). Two warm calls of different shapes is not enough: openfold3 passed exactly that and still died on the second request of the same shape. For THIS provider the identical requests are the cheap half — one program is compiled once and replayed — so the shape change is where the real evidence is, and a `num_recycle` change is where the *rebuild* evidence is.
- Then parallel levels 1, 2, 4, 8, and only 16 if memory permits.
- Record successes/errors, p50/p95, peak RAM/VRAM, utilization, queueing, cancellation cleanup, and recovery.
- Increase workers only after single-flight initialization and sanitized recoverable OOM/timeout behavior are proven.

## Troubleshoot and clean up

| what you see | what it means | what to do |
| --- | --- | --- |
| `--params-dir ... holds no params/params_model_1_ptm.npz` | `AF2_PARAMS` points at the `params/` directory or at the file | point it at the directory that **holds** `params/`, then `tu remote setup af2ig --only weights` |
| `--af2ig-dir ... holds no predict_pdb.py` | the patched tree is absent; it is produced, not pip-installed | `tu remote setup af2ig --only kit` |
| `holds predict_pdb.py but no alphafold/model/modules.py` | the tree is half unpacked | remove it and re-run `--only kit` |
| `--mode ...: this worker implements the kit's stock route only` | `[kit] mode` was changed away from `off` | leave it at `off`; see provider.toml `[kit]` for the three reasons |
| `jax reports no GPU device` | the CUDA plugin did not load | re-run `--only environment`; note TensorFlow is CPU-only here **by design**, so asking it about the card gives the wrong answer |
| `the kit's pin check refused for a reason other than the one documented substitution` | a second pin is unmet | read the printed `check_pins:` lines; re-run `--only environment` |
| `weights_off_pin` | the file is absent, short, or a different digest | the named file is **left in place** rather than deleted, because a truncated transfer and a corrupt file look alike. Remove it by hand and re-run `--only weights` |
| `smoke_produced_nothing` | the model answered and wrote no structure | read `~/.cache/tooluniverse/remote-logs/af2ig-resident.log`; `check.point` is appended even for a request that raised, so a directory can hold bookkeeping and no result |
| every interface score is null | the input had one chain, or `force_monomer` was set | give the target as the chains after the binder |
| `The distance between residues N and N+1 is ... > limit 3.0 A` | normal and expected | upstream detected a chain break and inserted AlphaFold's +200 residue-index offset, exactly as it does for the kit's own tiled inputs |

- Read the refusal. Every step of `tu remote setup` names what is wrong and carries the fix; exit 3 is a refusal and exit 1 is a failure.
- This kit installs **no `.pth` and no import hook at all** — its own `pyproject.toml` says so, and its build backend confirms it by finding no `*_autoload.pth` to add. That is a sixth activation shape (argv only) and it is why this provider can hold the model: nothing of the kit replaces upstream's loader, so the worker legitimately may. It also means a stray `AF2IG_OPT` in your shell cannot kill the worker the way an undeclared `AF3_JAX_*` kills af3_jax's. The launcher strips those names anyway — every prefix under the kit's own `stock_environment.must_be_absent_prefixes`, read from `stock/PINS.json` rather than copied — because two of them (`JAX_COMPILATION_CACHE_DIR`, `JAX_PERSISTENT_CACHE_*`) would change what this provider *measures* without changing what it answers.
- Import/executable failure in the model half: re-run `tu remote setup af2ig --only environment`. It rebuilds from the lock with `--no-deps` and will not silently resolve a different version.
- 401/403 on deliberate network binding: configure matching TOOLUNIVERSE_API_TOKEN bearer auth; prefer loopback plus relay.
- Stop server/relay with Ctrl-C. If installed, run `tuplatform-service uninstall --name validation-af2ig`.
- A worker outliving its server is a known shape: it has an idle timeout (900 s, long because a restart recompiles every length again) and an orphan watchdog, and it exits when its parent becomes init. Check with `nvidia-smi --query-compute-apps=pid,used_memory --format=csv` before assuming the card is free.
- Revoke temporary keys. After confirmation, remove only .venvs/af2ig and the provider's own cache directory; never use a broad recursive target.

Use only official upstream documentation linked by the implementation README; do not substitute third-party model mirrors.

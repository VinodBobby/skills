---
name: setup-complexa-remote-tool
description: "Set up, validate, or troubleshoot Proteina-Complexa as a ToolUniverse remote tool; use for deployment or runtime issues, with optional Connect relay."
---

# Set up Proteina-Complexa as a remote tool

> Validation status (2026-10-02): Proteina-Complexa 1.1.0 (NVIDIA's flow-matching binder generator -- it DESIGNS proteins against a target structure, it does not fold one) ran on the NVIDIA GB10 (aarch64, cc 12.1) with the optimization kit in `fast` mode, all six levers engaged. Verified on FOUR CONSECUTIVE IDENTICAL REQUESTS, a mixed-shape sequence (100, 100, 200, 100 residues) and an ascending ladder (100/200/400), plus a sequence that changed the ENGINE KEY (`num_steps`, batch size, binder length, the target, the seed) and returned to the first request, which reproduced byte for byte. The held worker's design for the smoke target is byte-identical to the kit's own `run.sh design` in a fresh process, and to a worker built from the lock in an empty venv. Per-request peak reserved runs from 1.70 GiB (100 residues) to 20.25 GiB at the ceiling corner, which is the declared budget. One thing to know before deploying: torch 2.7.0+cu128's NVRTC does not know this card, and without the pinned 12.9 NVRTC every request dies in `torch.prod` (see the environment section). Public publication, cross-user isolation, concurrency, recovery and design quality (binding, designability) are untested; keep this deployment private.

## What a request is

A target protein STRUCTURE (PDB text), a crop of one of its chains (`A1-115`), hotspot residues on its surface (`["A37", "A39"]`, numbered as in that file), a binder length and a design count. The model samples that many binders, and each comes back as a decoded amino-acid sequence (and, with `return_pdb`, a PDB: chain A the target crop, chain B the new binder). It is NOT a predictor: nothing says a design binds, and this deployment runs upstream's **generation stage alone** -- upstream's own `++generation.search.algorithm=single-pass ++generation.reward_model=null` -- so the designs are raw, unscored and unranked. Upstream's shipped configuration also scores every design with an AlphaFold2 reward model whose parameters are not carried here.

The tool validates the target before it queues: the chain must exist in the PDB, the crop must hold residues, every hotspot must be a residue of that crop. This is not pedantry. Upstream does not refuse a hotspot it cannot find (measured: a request naming `A400` in a 115-residue target designed a binder anyway, against fewer hotspots than the caller thought).

## Prerequisites

- Run from the ToolUniverse repository root on Linux with Python 3.12.
- A CUDA GPU is required. This provider holds its model resident between requests; CPU is not a target.
- Keep provider data, weights, caches, and credentials outside Git.
- Bind to loopback. A non-loopback bind requires TOOLUNIVERSE_API_TOKEN; never put it in arguments or results.

Run the standard-library contract check before downloading large dependencies:

~~~bash
python scripts/remote_validation/setup_skill_preflight.py --implementation complexa
~~~

After exporting provider resources, add `--check-provider-env`. After the
server starts, add `--live` to verify the exact MCP tool set without running
the model. Before sharing, add `--check-connect-prereqs`; this reports only
whether a key is set and never prints its value.

## Create the two environments

This provider is on the remote-tool standard, so it has two environments, not
one: the MCP server runs in ToolUniverse's, and the model runs in its own,
built from a pinned lock. They cannot import each other, and that is the point.

~~~bash
python3 -m venv .venvs/complexa
. .venvs/complexa/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install fastmcp
~~~

The model half lives at the path `TOOLUNIVERSE_COMPLEXA_PYTHON` names, and
nothing above creates it. Create an empty CPython 3.12.10 interpreter there with
the STDLIB venv module, not `uv venv` (this kit activates through a `.pth` file
and a `uv venv` `_virtualenv.pth` has broken that detection for another kit):

~~~bash
uv python install 3.12.10
~/.local/share/uv/python/cpython-3.12.10-linux-aarch64-gnu/bin/python3.12 -m venv ~/complexa-venv
export TOOLUNIVERSE_COMPLEXA_PYTHON=~/complexa-venv/bin/python
~~~

`tu remote setup --only environment` then fills it from
`src/tooluniverse/remote/complexa/environment/requirements.lock` with `--no-deps`
(~160 distributions, about 8 GB, torch 2.7.0+cu128 included). The lock's header
records every change from the kit's own x86-64 lock. Two matter here.

- **torch is 2.7.0+cu128, not the kit's +cu126.** 2.7.0 is above the 2.7 line below which no CUDA build can drive this card at all, and an sm_120 cubin runs on sm_121. It is the same upstream version; the kit's pin check treats its torch line as a label.
- **The lock carries a NEWER NVRTC than torch does, and without it every request dies.** torch 2.7.0+cu128 bundles NVRTC 12.8, which does not know sm_121, so `torch.prod(x, dim=-1)` -- which upstream's openfold transforms call on every target's side-chain torsion features -- raises `nvrtc: error: invalid value for --gpu-architecture (-arch)` on every CUDA dtype. `nvidia-cuda-nvrtc-cu12==12.9.86` is pinned and the launcher puts its `lib` directory first on `LD_LIBRARY_PATH` (the loader reads it once at process start, so it has to be the child's environment). Nothing else in the model is affected; this is the only op that failed.

The rest is built by `tu remote setup`, which reads
`src/tooluniverse/remote/complexa/provider.toml` and runs five steps: preflight,
environment, kit, weights, smoke. Each refuses by name and carries its fix.

~~~bash
tu remote setup complexa
~~~

Run one step at a time with `--only preflight|environment|kit|weights|smoke`
while bringing a machine up. The smoke step holds the model, sends one request,
asserts the provider produced a design file (`job_*_n_*_id_*.pdb` -- not `*.pdb`,
which would match the target the provider itself writes), and records the
measured peak VRAM to `~/.cache/tooluniverse/measured/complexa.json`. A host
schedules on that file.

The kit step also builds `torch_scatter` 2.1.2 from the PyPI sdist, CPU-only
(`FORCE_ONLY_CPU=1`): no aarch64 wheel exists, pip's isolated build cannot import
torch, and this host has nvcc 13 beside a cu128 torch. Upstream imports exactly
one name from it, `scatter_mean`, which is torch-native and runs on CUDA tensors.

Package/network-dependent commands must be rerun in a clean environment before marking this skill complete.

## Obtain credentials, data, and model weights

- No credential is needed. The two checkpoints (`complexa.ckpt`, 2,934,289,381 bytes; `complexa_ae.ckpt`, 4,100,101,779 bytes; 6.6 GiB together) come from NVIDIA's own repository `nvidia/NV-Proteina-Complexa-Protein-Target-160M-v1` on the Hugging Face Hub, which answers 200 without a token (`gated: false`), through the kit's own fetcher. Their licence is the NVIDIA Open Model License: commercially usable, derivative models allowed, no ownership claim on outputs. Do not substitute a third-party mirror.
- Nothing is fetched at request time. The manifest declares both files with size and sha256, and the launch refuses if one is off its pin. `CKPT_PATH` names the directory (default `~/complexa_weights`).
- The resident worker forces the data loader to 0 workers and nothing on the path forks: every reply carries `child_processes`, which is 0.

## Authorize once, then share with one short command

After installing dependencies, exporting the provider resources above, and
installing the pinned relay SDK described under Connect below, run from the
repository root. Log in only once per machine (and again after key
rotation):

~~~bash
tu remote login
# Or import an existing protected 0600 file without sourcing it:
tu remote login --env-file /path/to/tooluniverse-service.env
~~~

Then each private share is one short command:

~~~bash
tu remote share complexa
~~~

By default, `tu remote login` requests a short-lived device code, opens the
TU Platform approval page, and polls until the signed-in user approves. No key
copy/paste is required. On a headless machine, add `--no-browser` and open the
printed link elsewhere. The CLI exchanges the approval for a computer-only key,
verifies `/remote-servers/preflight`, stores it in a local 0600 config file, and
never displays it.

The share command runs environment and TU Platform preflights, starts or reuses
the exact loopback endpoint, validates discovery, and keeps the relay in the
foreground until Ctrl-C. It automatically uses the reviewed Python, name,
and worker count. Override them only when needed:

~~~bash
tu remote share complexa --name my-complexa-remote --workers 1
~~~

Use `tu remote check complexa` for a non-sharing readiness check and
`tu remote run complexa` for a local-only foreground server.

In an interactive terminal, sharing automatically starts the same browser flow
when the key is missing, expired, or revoked. A malformed or revoked explicit
`TOOLUNIVERSE_SERVICE_KEY` fails fast instead of being silently replaced; unset
or correct it, then run `tu remote login`. Non-interactive jobs also fail fast.
Use `tu remote logout` to remove only the local copy. Use `tu remote logout --revoke` to revoke the computer-only platform connection first; the server record remains offline for owner inspection.

## Start and verify locally

~~~bash
python -m tooluniverse.remote.complexa.complexa_tool
~~~

The Streamable HTTP endpoint is http://127.0.0.1:8056/mcp. In a second activated shell run:

~~~bash
python - <<'PY'
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8056/mcp") as client:
        print([tool.name for tool in await client.list_tools()])

asyncio.run(main())
PY
~~~

Confirm discovery contains complexa_design_binder; stop on empty, duplicate, or schema-drifted discovery.

The first request after a restart pays the interpreter, the import graph and the model build; the ones after it do not. That is the whole reason this provider is resident, and a benchmark that measures only the first call measures the wrong thing.

## Connect to ToolUniverse Connect

The `tuplatform-connect` relay is not yet published on PyPI. Install the reviewed public wheel below; its SHA-256 is pinned. Interactive sharing uses browser device authorization, so no key copy/paste or GitHub access is required.

~~~bash
python -m pip install fastmcp pyyaml "tuplatform-connect @ https://connect.aiscientist.tools/downloads/tuplatform_connect-0.3.0-py3-none-any.whl#sha256=3fad5eee5ecf7887a693d93ccd1aa112dc0955617a885d1fc3daded0030f9ae0"
tu doctor --forward http://127.0.0.1:8056/mcp --json
tu serve --share --forward http://127.0.0.1:8056/mcp --name validation-complexa --workers 1
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

Operation: complexa_design_binder

The first 50 residues of PD-L1 (chain A, residues 1-50 of upstream's own `PD-L1.pdb` target), two 40-residue binders, 50 integration steps instead of the default 400 so it finishes in minutes, hotspots A37, A39 and A49:

The complete runnable request, including the target PDB coordinates, is in [the verified example JSON](references/complexa-pdl1-example.json). Read it only when running this example.

Invoke the example through the live local MCP endpoint. The snippet reads the packaged JSON reference, so the request remains separate from the setup instructions:

~~~bash
python - <<'PY'
import asyncio
import json
from pathlib import Path

from fastmcp import Client

arguments = json.loads(Path("skills/setup-complexa-remote-tool/references/complexa-pdl1-example.json").read_text())

async def main():
    async with Client("http://127.0.0.1:8056/mcp", timeout=3600) as client:
        result = await client.call_tool("complexa_design_binder", arguments)
        print(result)

asyncio.run(main())
PY
~~~

Expected success shape: `n_designs` equal to `num_designs`, and under `designs` one record per design with a `binder_sequence` of exactly `binder_length` letters; `stage` says "generation only: raw samples, no reward model, no ranking". Run through the live endpoint on 2026-10-02 it returned `n_designs` 2 with binder sequences `KTCSTKGDKVGGCNSNGGCVCKNGVCDKGWSGKNCEEGVN` and `KLLKKNFDGTNDNLTKQAVTEFQKKAGLGVTGIFPTQTRR` (40 residues each), `num_steps` 50, `request_peak_reserved_gib` about 1.9, in 81 s including the cold model build; sampling is seeded, so the same seed reproduces them. Pass `"return_pdb": true` to receive each design's PDB (about 100 KB each). A request that fails on its input comes back as an `error` field naming the problem -- different from "resident worker is not available", which is the provider. Check scientific meaning, output bounds, invalid-input behavior, and absence of paths, secrets, and traces.

## Limits, and why they are what they are

The input has two axes that multiply -- the pair tensor over (target crop + binder) and the designs sampled in one forward pass -- and the ceilings bound the PRODUCT, because a ceiling per axis is how progen2 admitted a 116.93 GiB request. Crop at most 300 residues, binder 20-200, at most 16 designs, `num_steps` 10-400, and (crop + binder)^2 x batch at most 4,000,000. The worst point those admit together, 300 + 200 residues with 16 designs in one pass, is the row the manifest's `vram_budget_gb` (20.25 GiB) is declared at. A request past any one is refused in milliseconds and names the limit; the `batch_size` argument splits the same number of designs into more passes at a lower peak.

Per-request peak reserved on this card, GiB (the peak tracks the input, so the budget is declared at the corner, not the smoke): N = 100 / 200 / 300 / 400 / 500 residues at one design 1.70 / 1.88 / 2.17 / 2.65 / 3.18; at N = 500, 2 / 4 / 8 / 16 designs per pass 4.81 / 6.03 / 10.33 / 17.75-20.25 (20.25 when the previous request left a differently shaped pair-bias buffer, which the kit replaces on a shape change). Designs per pass, not length, is the expensive axis, so a host that never samples more than 4 per pass can hold this provider in about 9 GiB.

## Tune GPU and concurrency

- Use one worker. The resident worker serves one request at a time by design; a second in-flight request queues on its lock rather than doubling peak VRAM.
- Read `vram_budget_gb` from the provider manifest and the measured file before co-tenanting anything else on the card. The manifest states the envelope the figure was measured at; the budget is the worst case, not the smoke.
- Residency is worth 5.4x at its best rung (a 36-residue binder, 10 steps: 44 s fresh against 8 s held), about 5x for the smoke shape on a quiet card (1.6x when other sessions load it), and only about 1.13x at the budget row, where a request is minutes of sampling and the saved import graph and model build are seconds. Wall times on a shared card do not reproduce; peaks do.
- Measure cold start, then **at least four consecutive identical requests**, then a sequence that changes the ENGINE KEY, not merely the input: here that is `num_steps`, `batch_size`, the target and the binder length, then back to the first request, which must reproduce byte for byte. It does (see the status line); that is what shows a held worker rebuilds its per-request state correctly.
- Then parallel levels 1, 2, 4, 8, and only 16 if memory permits.
- Record successes/errors, p50/p95, peak RAM/VRAM, utilization, queueing, cancellation cleanup, and recovery.
- Increase workers only after single-flight initialization and sanitized recoverable OOM/timeout behavior are proven.

## Troubleshoot and clean up

- Read the refusal. Every step of `tu remote setup` names what is wrong and carries the fix; exit 3 is a refusal and exit 1 is a failure.
- The worker's own transcript is at `~/.cache/tooluniverse/remote-logs/complexa-resident.log`. It holds the kit's lever census (`LEVER name=... state=on` for all six levers of `fast`; `state=skipped reason=padded_batches` on `pair_assembly` would mean a binder-length range reached the model, which this tool never sends) and, for a failed request, the Python traceback -- the reply carries only the message.
- `nvrtc: error: invalid value for --gpu-architecture` in a reply means the worker started without the 12.9 NVRTC first on `LD_LIBRARY_PATH`: re-run `tu remote setup complexa --only environment` and start the worker through `tu remote run complexa`, which applies the launcher. Do not export `LD_LIBRARY_PATH` into the MCP server's shell expecting it to reach the worker.
- A `COMPLEXA_OPT*` name exported in your shell (other than `COMPLEXA_OPT` and `COMPLEXA_OPT_RECORD`) makes the kit's start-up hook exit 3 in EVERY interpreter of the model environment. The launcher strips such names from the worker's environment; running the model interpreter by hand with one set is what fails.
- Import/executable failure in the model half: re-run `tu remote setup complexa --only environment`. It rebuilds from the lock with `--no-deps` and will not silently resolve a different version.
- Weights off their pin: the named file is left in place for inspection rather than deleted, because a truncated transfer and a corrupt file look alike. Remove it by hand and re-run `--only weights`.
- 401/403 on deliberate network binding: configure matching TOOLUNIVERSE_API_TOKEN bearer auth; prefer loopback plus relay.
- Stop server/relay with Ctrl-C. If installed, run `tuplatform-service uninstall --name validation-complexa`.
- A worker outliving its server is a known shape: it has an idle timeout and an orphan watchdog, and it exits when its parent becomes init. Between requests it holds 0.02 to 2.5 GiB of the card (the model returns to the CPU after each request; the 2.5 GiB is the kit's one pair-bias buffer, kept for the last request's shape). Check with `nvidia-smi --query-compute-apps=pid,used_memory --format=csv` before assuming the card is free.
- Revoke temporary keys. After confirmation, remove only .venvs/complexa and the provider's own cache directory; never use a broad recursive target.

Use only official upstream documentation linked by the implementation README; do not substitute third-party model mirrors.

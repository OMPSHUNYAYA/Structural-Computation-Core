# ⭐ **Shunyaya Structural Computation Core (SSC-Core)**

## **Quickstart**

**Deterministic • Replay-Verifiable • Conservative Structural Computation Overlay**  
**No Probability • No Randomness • No Magnitude Modification**

---

# 🚀 **What This Repository Demonstrates**

This repository demonstrates a **deterministic structural computation overlay** that measures the **geometry of execution** without altering classical results.

Running the Quickstart will show that:

- **structural work quantities can be computed deterministically**
- **certificates can be derived directly from execution traces**
- **artifact bundles can be verified using cryptographic manifests**
- **independent executions produce byte-identical outputs**

You can also **interactively visualize the structural execution geometry** by opening:

```
docs/SSC-Core-Interactive-Topology.html
```

The viewer renders **`Psi(t)`** and the **g-stream** directly from `ssc_trace.csv` and recomputes **`Omega`**, **`K`**, **`D`**, and **`F`** deterministically.

The **core verification condition** is:

`B_A = B_B`

If two executions produce **identical artifact bundles**, the computation is **deterministically verified**.

---

# **What You Need to Know First**

**Shunyaya Structural Computation Core (SSC-Core)** is intentionally **conservative**.

SSC-Core **does not**:

- modify classical magnitude
- modify domain mathematics
- predict future behavior
- inject control logic
- perform optimization
- apply smoothing or machine learning
- use probabilistic inference

SSC-Core **overlays a deterministic structural computation layer** over stepwise execution.

It:

- computes **structural work geometry deterministically**
- computes **structural compression**
- computes **structural curvature**
- computes **structural topology fingerprint**
- preserves **magnitude exactly**
- produces **replay-verifiable artifacts**

---

# **Core Invariant (Non-Negotiable)**

**Conservative collapse mapping**

`phi((m,a,s)) = m`

Where:

- `m` = classical magnitude (unchanged)  
- `a` = structural alignment  
- `s` = structural state  

**Magnitude is never altered.**

---

# **Structural Quantities Computed**

For deterministic execution of length **N**:

**Work Field**

`Psi(t) = W_allow(t) / W(t)`

**Compression**

`Omega = sum_{i=1..N} (1 - Psi(i))`

**Curvature**

`K = sum_{i=2..N} |g(i) - g(i-1)|`

**Structural Density**

`D = W_allow(N) / W(N)`

**Fingerprint**

`F = sha256(g_stream || '|' || Psi_samples || '|' || Omega || '|' || K)`

All quantities are:

- **deterministic**
- **trace-derived**
- **replay-verifiable**
- **manifest-bound**

---

# **Requirements**

- **Python 3.9+** (CPython recommended)
- **Standard library only**
- **No external dependencies**
- **Offline capable execution**

All verification is:

- **deterministic**
- **replay-verifiable**
- **byte-identical across machines**
- **environment-normalized**

There is:

- **no randomness**
- **no statistical inference**
- **no adaptive thresholds**

---

# **What Quickstart Guarantees**

If you follow this Quickstart exactly, you will verify:

`B_A = B_B`

without:

- editing scripts
- trusting documentation claims
- inspecting internal logic

Verification proves:

- **deterministic structural work computation**
- **trace-derived certificate enforcement**
- **structural compression integrity**
- **structural curvature integrity**
- **byte-identical artifact generation**
- **replay identity**

If verification fails, **SSC-Core fails**.

There is **no partial success**.

---

# **Repository Layout**

```
SSC-Core/
│
├── README.md
├── LICENSE
│
├── docs/
│   ├── Quickstart.md
│   ├── FAQ.md
│   ├── INSTRUMENTATION_GUIDE.md
│   ├── SSC-Core-Conformance-Specification.md
│   ├── SSC-Core-Structural-Computation-Model.md
│   ├── TEST_CYCLE_LOG.txt
│   ├── Concept-Flyer_SSC-Core_v1.4.pdf
│   ├── SSC-Core_v1.4.pdf
│   ├── SSC-Core-Topology-Diagram.png
│   └── SSC-Core-Interactive-Topology.html
│
├── scripts/
│   ├── run_ssc_core.py
│   ├── verify_ssc_core.py
│   └── derive_certificate_from_trace.py
│
├── isa/
│   ├── README.md
│   ├── SSC-ISA-Machine-Model.md
│   ├── SSC-ISA-Specification.md
│   │
│   ├── examples/
│   │   └── case01.isa
│   │
│   ├── tools/
│   │   ├── ss_isa_run.py
│   │   └── ss_isa_verify.py
│   │
│   └── outputs_example/
│       ├── primary/
│       └── replay/
│
├── outputs_example/
│   ├── primary/
│   │   ├── MANIFEST.sha256
│   │   ├── OIR_SSC_CORE.txt
│   │   ├── RUN.txt
│   │   ├── RUN_CONFIG.json
│   │   ├── SSC_CORE_CERTIFICATE.txt
│   │   ├── ssc_summary.txt
│   │   └── ssc_trace.csv
│   │
│   └── replay/
│       ├── MANIFEST.sha256
│       ├── OIR_SSC_CORE.txt
│       ├── RUN.txt
│       ├── RUN_CONFIG.json
│       ├── SSC_CORE_CERTIFICATE.txt
│       ├── ssc_summary.txt
│       └── ssc_trace.csv
│
└── verify/
    └── VERIFY_RITUAL.md
```

---

# **Runtime & Example Output Policy**

`outputs_example/` contains a **replay-verified artifact bundle**.

These artifacts demonstrate:

- **manifest discipline**
- **trace-derived enforcement**
- **replay identity**
- **tamper detection**

Users may generate **fresh outputs locally** by running the declared commands.

Replay condition:

`B_A = B_B`

Identical declared parameters must produce **identical artifacts**.

Deterministic reproducibility is the **authority**.

---

# **Official Verification Procedure**

From the **project root**:

```
python scripts/run_ssc_core.py --out outputs_primary --label core
python scripts/run_ssc_core.py --out outputs_replay --label core
python scripts/verify_ssc_core.py --primary outputs_primary --replay outputs_replay
```

Expected result:

```
PRIMARY_VERIFY: PASS
REPLAY_VERIFY: PASS
TRACE_DERIVED_CHECK_PRIMARY: PASS
TRACE_DERIVED_CHECK_REPLAY: PASS
REPLAY_IDENTITY: PASS
OVERALL_STATUS: PASS
```

Replay identity condition:

`B_A = B_B`

If replay identity fails, **conformance fails**.

- **No tolerance**
- **No partial acceptance**
- **Byte identity required**

---

# **Tamper Ritual**

The formal tamper ritual is documented in:

```
verify/VERIFY_RITUAL.md
```

This document defines the procedure for confirming that:

- artifact manifests detect **tampering**
- certificate enforcement is **trace-derived**
- replay identity **cannot be falsified**

---

# **Manual Trace-Derived Certificate Verification**

From project root:

```
python scripts/derive_certificate_from_trace.py --dir outputs_primary
```

Derived values must match those inside:

`SSC_CORE_CERTIFICATE.txt`

Mismatch **invalidates structural conformance**.

Certificate authority is **trace-derived — not narrative**.

---

# **Core Structural Model Overview**

State model:

`X(t) = (m(t), a(t), s(t), w(t))`

Work field:

`Psi(t) = W_allow(t) / W(t)`

Compression:

`Omega = sum_{i=1..N} (1 - Psi(i))`

Curvature:

`K = sum_{i=2..N} |g(i) - g(i-1)|`

Collapse invariant:

`phi((m,a,s)) = m`

SSC-Core governs **structural computation geometry — not magnitude**.

---

# **Deterministic Replay Rule**

Two independent executions under identical inputs must produce:

`B_A = B_B`

Replay identity requires **byte-identical artifacts**, including:

- `ssc_trace.csv`
- `SSC_CORE_CERTIFICATE.txt`
- `ssc_summary.txt`
- `MANIFEST.sha256`

Replay identity is **authoritative proof**.

---

# **What SSC-Core Is Not**

SSC-Core **does not**:

- replace classical algorithms
- predict failure
- forecast cascade events
- perform optimization
- inject probabilistic reasoning
- guarantee safety

It computes **structural geometry of execution only**.

---

# **One-Line Summary**

**Shunyaya Structural Computation Core (SSC-Core)** computes deterministic structural work geometry (`Psi(t)`, `Omega`, `K`, `D`, `F`) alongside classical outputs, preserves magnitude via `phi((m,a,s)) = m`, enforces trace-derived certificate equality, and defines conformance strictly through exact replay identity `B_A = B_B`.

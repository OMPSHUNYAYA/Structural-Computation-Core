# **SSC-ISA Specification (v0.1)**

**Shunyaya Structural Computation Instruction Set**

---

# **1. Objective**

SSC-ISA defines a deterministic instruction language and execution model capable of generating **replay-verifiable structural traces**.

SSC-ISA authority is defined by replay identity:

`B_ISA_A = B_ISA_B`

No tolerance is allowed.

---

# **2. Instruction Alphabet**

SSC-ISA **v0.1** defines a minimal finite instruction set:

`I = {SET, STEP, HALT}`

These instructions are sufficient to generate **deterministic structural traces**.

---

# **3. Machine State**

At logical time `t`, the SSC-ISA machine state is:

`S(t) = (m(t), w_allow(t), w(t))`

Where:

`m(t)` = classical magnitude state  
`w_allow(t)` = allowed work value  
`w(t)` = observed work value  

State variables are updated using the `SET` instruction.

---

# **4. Instruction Semantics**

## **SET**

Syntax:

`SET <key> <value>`

Where:

`key ∈ {m, w_allow, w}`

Effect:

`key := value`

No trace row is emitted.

---

## **STEP**

`STEP` emits a deterministic trace row.

Requirements:

`m != None`  
`w_allow != None`  
`w != None`

Logical time increments:

`t := t + 1`

A single trace row is emitted.

---

## **HALT**

`HALT` terminates execution.

A valid SSC-ISA program must contain **exactly one reachable HALT**.

Programs without `HALT` are **invalid**.

---

# **5. Trace Format**

SSC-ISA emits `isa_trace.csv` containing columns:

`t, m, w_allow, w, Psi, g`

Each `STEP` instruction produces **exactly one row**.

---

# **6. Derived Structural Quantities**

For each time step:

`Psi(t) = w_allow(t) / w(t) if w(t) != 0 else 0`

`g(t) = 1 - Psi(t)`

Let `N` be the number of steps.

**Compression:**

`Omega = sum_{i=1..N} (1 - Psi(i))`

**Curvature:**

`K = sum_{i=2..N} |g(i) - g(i-1)|`

**Fingerprint:**

`F = sha256(g_stream || '|' || Psi_samples || '|' || Omega || '|' || K)`

Where:

`g_stream = g(1), g(2), ... , g(N)`

`Psi_samples = Psi(1), Psi(2), ... , Psi(N)`

---

# **7. Certificate**

SSC-ISA produces:

`SSC_ISA_CERTIFICATE.txt`

Certificate fields:

- `LABEL`
- `N`
- `Omega`
- `K`
- `F`

Certificate values must be **trace-derived**.

Certificate authority is **trace-derived — not narrative**.

---

# **8. Manifest Discipline**

SSC-ISA produces:

`MANIFEST.sha256`

The manifest records **SHA-256 hashes** for the artifact set:

- `isa_trace.csv`
- `isa_summary.txt`
- `SSC_ISA_CERTIFICATE.txt`
- `RUN_CONFIG.json`
- `RUN.txt`

Verification requires **exact hash equality**.

---

# **9. Replay Identity**

Two executions using identical program and parameters must produce:

`B_ISA_A = B_ISA_B`

Replay identity requires **byte-identical artifacts**.

No tolerance.

No partial acceptance.

---

# **10. Failure Witness Rules**

SSC-ISA execution fails deterministically under the following conditions:

`STATE_INCOMPLETE`  
if `STEP` occurs before required state values are set.

`NO_HALT`  
if the program terminates without executing `HALT`.

`BAD_SET`  
if the syntax of `SET` is invalid.

`UNKNOWN_KEY`  
if `SET` uses a key outside `{m, w_allow, w}`.

Failure conditions must produce **deterministic error witnesses**.

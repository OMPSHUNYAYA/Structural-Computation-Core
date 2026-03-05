# **SSC-ISA Machine Model (v0.2)**

---

# **1. Purpose**

SSC-ISA defines a deterministic instruction machine whose executions emit a **trace** and a **trace-derived certificate**.

SSC-ISA authority is defined only by replay identity:

`B_ISA_A = B_ISA_B`

No tolerance is permitted.

---

# **2. The Machine**

Define the SSC-ISA machine as:

`M = (I, S, T, Phi, E)`

Where:

`I` = finite instruction alphabet  
`S` = machine state space  
`T` = deterministic trace emission function  
`Phi` = conservative collapse mapping (**magnitude preservation**)  
`E` = deterministic error witness function  

---

# **3. Instruction Alphabet**

For **v0.2**:

`I = {SET, STEP, HALT, ASSERT_EQ}`

`SET`, `STEP`, `HALT` define the **minimal execution path**.

`ASSERT_EQ` introduces **deterministic certified failure witnesses**.

---

# **4. State Space**

At logical time `t`, the machine state is:

`S(t) = (t, m(t), w_allow(t), w(t), R(t))`

Where:

`t` = logical step counter  
`m(t)` = classical magnitude state  
`w_allow(t)` = allowed work value  
`w(t)` = observed work value  
`R(t)` = register map (**finite set of named registers**)  

In **v0.2** the register set is:

`R = {m, w_allow, w}`

---

# **5. Conservative Collapse Mapping**

SSC-ISA is **conservative with respect to magnitude**.

Collapse mapping:

`Phi((m,a,s)) = m`

Meaning:

- structural computation may evolve  
- certificates may be produced  
- traces may be emitted  

**Magnitude is not modified by SSC-ISA.**

SSC-ISA may **store or read `m`**, but never transforms `m` into a different magnitude output.

---

# **6. Deterministic Trace Emission**

Define the trace emission function:

`T : (S(t), instr) -> (S(t+1), row?)`

Rules:

- `SET` emits **no trace row**
- `STEP` emits **exactly one trace row**
- `ASSERT_EQ` emits **no trace row if it passes**, otherwise halts with witness
- `HALT` emits **no trace row**

Trace rows are emitted **only by `STEP`**.

---

# **7. Derived Structural Quantities**

For each emitted trace row:

`Psi(t) = w_allow(t) / w(t) if w(t) != 0 else 0`

`g(t) = 1 - Psi(t)`

For `N` steps:

`Omega = sum_{i=1..N} (1 - Psi(i))`

`K = sum_{i=2..N} |g(i) - g(i-1)|`

`F = sha256(g_stream || '|' || Psi_samples || '|' || Omega || '|' || K)`

These quantities are **trace-derived**.

---

# **8. Deterministic Error Witness**

Define the witness function:

`E : (S(t), error_code) -> W`

Where `W` is a **deterministic witness record** that includes:

- witness code  
- instruction pointer `t`  
- instruction text  
- key state values required to reproduce the failure  

Examples:

- `STATE_INCOMPLETE`
- `ASSERT_EQ_FAIL`
- `NO_HALT`
- `UNKNOWN_KEY`
- `BAD_SET`

Witness records are **replay-verifiable artifacts**.

---

# **9. Conformance**

A run is **conformant** iff:

All produced artifacts verify under:

`MANIFEST.sha256`

Replay identity holds:

`B_ISA_A = B_ISA_B`

This includes:

- `isa_trace.csv`
- `SSC_ISA_CERTIFICATE.txt`
- `RUN_CONFIG.json`
- `RUN.txt`
- `MANIFEST.sha256`

**No tolerance.**

---

# **10. Civilization-Grade Property**

SSC-ISA is a computation machine whose authority is **not granted by narrative**.

Authority is granted **only by replay identity**:

`B_ISA_A = B_ISA_B`

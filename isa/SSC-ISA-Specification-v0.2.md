# **SSC-ISA Specification (v0.2)**

**Shunyaya Structural Computation Instruction Set**

---

# **1. Instruction Set**

The SSC-ISA v0.2 instruction alphabet is:

`I = {SET, STEP, HALT, ASSERT_EQ}`

This extends the minimal instruction machine by introducing a **deterministic verification instruction** capable of producing certified failure witnesses.

---

# **2. New Instruction: ASSERT_EQ**

## **Syntax**

`ASSERT_EQ <key> <value>`

Where:

`key ∈ {m, w_allow, w}`

---

## **Semantics**

Read the current state value:

`x = key`

Execution rule:

- If `x == value`, execution **continues**
- Otherwise execution **fails deterministically** with witness:

`ASSERT_EQ_FAIL`

---

## **Notes**

- Equality comparison is **exact**
- **No tolerance** is permitted
- **No implicit casting** beyond standard numeric parse rules

The instruction therefore produces **deterministic structural validation**.

---

# **3. Failure Witness Artifact (Required)**

On deterministic failure, SSC-ISA must produce the following artifact set:

- `SSC_ISA_FAILURE_WITNESS.txt`
- `RUN_CONFIG.json`
- `RUN.txt`
- `MANIFEST.sha256`

If failure occurs **after at least one `STEP`**, the artifact set may also include:

- `isa_trace.csv`

The witness artifact must allow **complete deterministic reproduction of the failure condition**.

---

## **Witness File Format (Minimum)**

The witness file must contain at least the following fields:

- `WITNESS_CODE`
- `T`
- `INSTR`
- `STATE_SNAPSHOT`

Where:

`T` = logical instruction pointer  
`INSTR` = instruction text that triggered failure  
`STATE_SNAPSHOT` = key state values required to reproduce the failure  

The witness must be **fully deterministic**.

---

# **4. Replay Identity for Failure Capsules**

Failure capsules must also satisfy **replay identity**.

Authority condition:

`B_ISA_FAIL_A = B_ISA_FAIL_B`

Meaning:

- failure witnesses are **replay-verifiable**
- deterministic failure is **as certifiable as success**

Failure therefore becomes a **structural artifact**, not a narrative explanation.

---

# **5. Rationale**

The introduction of `ASSERT_EQ` transforms SSC-ISA from a simple execution runner into a **civilization-grade structural computation language**.

The machine can now certify both execution outcomes:

- **success can be certified**
- **failure can be certified**
- **every failure produces an exact witness**

No probabilistic ambiguity exists.

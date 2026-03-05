# **INSTRUMENTATION GUIDE**

**Applying SSC-Core Structural Geometry to Deterministic Algorithms**

---

# **INTRODUCTION**

SSC-Core can measure the **structural geometry of any deterministic computation** without altering its classical output.

The only requirement is that the execution can expose **two deterministic quantities at each step**:

**`W(t)`**  
Actual work performed at step `t`

**`W_allow(t)`**  
Allowed work envelope at step `t`

From these quantities SSC-Core computes the **structural geometry of execution**.

The **classical magnitude of the algorithm remains unchanged**.

The collapse invariant must always hold:

`phi((m,a,s)) = m`

SSC-Core therefore **observes execution structure while preserving the original algorithm exactly**.

---

# **STRUCTURAL GEOMETRY MODEL**

For deterministic execution steps `t = 1..N`:

### **Work field**

`Psi(t) = W_allow(t) / W(t)`

### **Decision stream**

`g(t) = 1 - Psi(t)`

### **Structural compression**

`Omega = sum_{i=1..N} (1 - Psi(i))`

### **Structural curvature**

`K = sum_{i=2..N} |g(i) - g(i-1)|`

### **Structural fingerprint**

`F = sha256(g_stream || '|' || Psi_samples || '|' || Omega || '|' || K)`

All values must be **derived from the execution trace**.

---

# **TRACE DISCIPLINE**

Every deterministic execution step must **emit a trace row**.

### **Example trace format**

`t, W, W_allow, Psi, g`

### **Example**

```
1, 10, 4, 0.400000000000, 0.600000000000
2, 10, 4, 0.400000000000, 0.600000000000
3, 10, 4, 0.400000000000, 0.600000000000
```

The **trace file is the authoritative structural record**.

Certificates must **always be recomputed from the trace**.

---

# **INSTRUMENTATION TEMPLATE**

A deterministic algorithm can be instrumented using a **simple pattern**.

### **Generic structure**

Initialize trace.

For each deterministic step `t`:

Compute classical work:

`W = actual work performed`

Define deterministic allowance:

`W_allow = permitted work envelope`

Compute structural quantities:

`Psi = W_allow / W`  
`g = 1 - Psi`

Append trace row.

Continue execution.

After completion, compute structural invariants:

`Omega`  
`K`  
`F`

---

# **MINIMAL INSTRUMENTATION EXAMPLE**

Example deterministic loop:

```
for i in range(N):
    perform_step()
```

### **Instrumentation pattern**

```
for i in range(N):

    perform_step()

    W = measure_work()

    W_allow = allowed_work()

    Psi = W_allow / W

    g = 1 - Psi

    record_trace(i, W, W_allow, Psi, g)
```

After the loop:

```
compute Omega
compute K
compute F
```

Generate certificate.

---

# **TRACE-DERIVED CERTIFICATION**

SSC-Core certificates must **always be trace-derived**.

### **Procedure**

1. Execute deterministic algorithm  
2. Generate trace file  
3. Recompute structural quantities from trace  
4. Produce certificate

Verification requires:

- **Primary execution artifacts**
- **Replay execution artifacts**

Both must satisfy:

`B_A = B_B`

**Byte-identical artifact bundles confirm deterministic conformance.**

---

# **WORK ACCOUNTING GUIDELINES**

Instrumentation must follow **deterministic work accounting**.

Work measurement must be:

- **Deterministic**
- **Repeatable**
- **Traceable**

### **Examples of deterministic work units**

- Loop iterations
- Memory accesses
- Instruction counts
- Algorithmic operations
- State transitions

**Timing measurements are not recommended unless deterministic.**

---

# **CHOOSING `W_allow`**

`W_allow` defines the **structural work envelope**.

Possible interpretations include:

- Expected algorithmic work
- Upper bound of work
- Budgeted work allowance
- Theoretical optimal work

The chosen definition must **remain deterministic across executions**.

---

# **STRUCTURAL INTERPRETATION**

SSC-Core measures **structural properties of execution**.

### **`Psi(t)`**

Local **work compression or expansion**.

### **`Omega`**

Aggregate **structural compression across execution**.

### **`K`**

Structural **oscillation of the decision stream**.

### **`F`**

Cryptographic **structural fingerprint of execution geometry**.

These quantities describe **execution topology while leaving classical magnitude untouched**.

---

# **INSTRUMENTATION PRINCIPLES**

SSC-Core instrumentation must obey the following rules:

**Do not modify classical magnitude**

`phi((m,a,s)) = m`

**Do not introduce randomness**

**Do not introduce tolerance**

**Do not introduce approximate equality**

All quantities must be **deterministic**.

All certificates must be **trace-derived**.

Replay identity must hold:

`B_A = B_B`

---

# **MINIMAL ADOPTION PATH**

To instrument an existing deterministic algorithm:

1. Identify the deterministic execution steps  
2. Define `W(t)`  
3. Define `W_allow(t)`  
4. Emit trace rows  
5. Derive structural invariants  
6. Generate SSC-Core certificate  
7. Validate replay identity  

The **classical algorithm remains unchanged**.

Only **structural observation** is added.

---

# **RESULT**

Any deterministic algorithm can produce:

`Psi(t)`  
`Omega`  
`K`  
`F`

while **preserving classical output exactly**.

SSC-Core therefore enables **structural observability of computation without altering the underlying system**.

Conformance authority remains:

`B_A = B_B`

and the collapse invariant:

`phi((m,a,s)) = m`

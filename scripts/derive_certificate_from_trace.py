import argparse
import csv
import hashlib
import os

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    args = ap.parse_args()

    base = os.path.abspath(args.dir)
    trace_path = os.path.join(base, "ssc_trace.csv")

    if not os.path.exists(trace_path):
        raise SystemExit("TRACE_MISSING")

    rows = []
    with open(trace_path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)

    m_out = 0
    W = 0
    W_allow = 0
    psi_curve = []
    g_stream = []

    for row in rows:
        W += 1
        W_allow = int(row["W_allow_cum"])
        psi = float(row["Psi"])
        psi_curve.append(psi)
        g = int(row["g"])
        g_stream.append(g)
        m_out += int(row["sq_used"])

    Omega = 0.0
    for psi in psi_curve:
        Omega += (1.0 - psi)

    K = 0
    for i in range(1, len(g_stream)):
        K += abs(g_stream[i] - g_stream[i-1])

    g_str = "".join(str(v) for v in g_stream)
    psi_str = ",".join(f"{v:.12f}" for v in psi_curve)
    F_payload = g_str + "|" + psi_str + "|" + f"{Omega:.12f}" + "|" + str(K)
    F = sha256_bytes(F_payload.encode("utf-8"))

    print("TRACE_DERIVED_VALUES")
    print("M_OUT:", m_out)
    print("W:", W)
    print("W_ALLOW:", W_allow)
    print("OMEGA:", f"{Omega:.12f}")
    print("K:", K)
    print("F:", F)

if __name__ == "__main__":
    main()
import argparse
import os
import hashlib
import csv

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_manifest(path: str):
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                raise ValueError("Bad manifest line: " + line)
            digest = parts[0]
            name = parts[1]
            entries.append((digest, name))
    return entries

def verify_one(dir_path: str):
    manifest_path = os.path.join(dir_path, "MANIFEST.sha256")
    if not os.path.exists(manifest_path):
        return False, "MISSING_MANIFEST"

    entries = read_manifest(manifest_path)
    for expected, name in entries:
        fp = os.path.join(dir_path, name)
        if not os.path.exists(fp):
            return False, "MISSING_FILE: " + name
        got = sha256_file(fp)
        if got.lower() != expected.lower():
            return False, "HASH_MISMATCH: " + name
    return True, "OK"

def file_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def parse_cert(path: str):
    kv = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            k, v = line.split(":", 1)
            kv[k.strip()] = v.strip()
    return kv

def trace_derive(dir_path: str):
    trace_path = os.path.join(dir_path, "ssc_trace.csv")
    if not os.path.exists(trace_path):
        return None, "TRACE_MISSING"

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

    return {
        "M_OUT": str(m_out),
        "W": str(W),
        "W_ALLOW": str(W_allow),
        "OMEGA": f"{Omega:.12f}",
        "K": str(K),
        "F": F
    }, "OK"

def enforce_trace_equals_cert(dir_path: str):
    cert_path = os.path.join(dir_path, "SSC_CORE_CERTIFICATE.txt")
    if not os.path.exists(cert_path):
        return False, "CERT_MISSING"

    cert = parse_cert(cert_path)
    derived, msg = trace_derive(dir_path)
    if derived is None:
        return False, msg

    fields = ["M_OUT", "W", "W_ALLOW", "OMEGA", "K", "F"]
    for k in fields:
        if k not in cert:
            return False, "CERT_FIELD_MISSING: " + k
        if cert[k] != derived[k]:
            return False, "TRACE_CERT_MISMATCH: " + k

    return True, "OK"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--primary", required=True)
    ap.add_argument("--replay", required=True)
    args = ap.parse_args()

    primary = os.path.abspath(args.primary)
    replay = os.path.abspath(args.replay)

    ok1, msg1 = verify_one(primary)
    ok2, msg2 = verify_one(replay)

    if not ok1:
        print("PRIMARY_VERIFY: FAIL")
        print("REASON: " + msg1)
        raise SystemExit(1)

    if not ok2:
        print("REPLAY_VERIFY: FAIL")
        print("REASON: " + msg2)
        raise SystemExit(1)

    t1, tmsg1 = enforce_trace_equals_cert(primary)
    if not t1:
        print("TRACE_DERIVED_CHECK_PRIMARY: FAIL")
        print("REASON: " + tmsg1)
        raise SystemExit(3)

    t2, tmsg2 = enforce_trace_equals_cert(replay)
    if not t2:
        print("TRACE_DERIVED_CHECK_REPLAY: FAIL")
        print("REASON: " + tmsg2)
        raise SystemExit(3)

    m1 = file_bytes(os.path.join(primary, "MANIFEST.sha256"))
    m2 = file_bytes(os.path.join(replay, "MANIFEST.sha256"))

    if m1 != m2:
        print("REPLAY_IDENTITY: FAIL")
        print("CONDITION: B_A = B_B")
        raise SystemExit(2)

    print("PRIMARY_VERIFY: PASS")
    print("REPLAY_VERIFY: PASS")
    print("TRACE_DERIVED_CHECK_PRIMARY: PASS")
    print("TRACE_DERIVED_CHECK_REPLAY: PASS")
    print("REPLAY_IDENTITY: PASS")
    print("CONDITION: B_A = B_B")
    print("OVERALL_STATUS: PASS")

if __name__ == "__main__":
    main()
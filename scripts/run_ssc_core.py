import argparse
import csv
import hashlib
import json
import os
from datetime import datetime, timezone

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def write_text(path: str, s: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)

def write_json(path: str, obj) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=True, sort_keys=True, indent=2)
        f.write("\n")

def compute_ssc_core(xs):
    cache = {}
    m_out = 0
    W = len(xs)
    w_cum = 0
    w_allow_cum = 0

    g_stream = []
    psi_curve = []
    trace_rows = []

    prev_g = 0
    K = 0

    for i, x in enumerate(xs, start=1):
        w_cum += 1
        if x in cache:
            decision = "ABSTAIN"
            g = 0
            sq = cache[x]
        else:
            decision = "ALLOW"
            g = 1
            sq = x * x
            cache[x] = sq
            w_allow_cum += 1

        m_out += sq

        psi = w_allow_cum / w_cum
        psi_curve.append(psi)
        g_stream.append(g)

        if i == 1:
            K = 0
        else:
            K += abs(g - prev_g)
        prev_g = g

        trace_rows.append({
            "i": i,
            "x": x,
            "decision": decision,
            "g": g,
            "W_cum": w_cum,
            "W_allow_cum": w_allow_cum,
            "Psi": f"{psi:.12f}",
            "sq_used": sq
        })

    W_allow = w_allow_cum

    Omega = 0.0
    for psi in psi_curve:
        Omega += (1.0 - psi)

    g_str = "".join(str(v) for v in g_stream)
    psi_str = ",".join(f"{v:.12f}" for v in psi_curve)
    F_payload = g_str + "|" + psi_str + "|" + f"{Omega:.12f}" + "|" + str(K)
    F = sha256_bytes(F_payload.encode("utf-8"))

    work_eliminated_fraction = (W - W_allow) / W if W > 0 else 0.0
    structural_speedup = (W / W_allow) if W_allow > 0 else 1.0

    return {
        "m_out": m_out,
        "W": W,
        "W_allow": W_allow,
        "work_eliminated_fraction": work_eliminated_fraction,
        "structural_speedup": structural_speedup,
        "Psi_curve": psi_curve,
        "Omega": Omega,
        "K": K,
        "F": F,
        "trace_rows": trace_rows
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", required=True)
    args = ap.parse_args()

    out_dir = os.path.abspath(args.out)
    ensure_dir(out_dir)

    operator_name = "SSC_CORE_DEMO"
    run_label = args.label

    xs = [2, 7, 2, 9, 7, 3, 9, 9, 5, 3, 5, 2, 11, 7, 11, 13, 2, 13, 17, 17]
    input_digest = sha256_bytes((",".join(str(x) for x in xs)).encode("utf-8"))

    r = compute_ssc_core(xs)

    m_out = r["m_out"]
    W = r["W"]
    W_allow = r["W_allow"]
    work_eliminated_fraction = r["work_eliminated_fraction"]
    structural_speedup = r["structural_speedup"]
    Omega = r["Omega"]
    K = r["K"]
    F = r["F"]

    output_digest = sha256_bytes(str(m_out).encode("utf-8"))

    trace_path = os.path.join(out_dir, "ssc_trace.csv")
    with open(trace_path, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=["i", "x", "decision", "g", "W_cum", "W_allow_cum", "Psi", "sq_used"])
        w.writeheader()
        for row in r["trace_rows"]:
            w.writerow(row)

    run_config = {
        "operator": operator_name,
        "input_digest": input_digest,
        "input_xs": xs
    }
    write_json(os.path.join(out_dir, "RUN_CONFIG.json"), run_config)

    run_txt = "python scripts\\run_ssc_core.py --out <OUT_DIR> --label core\n"
    write_text(os.path.join(out_dir, "RUN.txt"), run_txt)

    run_meta = []
    run_meta.append("RUN_META")
    run_meta.append("OPERATOR: " + operator_name)
    run_meta.append("LABEL: " + run_label)
    run_meta.append("OUT_DIR: " + out_dir)
    run_meta.append("UTC_TIME: " + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    run_meta.append("")
    write_text(os.path.join(out_dir, "RUN_META.txt"), "\n".join(run_meta))

    oir = []
    oir.append("OPERATOR: " + operator_name)
    oir.append("OUTPUT_PRESERVATION: phi((m,a,s)) = m")
    oir.append("STATE: X(t) = (m(t), a(t), s(t), w(t))")
    oir.append("WORK_FIELD: Psi(t) = W_allow(t) / W(t)")
    oir.append("COMPRESSION: Omega = sum_{i=1..N} (1 - Psi(i))")
    oir.append("CURVATURE: K = sum_{i=2..N} |g(i) - g(i-1)|")
    oir.append("FINGERPRINT: F = sha256(g_stream || '|' || Psi_samples || '|' || Omega || '|' || K)")
    oir.append("DECISION_STREAM: g(i)=1 if ALLOW else 0")
    oir.append("")
    write_text(os.path.join(out_dir, "OIR_SSC_CORE.txt"), "\n".join(oir))

    cert = []
    cert.append("SSC_CORE_CERTIFICATE")
    cert.append("OPERATOR: " + operator_name)
    cert.append("INPUT_DIGEST: " + input_digest)
    cert.append("OUTPUT_DIGEST: " + output_digest)
    cert.append("M_OUT: " + str(m_out))
    cert.append("W: " + str(W))
    cert.append("W_ALLOW: " + str(W_allow))
    cert.append("WORK_ELIMINATED_FRACTION: " + f"{work_eliminated_fraction:.12f}")
    cert.append("STRUCTURAL_SPEEDUP: " + f"{structural_speedup:.12f}")
    cert.append("OMEGA: " + f"{Omega:.12f}")
    cert.append("K: " + str(K))
    cert.append("F: " + F)
    cert.append("")
    write_text(os.path.join(out_dir, "SSC_CORE_CERTIFICATE.txt"), "\n".join(cert))

    summary = []
    summary.append("SSC_CORE_SUMMARY")
    summary.append("OPERATOR: " + operator_name)
    summary.append("INPUT_DIGEST: " + input_digest)
    summary.append("OUTPUT_DIGEST: " + output_digest)
    summary.append("M_OUT: " + str(m_out))
    summary.append("W: " + str(W))
    summary.append("W_ALLOW: " + str(W_allow))
    summary.append("WORK_ELIMINATED_FRACTION: " + f"{work_eliminated_fraction:.12f}")
    summary.append("STRUCTURAL_SPEEDUP: " + f"{structural_speedup:.12f}")
    summary.append("OMEGA: " + f"{Omega:.12f}")
    summary.append("K: " + str(K))
    summary.append("F: " + F)
    summary.append("")
    write_text(os.path.join(out_dir, "ssc_summary.txt"), "\n".join(summary))

    manifest_items = [
        "OIR_SSC_CORE.txt",
        "RUN.txt",
        "RUN_CONFIG.json",
        "SSC_CORE_CERTIFICATE.txt",
        "ssc_summary.txt",
        "ssc_trace.csv",
    ]

    lines = []
    for name in sorted(manifest_items):
        path = os.path.join(out_dir, name)
        digest = sha256_file(path)
        lines.append(digest + "  " + name)

    write_text(os.path.join(out_dir, "MANIFEST.sha256"), "\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
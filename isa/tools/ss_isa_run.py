import argparse
import csv
import hashlib
import json
import os

def file_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return sha256_bytes(f.read())

def norm_lines(text: str) -> str:
    return "\n".join(
        [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    ).rstrip() + "\n"

def write_text(path: str, text: str) -> None:
    with open(path, "wb") as f:
        f.write(norm_lines(text).encode("utf-8"))

def write_json(path: str, obj) -> None:
    s = json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    write_text(path, s)

def parse_program(path: str):
    raw = file_bytes(path).decode("utf-8", errors="strict")
    lines = [ln.strip() for ln in raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    lines = [ln for ln in lines if ln and not ln.startswith(";")]
    return lines

def compute_psi(w_allow: float, w: float) -> float:
    if w == 0:
        return 0.0
    return w_allow / w

def compute_omega(psis) -> float:
    return sum((1.0 - p) for p in psis)

def compute_k(gs) -> float:
    if len(gs) <= 1:
        return 0.0
    return sum(abs(gs[i] - gs[i - 1]) for i in range(1, len(gs)))

def compute_fingerprint(gs, psis, omega, k) -> str:
    payload = (
        f"g_stream={','.join([repr(x) for x in gs])}"
        f"|psi={','.join([repr(x) for x in psis])}"
        f"|Omega={repr(omega)}"
        f"|K={repr(k)}"
    )
    return sha256_bytes(payload.encode("utf-8"))

def write_manifest(dir_path: str, files):
    lines = []
    for rel in sorted(files):
        abspath = os.path.join(dir_path, rel)
        lines.append(f"{sha256_file(abspath)}  {rel}")
    write_text(os.path.join(dir_path, "MANIFEST.sha256"), "\n".join(lines))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--program", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", default="isa")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    program_lines = parse_program(args.program)

    state = {"m": None, "w_allow": None, "w": None}
    t = 0
    rows = []
    psis = []
    gs = []

    halted = False
    for ln in program_lines:
        parts = ln.split()
        op = parts[0].upper()

        if op == "SET":
            if len(parts) != 3:
                raise ValueError(f"Bad SET: {ln}")
            key = parts[1]
            val = float(parts[2])
            if key not in state:
                raise ValueError(f"Unknown key: {key}")
            state[key] = val

        elif op == "STEP":
            if state["m"] is None or state["w_allow"] is None or state["w"] is None:
                raise ValueError("STATE_INCOMPLETE")

            psi = compute_psi(state["w_allow"], state["w"])
            g = 1.0 - psi
            t += 1

            rows.append(
                {
                    "t": t,
                    "m": state["m"],
                    "w_allow": state["w_allow"],
                    "w": state["w"],
                    "Psi": psi,
                    "g": g,
                }
            )
            psis.append(psi)
            gs.append(g)

        elif op == "HALT":
            halted = True
            break

        else:
            raise ValueError(f"Unknown op: {op}")

    if not halted:
        raise ValueError("NO_HALT")

    omega = compute_omega(psis)
    k = compute_k(gs)
    f = compute_fingerprint(gs, psis, omega, k)

    trace_path = os.path.join(args.out, "isa_trace.csv")
    with open(trace_path, "w", newline="", encoding="utf-8") as fcsv:
        w = csv.DictWriter(fcsv, fieldnames=["t", "m", "w_allow", "w", "Psi", "g"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    summary = []
    summary.append(f"LABEL={args.label}")
    summary.append(f"N={len(rows)}")
    summary.append(f"Omega={repr(omega)}")
    summary.append(f"K={repr(k)}")
    summary.append(f"F={f}")
    write_text(os.path.join(args.out, "isa_summary.txt"), "\n".join(summary))

    cert = []
    cert.append("SSC-ISA CERTIFICATE")
    cert.append(f"LABEL={args.label}")
    cert.append(f"N={len(rows)}")
    cert.append(f"Omega={repr(omega)}")
    cert.append(f"K={repr(k)}")
    cert.append(f"F={f}")
    write_text(os.path.join(args.out, "SSC_ISA_CERTIFICATE.txt"), "\n".join(cert))

    program_rel = os.path.normpath(args.program).replace("\\", "/")
    program_hash = sha256_bytes(file_bytes(args.program))

    run_cfg = {
        "label": args.label,
        "program": program_rel,
        "program_sha256": program_hash,
        "spec": "SSC-ISA",
        "spec_version": "0.1",
    }
    write_json(os.path.join(args.out, "RUN_CONFIG.json"), run_cfg)

    run_txt = []
    run_txt.append("SSC-ISA RUN")
    run_txt.append(f"LABEL={args.label}")
    run_txt.append(f"PROGRAM={run_cfg['program']}")
    run_txt.append(f"PROGRAM_SHA256={run_cfg['program_sha256']}")
    run_txt.append(f"SPEC={run_cfg['spec']}")
    run_txt.append(f"SPEC_VERSION={run_cfg['spec_version']}")
    run_txt.append("TIME=DETERMINISTIC")
    write_text(os.path.join(args.out, "RUN.txt"), "\n".join(run_txt))

    files = [
        "isa_trace.csv",
        "isa_summary.txt",
        "SSC_ISA_CERTIFICATE.txt",
        "RUN_CONFIG.json",
        "RUN.txt",
    ]
    write_manifest(args.out, files)

    print("SSC_ISA_RUN: OK")
    print(f"N={len(rows)}")
    print(f"Omega={repr(omega)}")
    print(f"K={repr(k)}")
    print(f"F={f}")
    print("MANIFEST: WRITTEN")

if __name__ == "__main__":
    main()
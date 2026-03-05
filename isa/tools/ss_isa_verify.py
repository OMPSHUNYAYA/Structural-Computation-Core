import argparse
import hashlib
import os
import sys

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_manifest(path: str):
    entries = []
    with open(path, "rb") as f:
        raw = f.read().decode("utf-8", errors="strict")
    lines = [ln.strip() for ln in raw.replace("\r\n", "\n").replace("\r", "\n").split("\n") if ln.strip()]
    for ln in lines:
        parts = ln.split()
        if len(parts) < 2:
            raise ValueError("BAD_MANIFEST_LINE")
        digest = parts[0]
        rel = parts[1]
        entries.append((digest, rel))
    return entries

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    args = ap.parse_args()

    mpath = os.path.join(args.dir, "MANIFEST.sha256")
    if not os.path.exists(mpath):
        print("MANIFEST_MISSING")
        sys.exit(2)

    entries = load_manifest(mpath)
    ok = True
    for digest, rel in entries:
        fpath = os.path.join(args.dir, rel)
        if not os.path.exists(fpath):
            print(f"MISSING: {rel}")
            ok = False
            continue
        got = sha256_file(fpath)
        if got != digest:
            print(f"HASH_MISMATCH: {rel}")
            print(f"EXPECTED: {digest}")
            print(f"GOT:      {got}")
            ok = False

    if ok:
        print("SS_ISA_VERIFY: PASS")
        sys.exit(0)
    else:
        print("SS_ISA_VERIFY: FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
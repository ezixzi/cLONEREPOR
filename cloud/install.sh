#!/usr/bin/env bash
set -euo pipefail
cd /workspace
python3 - <<'PYBOOT'
from pathlib import Path
import hashlib, subprocess, sys, urllib.request
if sys.version_info < (3,12): raise SystemExit('Python3.12+ is required for the verified video runtime.')
script=Path('/workspace/cLONEREPOR/cloud/bootstrap_runtime.py')
expected_bootstrap='cc7ceab870fde3184f008ceec8cd776617a321c6b4661de44e886f75d52eaa98'
if not script.is_file() or hashlib.sha256(script.read_bytes()).hexdigest()!=expected_bootstrap:
    script=Path('/workspace/.cache/openmontage-bootstrap-v2.py')
    script.parent.mkdir(parents=True,exist_ok=True)
    with urllib.request.urlopen('https://raw.githubusercontent.com/ezixzi/cLONEREPOR/76f1af3d71654e97fd6b9695b74b85a55ef594e7/cloud/bootstrap_runtime.py',timeout=30) as response: data=response.read()
    if hashlib.sha256(data).hexdigest()!=expected_bootstrap: raise SystemExit('Bootstrap checksum mismatch')
    script.write_bytes(data)
subprocess.run([sys.executable,str(script),'--archive','/workspace/cLONEREPOR/OpenMontage-portable-neon-v2.zip','--archive-url','https://raw.githubusercontent.com/ezixzi/cLONEREPOR/76f1af3d71654e97fd6b9695b74b85a55ef594e7/OpenMontage-portable-neon-v2.zip','--sha256','7fa4ee1c9938c5255f802e0ffd4d678107d8ad4c4965f12311026b92f441dfb2'],check=True)
PYBOOT

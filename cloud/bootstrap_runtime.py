"""Verified, versioned OpenMontage runtime installer; never overlays a checkout."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request
import zipfile


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb')as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def verify_sources(engine):
    manifest=json.loads((engine/'PORTABLE-MANIFEST.json').read_text())
    for name,expected in manifest['files'].items():
        rel=Path(name)
        if rel.is_absolute()or'..'in rel.parts:raise RuntimeError('Unsafe manifest path')
        f=engine/rel
        if not f.is_file()or f.is_symlink()or digest(f)!=expected:raise RuntimeError('Source manifest verification failed: '+name)


def install(archive,expected,state,link,smoke=True):
    if digest(archive)!=expected:raise RuntimeError('Archive SHA256 mismatch; download stopped without extracting')
    state.mkdir(parents=True,exist_ok=True);release=state/'releases'/expected[:16];engine=release/'OpenMontage'
    if not engine.exists():
        release.parent.mkdir(parents=True,exist_ok=True)
        stage=Path(tempfile.mkdtemp(prefix='unpack-',dir=state))
        try:
            with zipfile.ZipFile(archive)as z:
                infos=z.infolist()
                if len(infos)>20000 or sum(i.file_size for i in infos)>2*1024**3:raise RuntimeError('Archive exceeds safety limits')
                for i in infos:
                    rel=Path(i.filename)
                    if rel.is_absolute()or'..'in rel.parts or not rel.parts or rel.parts[0]!='OpenMontage' or stat.S_ISLNK(i.external_attr>>16):raise RuntimeError('Unsafe archive member')
                z.extractall(stage)
            verify_sources(stage/'OpenMontage');stage.rename(release)
        finally:
            if stage.exists():shutil.rmtree(stage)
    verify_sources(engine)
    if link.exists()and not link.is_symlink():raise RuntimeError('Runtime link destination is a user directory; choose another --link')
    # The previous release remains intact. Atomic link replacement is reversible.
    temp_link=link.with_name(link.name+'.next')
    if temp_link.is_symlink():temp_link.unlink()
    temp_link.symlink_to(engine,target_is_directory=True);os.replace(temp_link,link)
    env=os.environ.copy()
    for key,suffix in [('PIP_CACHE_DIR','pip'),('npm_config_cache','npm'),('OPENMONTAGE_CACHE_DIR','clips')]:
        env.setdefault(key,str(state/'cache'/suffix));Path(env[key]).mkdir(parents=True,exist_ok=True)
    command=[sys.executable,str(engine/'portable/cloud_setup.py')]
    if smoke:command.append('--smoke')
    subprocess.run(command,cwd=engine,env=env,check=True)
    result={'runtime_path':str(link),'release_path':str(engine),'archive_sha256':expected,'source_manifest_verified':True,'bootstrap_passed':True,'scheduler_modified':False,'elevenlabs_authentication':'requires separate check after secret is ready'}
    (state/'readiness.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path);p.add_argument('--archive-url');p.add_argument('--sha256',required=True);p.add_argument('--state-dir',type=Path,default=Path('/workspace/.openmontage'));p.add_argument('--link',type=Path,default=Path('/workspace/openmontage-runtime'));p.add_argument('--skip-smoke',action='store_true');a=p.parse_args()
    if len(a.sha256)!=64 or any(c not in '0123456789abcdef'for c in a.sha256):raise SystemExit('Invalid pinned SHA256')
    archive=a.archive
    if not archive or not archive.is_file():
        if not a.archive_url:raise SystemExit('Missing archive and archive URL')
        a.state_dir.mkdir(parents=True,exist_ok=True);archive=a.state_dir/('archive-'+a.sha256[:16]+'.zip')
        if not archive.is_file()or digest(archive)!=a.sha256:
            temp=archive.with_suffix('.download')
            try:
                with urllib.request.urlopen(a.archive_url,timeout=45)as response,temp.open('wb')as out:shutil.copyfileobj(response,out)
                if digest(temp)!=a.sha256:raise RuntimeError('Downloaded archive SHA256 mismatch')
                temp.replace(archive)
            finally:
                if temp.exists():temp.unlink()
    install(archive,a.sha256,a.state_dir,a.link,not a.skip_smoke)

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Preview or explicitly create CMPUT 301 issues. Requires `gh` only for --create."""
import argparse, json, pathlib, shutil, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument('--create',action='store_true')
a=p.parse_args()
stories=json.loads((pathlib.Path(__file__).parent/'requirements.json').read_text())
assert len(stories)==61
if not a.create:
    for s in stories:
        print(f"{s['id']:12s} {s['points']:>2} SP  {s['risk']:<6} {s['checkpoint']:<7} {s['statement']}")
    print('\nPREVIEW ONLY; no changes to GitHub. To create: --create')
    sys.exit(0)
if not shutil.which('gh'): sys.exit('Install and authenticate GitHub CLI gh first.')
subprocess.run(['gh','auth','status'],check=True)
subprocess.run(['gh','repo','view'],check=True)
confirm=input('Type CREATE to create all 61 issues in the repository shown above: ')
if confirm!='CREATE': sys.exit('Stopped, no issues created.')
for role in ('entrant','owner','admin','wow'):
    subprocess.run(['gh','label','create',f'role:{role}','--color','BFD7EA','--force'],check=True)
for risk,color in (('low','2DA44E'),('medium','D4A72C'),('high','CF222E')):
    subprocess.run(['gh','label','create',f'risk:{risk}','--color',color,'--force'],check=True)
for cp,color in (('halfway','8250DF'),('final','6E7781')):
    subprocess.run(['gh','label','create',f'checkpoint:{cp}','--color',color,'--force'],check=True)
for s in stories:
    role=s['role'].lower()
    if role.startswith('campsite'): role='owner'
    elif role.startswith('wow'): role='wow'
    title=f"[{s['id']}] {s['statement']}"
    body=(f"## User story\n{s['statement']}\n\n"
          f"## Estimate\nStory points: **{s['points']}**\n\n"
          f"Risk: **{s['risk']}**\n\nRelease: **{s['checkpoint']}**\n\n"
          f"## Done when\n- [ ] {s['acceptance']}\n\n"
          f"## Mockup/Storyboard\nScreens: {', '.join(s['screens'])}; "
          f"Flow: {', '.join(s['flows'])}\n")
    labels=[f'role:{role}',f'risk:{s["risk"].lower()}',f'checkpoint:{s["checkpoint"].lower()}']
    subprocess.run(['gh','issue','create','--title',title,'--body',body,'--label',','.join(labels)],check=True)
    print('Created',s['id'])

"""Negative tests: plant one defect at a time in a copy of the built site and
confirm scripts/verify_pip_strip.py rejects it. Control run must exit 0."""
import os, shutil, subprocess, sys

ROOT = '/root/.hermes/profiles/developer/cache/scratch'
SRC = os.path.join(ROOT, 'site-rollout')
WT = '/root/.hermes/profiles/developer/cache/scratch/wt-piproll'
WORK = os.path.join(ROOT, 'negative')


def run_case(name, mutate=None, expect=1):
    dest = os.path.join(WORK, name)
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(SRC, dest)
    note = ''
    if mutate:
        note = mutate(dest) or ''
    out = subprocess.run([sys.executable, 'scripts/verify_pip_strip.py', '--base', dest,
                          '--archive', 'audit/archive/tables-2026-11-20'],
                         cwd=WT, capture_output=True, text=True)
    tail = [l for l in out.stdout.strip().splitlines() if l.startswith(('FAIL', '  protocols', 'OK'))]
    status = 'PASS' if out.returncode == expect else 'UNEXPECTED'
    print(f'{status:10s} {name:28s} EXIT={out.returncode} (expected {expect}) {note}')
    for l in tail[:3]:
        print('            ' + l)
    shutil.rmtree(dest, ignore_errors=True)
    return out.returncode == expect


def flip_state(dest):
    p = os.path.join(dest, 'protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.html')
    t = open(p, encoding='utf-8').read()
    old = 'data-states="no,no,no,go,go"'
    assert old in t
    open(p, 'w', encoding='utf-8').write(t.replace(old, 'data-states="no,no,no,call,go"', 1))
    return 'flipped one row state'


def drop_block(dest):
    p = os.path.join(dest, 'protocols/cardiac/04_Supraventricular_Tachycardia_PROC.html')
    t = open(p, encoding='utf-8').read()
    i = t.find('<div class="pip-block" data-pip-block>')
    j = t.find('</tbody></table></div>', i) + len('</tbody></table></div>')
    open(p, 'w', encoding='utf-8').write(t[:i] + t[j:])
    return 'removed one of three pip blocks'


def drop_marker(dest):
    p = os.path.join(dest, 'protocols/trauma/09_Crush_Syndrome_PROC.html')
    t = open(p, encoding='utf-8').read()
    i = t.find('<span class="pip-mark pip-mark-auth"')
    j = t.find('</span>', i) + len('</span>')
    open(p, 'w', encoding='utf-8').write(t[:i] + t[j:])
    return 'removed a * marker'


def change_number(dest):
    p = os.path.join(dest, 'procedures/CPAP.html')
    t = open(p, encoding='utf-8').read()
    old = '<td class="pip-n">3</td>'
    assert old in t
    open(p, 'w', encoding='utf-8').write(t.replace(old, '<td class="pip-n">99</td>', 1))
    return 'renumbered a row'


def touch_skipped(dest):
    p = os.path.join(dest, 'protocols/administrative/01_Communications_PROC.html')
    t = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(t.replace('<table>', '<table class="x">', 1))
    return 'edited a policy table'


def convert_skipped(dest):
    p = os.path.join(dest, 'protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.html')
    t = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(t.replace('<div class="lv-wrap pending">',
                                                   '<div class="pip-block" data-pip-block><div class="lv-wrap pending">', 1))
    return 'faked a strip on a PENDING page'


def drop_tally(dest):
    p = os.path.join(dest, 'protocols/general/02_Cold_Exposure_PROC.html')
    t = open(p, encoding='utf-8').read()
    i = t.find('<p class="pip-tally"')
    j = t.find('</p>', i) + 4
    open(p, 'w', encoding='utf-8').write(t[:i] + t[j:])
    return 'removed the tally (row count check)'


if __name__ == '__main__':
    os.makedirs(WORK, exist_ok=True)
    ok = [run_case('control', None, 0)]
    ok.append(run_case('A-flipped-row-state', flip_state))
    ok.append(run_case('B-missing-block', drop_block))
    ok.append(run_case('C-missing-marker', drop_marker))
    ok.append(run_case('D-renumbered-row', change_number))
    ok.append(run_case('E-policy-table-edited', touch_skipped))
    ok.append(run_case('F-fake-strip-on-pending', convert_skipped))
    ok.append(run_case('G-no-tally-count', drop_tally))
    print()
    print('all negative cases behaved as expected' if all(ok) else 'SOME CASES DID NOT BEHAVE AS EXPECTED')
    sys.exit(0 if all(ok) else 1)

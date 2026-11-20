"""Negative tests: plant one defect at a time in a copy of the built site and
confirm scripts/verify_pip_strip.py rejects it. Control run must exit 0."""
import os, shutil, subprocess, sys

WT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(WT)
SRC = os.environ.get('PIP_SITE', os.path.join(WT, 'site'))
WORK = os.path.join(ROOT, 'negative-pipstrip')


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


def pending_as_no(dest):
    p = os.path.join(dest, 'protocols/neurologic/05_Stroke_TIA_PROC.html')
    t = open(p, encoding='utf-8').read()
    old = 'data-states="pending,pending,pending,pending,pending" data-pending="1"><td class="pip-n">8'
    assert old in t
    open(p, 'w', encoding='utf-8').write(t.replace(
        old, 'data-states="no,no,no,no,no"><td class="pip-n">8', 1))
    return 'rendered a PENDING row as "not authorised at every level"'


def pending_no_attr(dest):
    p = os.path.join(dest, 'protocols/trauma/09_Burns_Thermal_PROC.html')
    t = open(p, encoding='utf-8').read()
    old = 'data-states="pending,pending,pending,pending,pending" data-pending="1"><td class="pip-n">6'
    assert old in t
    open(p, 'w', encoding='utf-8').write(t.replace(
        old, 'data-states="pending,pending,pending,pending,pending"><td class="pip-n">6', 1))
    return 'dropped data-pending from a PENDING row'


def pending_no_tag(dest):
    p = os.path.join(dest, 'protocols/neurologic/05_Stroke_TIA_PROC.html')
    t = open(p, encoding='utf-8').read()
    old = '<span class="pip-tag pending">PENDING \u2014 no published level</span>'
    assert old in t
    open(p, 'w', encoding='utf-8').write(t.replace(old, '', 1))
    return 'removed the PENDING tag'


def pending_untallied(dest):
    p = os.path.join(dest, 'protocols/neurologic/05_Stroke_TIA_PROC.html')
    t = open(p, encoding='utf-8').read()
    old = ' \u00b7 2 PENDING (no published level)'
    assert old in t
    open(p, 'w', encoding='utf-8').write(t.replace(old, '', 1))
    return 'hid the PENDING rows from the tally'


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
    ok.append(run_case('H-pending-as-not-authorised', pending_as_no))
    ok.append(run_case('I-pending-no-data-attr', pending_no_attr))
    ok.append(run_case('J-pending-no-tag', pending_no_tag))
    ok.append(run_case('K-pending-untallied', pending_untallied))
    print()
    print('all negative cases behaved as expected' if all(ok) else 'SOME CASES DID NOT BEHAVE AS EXPECTED')
    sys.exit(0 if all(ok) else 1)

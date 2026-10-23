import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/keycrumb-sheets/scripts/validate_sheet.py'


def minimal():
    return {'schemaVersion': 1, 'title': 'Editor', 'sections': [
        {'id': 'editing', 'title': 'Editing', 'entries': [
            {'id': 'find', 'title': 'Find', 'shortcuts': [
                {'steps': [{'modifiers': ['command'], 'key': 'f'}]}]}]}]}


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.sheet = self.root / 'editor.keycrumb.json'

    def run_sheet(self, data=None, expected=0):
        self.sheet.write_text(json.dumps(data or minimal()), encoding='utf-8')
        result = self.invoke()
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def invoke(self):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.sheet),
            '--library-root', str(self.root)], capture_output=True, text=True)

    def test_minimal_null_unknown_unicode_and_text_only(self):
        data = minimal()
        data.update(description=None, icon=None, futureProperty=True)
        entry = data['sections'][0]['entries'][0]
        entry['text'] = None
        for key in ['é', '😀', '\ue000', 'f24', 'arrowRight']:
            entry['shortcuts'][0]['steps'][0]['key'] = key
            self.run_sheet(data)
        entry['shortcuts'] = []
        self.run_sheet(data)

    def test_invalid_content(self):
        changes = [('schemaVersion', 2), ('title', '  '), ('title', 'x' * 201)]
        for field, value in changes:
            data = minimal()
            data[field] = value
            with self.subTest(field=field, value=str(value)[:10]):
                self.assertIn(field, self.run_sheet(data, 1))
        for step in [{'modifiers': ['command', 'command'], 'key': 'f'},
                     {'modifiers': ['meta'], 'key': 'f'},
                     {'modifiers': [], 'key': 'two'},
                     {'modifiers': [], 'key': '\u200b'}]:
            data = minimal()
            data['sections'][0]['entries'][0]['shortcuts'][0]['steps'] = [step]
            self.assertIn('shortcuts', self.run_sheet(data, 1))

    def test_duplicate_ids_and_entry_overflow(self):
        data = minimal()
        second = copy.deepcopy(data['sections'][0])
        second['id'] = 'other'
        data['sections'].append(second)
        self.assertIn('duplicate entry', self.run_sheet(data, 1))
        second['entries'][0]['id'] = 'other-find'
        second['id'] = 'editing'
        self.assertIn('duplicate section', self.run_sheet(data, 1))
        data['sections'][0]['id'] = 'é'
        data['sections'][1]['id'] = 'e\u0301'
        self.assertIn('duplicate section', self.run_sheet(data, 1))
        data['sections'] = [{'id': str(i), 'title': 'Group', 'entries': [
            {'id': f'{i}-{j}', 'title': 'Text', 'shortcuts': []} for j in range(200)]}
            for i in range(11)]
        self.assertIn('2000', self.run_sheet(data, 1))

    def test_sequences_alternatives_and_limits(self):
        data = minimal()
        shortcut = data['sections'][0]['entries'][0]['shortcuts'][0]
        shortcut['steps'] *= 8
        data['sections'][0]['entries'][0]['shortcuts'] = [copy.deepcopy(shortcut)] * 4
        self.run_sheet(data)
        shortcut['steps'].append({'modifiers': [], 'key': 'x'})
        data['sections'][0]['entries'][0]['shortcuts'][0] = shortcut
        self.run_sheet(data, 1)

    def test_icon_warning_cases_and_valid_png(self):
        from PIL import Image
        icon = self.root / 'icon.png'
        data = minimal()
        for path in ['missing.png', 'https://example.com/icon.png', '/icon.png',
                     '../icon.png', '%2e%2e/icon.png']:
            data['icon'] = path
            self.assertIn('warning: $.icon', self.run_sheet(data))
        data['icon'] = 'icon.png'
        for size in [(256, 256), (128, 256)]:
            Image.new('RGBA', size, 'red').save(icon)
            out = self.run_sheet(data)
            self.assertEqual('warning:' in out, size != (256, 256))
        Image.new('RGB', (256, 256), 'red').save(icon, format='JPEG')
        self.assertIn('warning:', self.run_sheet(data))
        icon.write_bytes(b'\x89PNG\r\n\x1a\n')
        self.assertIn('warning:', self.run_sheet(data))
        icon.write_bytes(b'x' * 262145)
        self.assertIn('warning:', self.run_sheet(data))
        Image.new('RGBA', (256, 256), 'red').save(icon, save_all=True,
            append_images=[Image.new('RGBA', (256, 256), 'blue')], duration=100)
        self.assertIn('warning:', self.run_sheet(data))
        outside = self.root.parent / (self.root.name + '-outside.png')
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        Image.new('RGBA', (256, 256)).save(outside)
        icon.unlink()
        icon.symlink_to(outside)
        self.assertIn('warning:', self.run_sheet(data))

    def test_file_boundary_and_read_only(self):
        self.run_sheet()
        before = self.sheet.read_bytes(), self.sheet.stat().st_mtime_ns
        self.assertEqual(self.invoke().returncode, 0)
        self.assertEqual(before, (self.sheet.read_bytes(), self.sheet.stat().st_mtime_ns))
        self.sheet.write_bytes(b'\xff')
        self.assertEqual(self.invoke().returncode, 1)
        self.sheet.write_bytes(b' ' * (2 * 1024 * 1024 + 1))
        self.assertEqual(self.invoke().returncode, 1)
        self.sheet.unlink()
        self.sheet.symlink_to(self.root / 'absent.keycrumb.json')
        self.assertEqual(self.invoke().returncode, 1)
        self.sheet.unlink()
        self.sheet = self.root / '.hidden.keycrumb.json'
        self.run_sheet(expected=1)
        self.sheet = self.root / 'sub' / 'nested.keycrumb.json'
        self.sheet.parent.mkdir()
        self.run_sheet(expected=1)

    def test_invalid_json_tokens_and_surrogates(self):
        self.sheet.write_text(json.dumps(minimal())[:-1] + ',"unknown":NaN}')
        self.assertEqual(self.invoke().returncode, 1)
        data = minimal()
        data['title'] = '\ud800'
        self.run_sheet(data, 1)

    def test_invocation_and_missing_dependency(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.sheet.write_text(json.dumps(minimal()))
        result = subprocess.run([sys.executable, '-S', str(SCRIPT), str(self.sheet),
            '--library-root', str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'dependenc', result.stderr)


if __name__ == '__main__':
    unittest.main()

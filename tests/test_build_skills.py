import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / 'skills/keycrumb-sheets'


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def build(self, output, repo=REPO, version='0.1.0'):
        return subprocess.run([sys.executable, str(repo / 'scripts/build_skills.py'),
            '--version', version, '--output-dir', str(output)], capture_output=True, text=True)

    def test_reproducible_complete_portable_archives(self):
        first, second = self.root / 'one', self.root / 'two'
        result = self.build(first)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.build(second).returncode, 0)
        self.assertEqual({p.name for p in first.iterdir()}, {
            'keycrumb-sheets-0.1.0.zip', 'keycrumb-skills-plugin-0.1.0.zip', 'SHA256SUMS'})
        for source in first.iterdir():
            self.assertEqual(source.read_bytes(), (second / source.name).read_bytes())
        for line in (first / 'SHA256SUMS').read_text().splitlines():
            digest, name = line.split('  ')
            self.assertEqual(digest, hashlib.sha256((first / name).read_bytes()).hexdigest())
        for name, location in [('keycrumb-sheets-0.1.0.zip', 'keycrumb-sheets'),
                               ('keycrumb-skills-plugin-0.1.0.zip', 'skills/keycrumb-sheets')]:
            extracted = self.root / name.removesuffix('.zip')
            with zipfile.ZipFile(first / name) as archive:
                self.assertFalse(any('AGENTS.md' in x or x.startswith(('Casks/', 'tests/', '.git'))
                                     for x in archive.namelist()))
                archive.extractall(extracted)
            installed = extracted / location
            for markdown in installed.rglob('*.md'):
                prose = re.sub(r'```.*?```|`[^`]*`', '', markdown.read_text(), flags=re.S)
                for link in re.findall(r'\]\(([^)]+)\)', prose):
                    if '://' not in link:
                        self.assertTrue((markdown.parent / link.split('#')[0]).exists(), link)
            example = installed / 'assets/example-library'
            result = subprocess.run([sys.executable, str(installed / 'scripts/validate_sheet.py'),
                str(example / 'editor.keycrumb.json'), '--library-root', str(example)],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn('warning:', result.stdout)
            from PIL import Image
            with Image.open(example / 'images/workflow.png') as illustration:
                illustration.load()
            if name.startswith('keycrumb-skills-plugin'):
                self.assertTrue((extracted / 'LICENSE.txt').is_file())
                self.assertTrue((extracted / 'plugin.json').is_file())

    def test_version_mismatch_and_symlink_rejected(self):
        self.assertNotEqual(self.build(self.root / 'bad', version='0.2.0').returncode, 0)
        copy = self.root / 'repo'
        shutil.copytree(REPO / 'scripts', copy / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(SKILL, copy / 'skills/keycrumb-sheets')
        shutil.copy(REPO / 'plugin.json', copy / 'plugin.json')
        shutil.copy(REPO / 'LICENSE-skills.txt', copy / 'LICENSE-skills.txt')
        target = copy / 'skills/keycrumb-sheets/assets/example-library/icons/editor.png'
        target.unlink()
        target.symlink_to(SKILL / 'assets/example-library/icons/editor.png')
        self.assertNotEqual(self.build(self.root / 'linked', repo=copy).returncode, 0)

    def test_cask_paths_and_release_verification_gate(self):
        import yaml
        workflow = yaml.load((REPO / '.github/workflows/ci.yml').read_text(), Loader=yaml.BaseLoader)
        for event in ['push', 'pull_request']:
            self.assertIn('Casks/**', workflow['on'][event]['paths'])
            self.assertIn('.github/workflows/ci.yml', workflow['on'][event]['paths'])
            self.assertNotIn('skills/**', workflow['on'][event]['paths'])
        release = yaml.load((REPO / '.github/workflows/skills-release.yml').read_text(),
                            Loader=yaml.BaseLoader)
        self.assertEqual(release['permissions'], {'contents': 'read'})
        self.assertEqual(release['jobs']['package']['needs'], 'verify')
        self.assertEqual(release['jobs']['release']['needs'], 'package')
        self.assertEqual(release['jobs']['release']['permissions'], {'contents': 'write'})

    def test_metadata_schema_provenance_and_references(self):
        import yaml
        frontmatter = (SKILL / 'SKILL.md').read_text().split('---', 2)[1]
        metadata = yaml.safe_load(frontmatter)
        self.assertEqual(metadata['name'], 'keycrumb-sheets')
        self.assertTrue(metadata['description'])
        self.assertNotIn('TODO', (SKILL / 'SKILL.md').read_text())
        interface = yaml.safe_load((SKILL / 'agents/openai.yaml').read_text())
        self.assertNotEqual(interface.get('policy', {}).get('allow_implicit_invocation'), False)
        provenance = json.loads((SKILL / 'references/format-provenance.json').read_text())
        self.assertEqual(provenance['schemaSHA256'], hashlib.sha256(
            (SKILL / 'references/keycrumb-sheet.schema.json').read_bytes()).hexdigest())
        manifest = json.loads((REPO / 'plugin.json').read_text())
        self.assertEqual(manifest['$schema'], 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        self.assertFalse(any(k in manifest for k in ['mcpServers', 'apps', 'hooks']))


if __name__ == '__main__':
    unittest.main()

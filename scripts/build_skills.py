"""Build deterministic, allowlisted skill archives without publishing anything."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

SKILL_FILES = (
    'SKILL.md', 'LICENSE.txt', 'agents/openai.yaml',
    'references/markdown.md', 'references/json-format.md',
    'references/keycrumb-sheet.schema.json', 'references/format-provenance.json',
    'assets/example-library/commands.md', 'assets/example-library/editor.keycrumb.json',
    'assets/example-library/icons/editor.png', 'assets/example-library/images/workflow.png',
    'assets/example-library/ATTRIBUTION.txt',
    'scripts/validate_sheet.py', 'scripts/requirements.txt',
)


def write_archive(destination, entries):
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(entries):
            metadata = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            metadata.compress_type = zipfile.ZIP_DEFLATED
            metadata.create_system = 3
            metadata.external_attr = 0o100644 << 16
            archive.writestr(metadata, data, compresslevel=9)


def build(repo, version, output):
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('version must be MAJOR.MINOR.PATCH')
    manifest_path = repo / 'plugin.json'
    if manifest_path.is_symlink():
        raise ValueError('plugin.json must not be a symlink')
    license_path = repo / 'LICENSE-skills.txt'
    if license_path.is_symlink() or not license_path.is_file():
        raise ValueError('LICENSE-skills.txt must be a regular file')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('version') != version:
        raise ValueError('requested version must match plugin.json')
    if (manifest.get('$schema') != 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
            or manifest.get('name') != 'keycrumb-skills'
            or set(manifest) - {'$schema', 'name', 'version', 'description', 'author',
                                'homepage', 'repository', 'license'}):
        raise ValueError('expected the minimal skills-only Agent Plugins manifest')
    skill = repo / 'skills/keycrumb-sheets'
    resources = []
    for relative in SKILL_FILES:
        source = skill / relative
        if (any(part.is_symlink() for part in [source, *source.parents] if part != repo.parent)
                or not source.is_file()):
            raise ValueError(f'missing or symlinked package resource: {relative}')
        resources.append((relative, source.read_bytes()))
    output.mkdir(parents=True, exist_ok=True)
    standalone = output / f'keycrumb-sheets-{version}.zip'
    plugin = output / f'keycrumb-skills-plugin-{version}.zip'
    write_archive(standalone, [('keycrumb-sheets/' + name, data) for name, data in resources])
    write_archive(plugin, [('plugin.json', manifest_path.read_bytes()),
                           ('LICENSE.txt', license_path.read_bytes())] + [
        ('skills/keycrumb-sheets/' + name, data) for name, data in resources])
    checksums = ''.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n'
                        for path in sorted([standalone, plugin]))
    (output / 'SHA256SUMS').write_text(checksums, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        build(Path(__file__).resolve().parents[1], args.version, args.output_dir)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()

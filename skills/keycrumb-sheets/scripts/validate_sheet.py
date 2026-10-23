"""Read-only KeyCrumb v1 structural checks. Icon failures are warnings, like the app."""
import argparse
import io
import json
import os
from pathlib import Path
import stat
import sys
import unicodedata
from urllib.parse import unquote, urlsplit
import warnings

MAX_SHEET = 2 * 1024 * 1024
MAX_ICON = 262144


def bounded_read(path, limit):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as file:
        info = os.fstat(file.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError(f'expected regular file at most {limit} bytes')
        data = file.read(limit + 1)
        if len(data) > limit:
            raise ValueError(f'exceeds {limit} bytes')
        return data


def icon_warning(value, root, image_module):
    try:
        if urlsplit(value).scheme or value.startswith('/'):
            raise ValueError('use a local path relative to the library')
        path = (root / unquote(value)).resolve()
        if not path.is_relative_to(root) or path == root:
            raise ValueError('path escapes the library')
        if path.suffix.lower() != '.png':
            raise ValueError('icon must have a .png extension')
        data = bounded_read(path, MAX_ICON)
        with warnings.catch_warnings():
            warnings.simplefilter('error', image_module.DecompressionBombWarning)
            with image_module.open(io.BytesIO(data)) as image:
                if image.format != 'PNG' or image.size != (256, 256) or image.n_frames != 1:
                    raise ValueError('expected static PNG, exactly 256 x 256 pixels')
                image.verify()
            with image_module.open(io.BytesIO(data)) as image:
                image.load()
    except (OSError, ValueError, SyntaxError, image_module.DecompressionBombWarning,
            image_module.DecompressionBombError, EOFError) as error:
        return str(error)
    return None


def reject_constant(value):
    raise ValueError(f'invalid JSON numeric token: {value}')


def invalid_scalars(value, path='$'):
    if isinstance(value, str):
        if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            yield path, 'unpaired surrogate is not a Unicode scalar'
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from invalid_scalars(item, f'{path}[{index}]')
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from invalid_scalars(key, path)
            yield from invalid_scalars(item, path + '.' + key)


def validate(sheet, root, validator, image_module):
    errors, notices = [], []
    try:
        if sheet.is_symlink() or sheet.name.startswith('.') or not sheet.name.endswith('.keycrumb.json'):
            raise ValueError('use a nonhidden, nonsymlink .keycrumb.json sheet')
        if sheet.absolute().parent.resolve() != root:
            raise ValueError('sheet must be at the top level of --library-root')
        document = json.loads(bounded_read(sheet, MAX_SHEET).decode('utf-8'),
                              parse_constant=reject_constant)
    except (OSError, ValueError, UnicodeError) as error:
        return [('$', str(error))], []
    errors.extend(invalid_scalars(document))
    if errors:
        return errors, notices
    for error in validator.iter_errors(document):
        errors.append((error.json_path, error.message))
    if errors:
        return errors, notices
    section_ids, entry_ids = set(), set()
    total = 0
    for i, section in enumerate(document['sections']):
        section_path = f'$.sections[{i}]'
        section_id = unicodedata.normalize('NFC', section['id'])
        if section_id in section_ids:
            errors.append((section_path + '.id', 'duplicate section ID'))
        section_ids.add(section_id)
        total += len(section['entries'])
        for j, entry in enumerate(section['entries']):
            entry_path = f'{section_path}.entries[{j}]'
            entry_id = unicodedata.normalize('NFC', entry['id'])
            if entry_id in entry_ids:
                errors.append((entry_path + '.id', 'duplicate entry ID across sections'))
            entry_ids.add(entry_id)
            for k, shortcut in enumerate(entry['shortcuts']):
                for n, step in enumerate(shortcut['steps']):
                    key = step['key']
                    if len(key) == 1 and unicodedata.category(key) in {'Cc', 'Cf', 'Cs'}:
                        errors.append((f'{entry_path}.shortcuts[{k}].steps[{n}].key',
                                       'key must be a printable Unicode scalar'))
    if total > 2000:
        errors.append(('$.sections', 'maximum 2000 entries overall'))
    for path, item in [('$', document)] + [
            (f'$.sections[{i}]', section) for i, section in enumerate(document['sections'])]:
        if item.get('icon') is not None:
            message = icon_warning(item['icon'], root, image_module)
            if message:
                notices.append((path + '.icon', message + '; KeyCrumb displays a placeholder'))
    return errors, notices


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sheet', type=Path)
    parser.add_argument('--library-root', type=Path, required=True)
    args = parser.parse_args()
    if not args.library_root.is_dir():
        parser.error('--library-root must be an existing directory')
    try:
        from jsonschema import Draft202012Validator
        from PIL import Image
    except ImportError:
        print('Missing optional validator dependencies; install scripts/requirements.txt in a venv.',
              file=sys.stderr)
        return 2
    schema_path = Path(__file__).resolve().parents[1] / 'references/keycrumb-sheet.schema.json'
    try:
        schema = json.loads(schema_path.read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(schema)
    except (OSError, ValueError) as error:
        print(f'Cannot load bundled schema: {error}', file=sys.stderr)
        return 2
    errors, notices = validate(args.sheet, args.library_root.resolve(),
                              Draft202012Validator(schema), Image)
    for level, diagnostics in [('error', errors), ('warning', notices)]:
        for path, message in diagnostics:
            print(f'{args.sheet}: {level}: {path}: {message}')
    if not errors:
        print(f'{args.sheet}: format checked; shortcut accuracy and native rendering not checked')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

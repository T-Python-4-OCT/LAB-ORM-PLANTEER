import ast
import struct

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


def parse_po(source):
    translations = {}
    entry = {}
    current_field = None
    fuzzy = False

    def has_translation():
        return any(field.startswith("msgstr") for field in entry)

    def finish_entry():
        nonlocal current_field, fuzzy

        if "msgid" in entry and not fuzzy:
            message_id = entry["msgid"]
            if "msgctxt" in entry:
                message_id = f"{entry['msgctxt']}\x04{message_id}"

            if "msgid_plural" in entry:
                message_id = f"{message_id}\x00{entry['msgid_plural']}"
                plural_indexes = (
                    int(field.removeprefix("msgstr[").removesuffix("]"))
                    for field in entry
                    if field.startswith("msgstr[")
                )
                plural_count = max(plural_indexes, default=-1) + 1
                translation = "\x00".join(
                    entry.get(f"msgstr[{index}]", "") for index in range(plural_count)
                )
            else:
                translation = entry.get("msgstr", "")

            if translation.replace("\x00", "") or message_id == "":
                translations[message_id] = translation

        entry.clear()
        current_field = None
        fuzzy = False

    for line_number, line in enumerate(source.splitlines(), start=1):
        line = line.strip()

        if line.startswith("#,"):
            if has_translation():
                finish_entry()
            fuzzy = any(flag.strip() == "fuzzy" for flag in line[2:].split(","))
            continue
        if not line or line.startswith("#"):
            continue

        if line.startswith('"'):
            if current_field is None:
                raise CommandError(f"Line {line_number}: string without a keyword")
            entry[current_field] += ast.literal_eval(line)
            continue

        field, _, value = line.partition(" ")
        if field in ("msgctxt", "msgid") and has_translation():
            finish_entry()
        if field not in ("msgctxt", "msgid", "msgid_plural", "msgstr") and not field.startswith("msgstr["):
            raise CommandError(f"Line {line_number}: unexpected {field!r}")

        current_field = field
        entry[field] = ast.literal_eval(value)

    finish_entry()
    return translations


def build_mo(translations):
    messages = sorted(translations.items())
    message_ids = [message_id.encode("utf-8") for message_id, _ in messages]
    translated_strings = [translation.encode("utf-8") for _, translation in messages]

    header_size = struct.calcsize("<7I")
    table_size = len(messages) * struct.calcsize("<2I")
    ids_offset = header_size
    translations_offset = ids_offset + table_size
    data_offset = translations_offset + table_size

    header = struct.pack("<7I", 0x950412DE, 0, len(messages), ids_offset, translations_offset, 0, 0)
    offsets = bytearray()
    data = bytearray()

    for value in message_ids + translated_strings:
        offsets.extend(struct.pack("<2I", len(value), data_offset + len(data)))
        data.extend(value)
        data.append(0)

    return header + offsets + data


class Command(BaseCommand):
    help = "Compile .po translation files to .mo (no GNU gettext required)."

    def handle(self, *args, **options):
        catalogs = [
            catalog
            for locale_directory in settings.LOCALE_PATHS
            for catalog in sorted(locale_directory.glob("*/LC_MESSAGES/*.po"))
        ]
        if not catalogs:
            raise CommandError("No .po files found in LOCALE_PATHS.")

        for catalog in catalogs:
            translations = parse_po(catalog.read_text(encoding="utf-8"))
            catalog.with_suffix(".mo").write_bytes(build_mo(translations))
            relative_path = catalog.relative_to(settings.BASE_DIR)
            self.stdout.write(f"Compiled {relative_path} ({len(translations) - 1} messages)")

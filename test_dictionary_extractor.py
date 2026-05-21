import tempfile
import unittest
from pathlib import Path

import zstandard as zstd

from patch_aov_camera import (
    TARGET_ENTRIES,
    encode_entry,
    extract_raw_dict_from_assets,
    read_entry_dict_ids,
    read_target_entry_data,
)
import zipfile


def build_test_dictionary() -> bytes:
    samples = []
    for i in range(80):
        samples.append(
            (
                f'<?xml version="1.0" encoding="utf-8"?><Project><Action name="sample{i}">'
                f'<Track trackName="Move{i}" eventType="None"><Event time="0.{i:03d}" /></Track>'
                '</Action></Project>'
            ).encode("utf-8")
        )
    return zstd.train_dictionary(8192, samples).as_bytes()


def build_test_package(pkg_path: Path, raw_dict: bytes) -> None:
    zdict = zstd.ZstdCompressionDict(raw_dict)
    with zipfile.ZipFile(pkg_path, "w", compression=zipfile.ZIP_STORED) as zout:
        for entry in TARGET_ENTRIES:
            xml = (
                '\ufeff<?xml version="1.0" encoding="utf-8"?>\n'
                '<Project><Action actionName="test">'
                f'<String name="entry" value="{entry}" />'
                '</Action></Project>'
            )
            zout.writestr(entry, encode_entry(xml, zdict, level=10))


class DictionaryExtractorTests(unittest.TestCase):
    def test_extracts_raw_zstd_dictionary_from_resources_using_commonactions_validation(self):
        raw_dict = build_test_dictionary()

        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            resources_path = tmp / "resources.assets"
            resources_path.write_bytes(b"asset-prefix" + raw_dict + b"asset-tail")
            pkg_path = tmp / "CommonActions.pkg.bytes"
            build_test_package(pkg_path, raw_dict)

            extracted = extract_raw_dict_from_assets(
                resources_path,
                required_ids=read_entry_dict_ids(pkg_path),
                entry_data=read_target_entry_data(pkg_path),
            )

        self.assertEqual(extracted.offset, len(b"asset-prefix"))
        self.assertEqual(extracted.data, raw_dict)


class OutputNameTests(unittest.TestCase):
    def test_repeated_commonactions_extension_is_normalized_to_original_name(self):
        from patch_camera_gui import normalize_output_path

        bad_path = Path(r"C:\Game\Out\CommonActions.pkg.bytes.pkg.bytes.pkg.bytes")

        output = normalize_output_path(bad_path)

        self.assertEqual(output, Path(r"C:\Game\Out\CommonActions.pkg.bytes"))

    def test_output_folder_always_uses_original_commonactions_file_name(self):
        from patch_camera_gui import output_path_from_folder

        output = output_path_from_folder(Path(r"C:\Game\Out"))

        self.assertEqual(output, Path(r"C:\Game\Out\CommonActions.pkg.bytes"))

    def test_default_output_file_keeps_original_commonactions_name_in_mod_folder(self):
        from patch_camera_gui import CameraPatchGui
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            source = tmp / "CommonActions.pkg.bytes"
            source.write_bytes(b"placeholder")

            gui = CameraPatchGui.__new__(CameraPatchGui)
            class FakeVar:
                def get(self):
                    return str(source)
            gui.input_path = FakeVar()

            output = CameraPatchGui._guess_output_path(gui)

        self.assertEqual(output.name, "CommonActions.pkg.bytes")
        self.assertEqual(output.parent.name, "CommonActions_mod")


if __name__ == "__main__":
    unittest.main()

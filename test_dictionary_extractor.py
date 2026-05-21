import unittest
from pathlib import Path

import zstandard as zstd

from patch_aov_camera import BYTESDICT_MAGIC, extract_raw_dict_from_assets


class DictionaryExtractorTests(unittest.TestCase):
    def test_extracts_raw_zstd_dictionary_from_app_resources_using_bytesdict_size(self):
        root = Path(__file__).resolve().parent
        raw_dict = (root / "zstd_dict.bin").read_bytes()

        import tempfile

        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            app_dir = tmp / "kgvn.app"
            resources_dir = app_dir / "Data"
            resources_dir.mkdir(parents=True)
            resources_path = resources_dir / "resources.assets"
            resources_path.write_bytes(b"asset-prefix" + raw_dict + b"asset-tail")

            bytesdict_path = tmp / "bytesDict.bytes"
            bytesdict_path.write_bytes(
                BYTESDICT_MAGIC
                + len(raw_dict).to_bytes(4, "little")
                + (b"\x00" * 16)
                + b"encrypted-payload-placeholder"
            )

            extracted = extract_raw_dict_from_assets(app_dir, bytesdict_path)

        self.assertEqual(extracted.offset, len(b"asset-prefix"))
        self.assertEqual(extracted.data, raw_dict)
        self.assertEqual(
            extracted.dict_id,
            zstd.ZstdCompressionDict(raw_dict).dict_id(),
        )


if __name__ == "__main__":
    unittest.main()

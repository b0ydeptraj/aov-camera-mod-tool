import tempfile
import unittest
from pathlib import Path

from resourceverification_analyzer import (
    COMMONACTIONS_RESOURCE_ID,
    RESOURCEVERIFICATION_NAME,
    analyze_resourceverification,
    contains_commonactions,
    resolve_resourceverification,
)


class ResourceVerificationAnalyzerTests(unittest.TestCase):
    def test_detects_commonactions_name(self):
        self.assertTrue(contains_commonactions(b"abc CommonActions.pkg.bytes xyz"))

    def test_detects_commonactions_resource_id(self):
        self.assertTrue(contains_commonactions(b"abc" + COMMONACTIONS_RESOURCE_ID + b"xyz"))

    def test_accepts_file_without_commonactions(self):
        self.assertFalse(contains_commonactions(b"ResourceVerificationInfoSetXML"))

    def test_resolves_from_resources_folder(self):
        with tempfile.TemporaryDirectory() as tmp_name:
            root = Path(tmp_name)
            expected = root / "assetbundle" / RESOURCEVERIFICATION_NAME
            expected.parent.mkdir()
            expected.write_bytes(b"data")

            self.assertEqual(resolve_resourceverification(root), expected)

    def test_analyze_reports_hash_and_flags(self):
        with tempfile.TemporaryDirectory() as tmp_name:
            path = Path(tmp_name) / RESOURCEVERIFICATION_NAME
            path.write_bytes(b"abc CommonActions.pkg.bytes xyz")

            report = analyze_resourceverification(path)

            self.assertEqual(report["path"], str(path))
            self.assertEqual(report["size"], len(b"abc CommonActions.pkg.bytes xyz"))
            self.assertEqual(report["md5"], "820b252a894bca4b04f2c0cea781adaf")
            self.assertTrue(report["contains_commonactions_name_or_path"])
            self.assertFalse(report["contains_commonactions_resource_id"])
            self.assertTrue(report["contains_commonactions"])


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from utils.validators import load_pipeline_config, validate_samplesheet  # noqa: E402


class LoadPipelineConfigTest(unittest.TestCase):
    def test_loads_known_pipeline_config(self):
        config = load_pipeline_config("rnaseq")

        self.assertIsNotNone(config)
        self.assertEqual(config["name"], "rnaseq")
        self.assertIn("samplesheet", config)

    def test_unknown_pipeline_returns_none(self):
        self.assertIsNone(load_pipeline_config("unknown-pipeline"))

    def test_validate_samplesheet_recognizes_known_pipeline(self):
        result = validate_samplesheet([], "rnaseq")

        self.assertEqual(result.errors, ["Samplesheet is empty - no samples found"])


if __name__ == "__main__":
    unittest.main()

"""Tests for download-host validation and URL encoding in ncbi_utils.

ncbi_utils is loaded directly (not via the ``utils`` package) so the suite can
run without the package's optional ``yaml`` dependency installed.
"""
import importlib.util
import unittest
from pathlib import Path
from urllib.parse import quote


_NCBI_UTILS_PATH = Path(__file__).resolve().parents[1] / "utils" / "ncbi_utils.py"
_spec = importlib.util.spec_from_file_location("ncbi_utils", _NCBI_UTILS_PATH)
ncbi_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ncbi_utils)


class IsTrustedDownloadHostTest(unittest.TestCase):
    def test_accepts_known_ena_and_ncbi_hosts(self):
        for url in (
            "http://ftp.sra.ebi.ac.uk/vol1/fastq/SRR635/SRR6357070_1.fastq.gz",
            "https://ftp.sra.ebi.ac.uk/vol1/x.fastq.gz",
            "https://ftp.ncbi.nlm.nih.gov/x.fastq.gz",
            "ftp://ftp.sra.ebi.ac.uk/x",
        ):
            self.assertTrue(ncbi_utils._is_trusted_download_host(url), url)

    def test_rejects_untrusted_and_lookalike_hosts(self):
        for url in (
            "http://evil.example.com/x.gz",
            "http://ftp.sra.ebi.ac.uk.evil.com/x.gz",  # suffix spoof
            "https://notebi.ac.uk.attacker.net/x",
            "",
            "not-a-url",
        ):
            self.assertFalse(ncbi_utils._is_trusted_download_host(url), url)


class DownloadFileHostGuardTest(unittest.TestCase):
    def test_untrusted_host_is_refused_before_writing(self):
        target = Path(__file__).resolve().parent / "_should_not_be_created.gz"
        self.addCleanup(lambda: target.exists() and target.unlink())

        result = ncbi_utils.download_file(
            "http://evil.example.com/x.gz", target, show_progress=False
        )

        self.assertFalse(result)
        self.assertFalse(target.exists())


class UrlEncodingTest(unittest.TestCase):
    def test_quote_neutralizes_injection_characters(self):
        # Sanity check on the encoding applied to user-supplied accessions:
        # query-string metacharacters must not pass through unescaped.
        encoded = quote("GSE1 OR foo[All]&db=evil", safe="")
        for forbidden in (" ", "&", "[", "]"):
            self.assertNotIn(forbidden, encoded)


if __name__ == "__main__":
    unittest.main()

import tempfile, unittest
from pathlib import Path
from phone_agent.security import safe_path

class SecurityTests(unittest.TestCase):
    def test_inside_path(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / "a").mkdir()
            self.assertEqual(safe_path(root, "a"), root / "a")
    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(PermissionError): safe_path(Path(d), "../escape")

if __name__ == "__main__": unittest.main()

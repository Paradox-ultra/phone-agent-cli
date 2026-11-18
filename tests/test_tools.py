import tempfile, unittest
from phone_agent.tools import call_tool

class ToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = {"workspace": self.tmp.name, "shell_enabled": False, "shell_allowlist": []}
    def tearDown(self): self.tmp.cleanup()
    def test_write_read(self):
        call_tool("workspace.write", {"path": "note.txt", "content": "hello"}, self.cfg)
        self.assertEqual(call_tool("workspace.read", {"path": "note.txt"}, self.cfg)["content"], "hello")
    def test_shell_disabled(self):
        with self.assertRaises(PermissionError): call_tool("shell.exec", {"argv": ["pwd"]}, self.cfg)

if __name__ == "__main__": unittest.main()

class SystemInfoTests(unittest.TestCase):
    def test_system_info(self):
        info = call_tool("system.info", {}, {})
        self.assertIn("platform", info)
        self.assertIn("python", info)
        self.assertIn("termux", info)

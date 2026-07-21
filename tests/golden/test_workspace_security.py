from __future__ import annotations

import importlib.util
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_workspace():
    path = ROOT / "scripts/golden/workspace.py"
    if not path.is_file():
        raise AssertionError("P3-RED-PARENT-ESCAPE")
    spec = importlib.util.spec_from_file_location("golden_workspace", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkspaceSecurityTests(unittest.TestCase):
    def test_parent_escape_is_rejected(self) -> None:
        workspace = load_workspace()
        with self.assertRaisesRegex(workspace.WorkspaceError, "WORKSPACE_PATH_INVALID"):
            workspace.validate_relative_path("../foreign")

    def test_symlink_swap_and_foreign_destination_are_rejected(self) -> None:
        path = ROOT / "scripts/golden/workspace.py"
        if not path.is_file():
            self.fail("P3-RED-SYMLINK-TOCTOU\nP3-RED-FOREIGN-DESTINATION")
        workspace = load_workspace()
        with tempfile.TemporaryDirectory() as temp:
            parent = pathlib.Path(temp)
            (parent / "foreign").mkdir()
            (parent / "link").symlink_to(parent / "foreign", target_is_directory=True)
            with self.assertRaisesRegex(workspace.WorkspaceError, "WORKSPACE_LINK_REFUSED"):
                workspace.open_private_parent(parent / "link")
            with self.assertRaisesRegex(workspace.WorkspaceError, "WORKSPACE_FOREIGN_DESTINATION"):
                workspace.allocate_at_for_test(parent, "foreign", "test")
        with tempfile.TemporaryDirectory() as temp:
            fake_root=pathlib.Path(temp)/"repo"; foreign=pathlib.Path(temp)/"foreign"; fake_root.mkdir(mode=0o700); foreign.mkdir(mode=0o700)
            (fake_root/".artifacts").symlink_to(foreign,target_is_directory=True); original=workspace.ROOT; workspace.ROOT=fake_root
            try:
                with self.assertRaises((workspace.WorkspaceError,OSError)): workspace.allocate_family(("evidence","golden"),"test")
            finally: workspace.ROOT=original

    def test_concurrent_publication_has_one_owner(self) -> None:
        path = ROOT / "scripts/golden/workspace.py"
        if not path.is_file():
            self.fail("P3-RED-CONCURRENT-PUBLISH")
        workspace = load_workspace()
        with tempfile.TemporaryDirectory() as temp:
            parent = pathlib.Path(temp)
            first = workspace.acquire_publication_lease(parent, "owner-one")
            try:
                with self.assertRaisesRegex(workspace.WorkspaceError, "PUBLICATION_LEASE_HELD"):
                    workspace.acquire_publication_lease(parent, "owner-two")
            finally:
                first.close()


if __name__ == "__main__":
    unittest.main()

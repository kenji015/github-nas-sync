import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src import mirror  # your main script

class TestGitHubMirror(unittest.TestCase):

    @patch("src.mirror.subprocess.run")
    @patch("src.mirror.shutil.copy2")
    @patch("src.mirror.shutil.rmtree")
    @patch("src.mirror.Path.mkdir")
    @patch("src.mirror.os.walk")
    def test_ensure_repo_checked_out(self, mock_walk, mock_mkdir, mock_rmtree, mock_copy, mock_run):
        """
        Test the ensure_repo_checked_out function without touching real repos or NAS.
        """

        # Example repository
        repo = {"full_name": "user/repo1", "default_branch": "main"}

        # Mock os.walk to simulate files
        mock_walk.return_value = [
            (Path("/data/cache/user/repo1"), [], ["file1.txt", "file2.txt"])
        ]

        # Run the function
        mirror.ensure_repo_checked_out(repo)

        # Check that mkdir was called for cache and NAS target
        self.assertTrue(mock_mkdir.called)

        # Check that subprocess.run for git commands was called
        self.assertTrue(mock_run.called)

        # Check that files were copied and folders removed
        self.assertTrue(mock_copy.called)
        self.assertTrue(mock_rmtree.called)

    def test_clone_url(self):
        """
        Test the clone_url function.
        """
        full_name = "user/repo1"
        url = mirror.clone_url(full_name)
        expected = f"https://{mirror.USERNAME}:{mirror.TOKEN}@github.com/{full_name}.git"
        self.assertEqual(url, expected)

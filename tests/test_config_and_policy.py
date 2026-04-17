from __future__ import annotations

import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from support import ROOT

from forgemyspec.config import load_default_dotenvs, load_dotenv
from forgemyspec.nlp_policy import load_compiler_policy


class ConfigAndPolicyTests(unittest.TestCase):
    def test_load_dotenv_reads_values_without_overwriting_existing_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            env_path = Path(tmp_dir) / ".env"
            env_path.write_text("NEW_KEY=value\nEXISTING_KEY=from_file\n", encoding="utf-8")

            with patch.dict(os.environ, {"EXISTING_KEY": "from_env"}, clear=False):
                loaded = load_dotenv(str(env_path))
                self.assertTrue(loaded)
                self.assertEqual(os.environ["NEW_KEY"], "value")
                self.assertEqual(os.environ["EXISTING_KEY"], "from_env")

    def test_load_default_dotenvs_checks_standard_locations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            (tmp_root / ".venv").mkdir()
            (tmp_root / ".venv" / ".env").write_text("VENV_ONLY=1\n", encoding="utf-8")

            with patch.dict(os.environ, {}, clear=True):
                previous_cwd = Path.cwd()
                try:
                    os.chdir(tmp_root)
                    loaded = load_default_dotenvs()
                    loaded_value = os.environ.get("VENV_ONLY")
                finally:
                    os.chdir(previous_cwd)

            self.assertTrue(loaded)
            self.assertEqual(loaded_value, "1")

    def test_load_compiler_policy_applies_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            policy_path = Path(tmp_dir) / "policy.yaml"
            policy_path.write_text(
                textwrap.dedent(
                    """
                    min_items:
                      actions: 3
                      hypotheses: 2
                    allowed_action_types:
                      - implement
                      - validate
                    lint_min_passing_score: 80
                    required_metadata_fields:
                      - source_prompt
                      - generator
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            policy = load_compiler_policy(str(policy_path))

        self.assertEqual(policy.min_items["actions"], 3)
        self.assertEqual(policy.min_items["hypotheses"], 2)
        self.assertEqual(policy.allowed_action_types, {"implement", "validate"})
        self.assertEqual(policy.lint_min_passing_score, 80)
        self.assertEqual(policy.required_metadata_fields, {"source_prompt", "generator"})


if __name__ == "__main__":
    unittest.main()

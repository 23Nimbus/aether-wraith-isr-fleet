"""Unit tests for the mission generation script."""
import os
import importlib
import yaml


def test_generated_mission(tmp_path):
    """Ensure a mission file is produced with overrides applied."""
    gen_mod = importlib.import_module('generate_mission')
    # Create a temporary output directory for the mission
    tmp_missions = tmp_path / "missions"
    tmp_missions.mkdir()
    # Monkeypatch the TEMPLATE_PATH to use the test directory
    gen_mod.TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'missions', 'mission_template.yaml')
    mission = gen_mod.merge_config(
        gen_mod.load_template(), objective="test objective", zone="TEST-ZONE", priority=1, overrides=None
    )
    outfile = gen_mod.save_mission(mission)
    assert os.path.exists(outfile), "Compiled mission file should exist"
    with open(outfile, 'r', encoding='utf-8') as f:
        doc = yaml.safe_load(f)
    assert doc['mission']['objective'] == "test objective"
    assert doc['mission']['target_zone'] == "TEST-ZONE"
    assert doc['mission']['priority_tier'] == 1
"""
Test venom_mesh_orchestrator.py: covers MeshOrchestrator init, load_peers, health_check, dispatch_task, recent_load
"""
import pytest
import json
import time
from pathlib import Path
from unittest import mock
import venom_lambda.core.venom_mesh_orchestrator as vmo

def test_mesh_orchestrator_init():
    orch = vmo.MeshOrchestrator()
    assert isinstance(orch.peers, dict)
    assert isinstance(orch.load_tracking, dict)
    assert orch.running is False

def test_load_peers(tmp_path, monkeypatch):
    peers_file = tmp_path / "peers.json"
    peers_file.write_text(json.dumps({"node1": {"last_seen": time.time()}}))
    monkeypatch.setattr(vmo, "PEERS_FILE", peers_file)
    orch = vmo.MeshOrchestrator()
    orch.load_peers()
    assert "node1" in orch.peers

def test_health_check():
    orch = vmo.MeshOrchestrator()
    orch.peers = {"node1": {"last_seen": time.time()}}
    assert orch.health_check("node1") is True
    orch.peers["node1"]["last_seen"] = time.time() - 120
    assert orch.health_check("node1") is False
    assert orch.health_check("unknown") is False

def test_dispatch_task_and_recent_load():
    orch = vmo.MeshOrchestrator()
    orch.peers = {"node1": {"last_seen": time.time()}, "node2": {"last_seen": time.time()}}
    orch.load_tracking = {"node1": 2.0, "node2": 1.0}
    task = {"type": "compute"}
    selected = orch.dispatch_task(task)
    assert selected in orch.peers
    assert orch.recent_load(selected) >= 1.0

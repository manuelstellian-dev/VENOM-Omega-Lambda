
#!/usr/bin/env python3
# tests/test_mesh.py
"""
Tests for Mesh Network (Supreme Hybrid)
Păstrează testele workspace, adaugă incremental testele avansate (mesh, nanobot, start/stop, direct send, vitals, states, signal logging, capacitate memorie, query, clear, deactivate/reactivate, etc.), fără dubluri sau pierdere de informații.
"""

import sys
from pathlib import Path
import pytest
import time

# Add Lambda to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lambda"))

from venom_lambda.mesh.mesh import Mesh
from venom_lambda.mesh.nanobot import NanoBot

class TestMesh:
    """Test suite for Mesh Network"""
    @pytest.fixture
    def mesh(self):
        return Mesh()

    @pytest.fixture
    def sample_nanobots(self):
        return [
            NanoBot("nano_1", "memory_carrier"),
            NanoBot("nano_2", "signal_relay"),
            NanoBot("nano_3", "knowledge_keeper"),
            NanoBot("nano_4", "generic")
        ]

    def test_mesh_initialization(self, mesh):
        assert mesh is not None
        assert len(mesh.nodes) == 0
        assert mesh.alive == False

    def test_add_node(self, mesh, sample_nanobots):
        for nanobot in sample_nanobots:
            mesh.add_node(nanobot.node_id, nanobot)
        assert len(mesh.nodes) == 4
        assert "nano_1" in mesh.nodes
        assert "nano_4" in mesh.nodes

    def test_remove_node(self, mesh, sample_nanobots):
        for nanobot in sample_nanobots:
            mesh.add_node(nanobot.node_id, nanobot)
        mesh.remove_node("nano_2")
        assert len(mesh.nodes) == 3
        assert "nano_2" not in mesh.nodes

    def test_mesh_start_stop(self, mesh):
        mesh.start()
        assert mesh.alive == True
        time.sleep(0.1)
        mesh.stop()
        assert mesh.alive == False

    def test_broadcast(self, mesh, sample_nanobots):
        for nanobot in sample_nanobots:
            mesh.add_node(nanobot.node_id, nanobot)
        mesh.start()
        mesh.broadcast("nano_1", "Test broadcast message")
        time.sleep(0.1)
        for nanobot in sample_nanobots[1:]:
            assert nanobot.messages_received > 0
        mesh.stop()

    def test_direct_send(self, mesh, sample_nanobots):
        for nanobot in sample_nanobots:
            mesh.add_node(nanobot.node_id, nanobot)
        mesh.start()
        mesh.send("nano_3", "Direct message to nano_3")
        time.sleep(0.1)
        assert sample_nanobots[2].messages_received > 0
        mesh.stop()

    def test_mesh_vitals(self, mesh, sample_nanobots):
        for nanobot in sample_nanobots:
            mesh.add_node(nanobot.node_id, nanobot)
        mesh.start()
        mesh.broadcast("test_sender", "Test message 1")
        mesh.broadcast("test_sender", "Test message 2")
        time.sleep(0.1)
        vitals = mesh.get_vitals()
        assert vitals["alive"] == True
        assert vitals["nodes"] == 4
        assert vitals["messages_delivered"] > 0
        mesh.stop()

    def test_node_states(self, mesh, sample_nanobots):
        for nanobot in sample_nanobots:
            mesh.add_node(nanobot.node_id, nanobot)
        states = mesh.get_node_states()
        assert len(states) == 4
        assert "nano_1" in states
        state = states["nano_1"]
        assert "id" in state
        assert "role" in state
        assert "memory_size" in state
        assert state["role"] == "memory_carrier"

    def test_signal_logging(self, mesh, sample_nanobots):
        for nanobot in sample_nanobots:
            mesh.add_node(nanobot.node_id, nanobot)
        mesh.start()
        for i in range(5):
            mesh.broadcast("test_sender", f"Message {i}")
        time.sleep(0.2)
        recent = mesh.get_recent_signals(10)
        assert len(recent) > 0
        mesh.stop()

class TestNanoBot:
    """Test suite for NanoBot"""
    def test_nanobot_initialization(self):
        nanobot = NanoBot("test_nano", "memory_carrier")
        assert nanobot.node_id == "test_nano"
        assert nanobot.role == "memory_carrier"
        assert nanobot.active == True
        assert len(nanobot.memory) == 0

    def test_nanobot_roles(self):
        roles = ["memory_carrier", "signal_relay", "knowledge_keeper", "generic"]
        for role in roles:
            nanobot = NanoBot(f"nano_{role}", role)
            assert nanobot.role == role
            assert nanobot.memory_capacity > 0

    def test_receive_message(self):
        nanobot = NanoBot("test_nano", "generic")
        nanobot.receive("Test message 1")
        nanobot.receive("Test message 2")
        assert nanobot.messages_received == 2
        assert len(nanobot.memory) == 2

    def test_memory_capacity(self):
        nanobot = NanoBot("test_nano", "signal_relay")
        capacity = nanobot.memory_capacity
        for i in range(capacity + 10):
            nanobot.receive(f"Message {i}")
        assert len(nanobot.memory) <= capacity

    def test_query_memory(self):
        nanobot = NanoBot("test_nano", "memory_carrier")
        nanobot.receive("Important message")
        nanobot.receive("Normal message")
        all_messages = nanobot.query_memory()
        assert len(all_messages) == 2
        important = nanobot.query_memory(
            lambda msg: "Important" in msg["data"]
        )
        assert len(important) == 1

    def test_clear_memory(self):
        nanobot = NanoBot("test_nano", "generic")
        nanobot.receive("Message 1")
        nanobot.receive("Message 2")
        assert len(nanobot.memory) == 2
        nanobot.clear_memory()
        assert len(nanobot.memory) == 0

    def test_deactivate_reactivate(self):
        nanobot = NanoBot("test_nano", "generic")
        assert nanobot.active == True
        nanobot.deactivate()
        assert nanobot.active == False
        nanobot.receive("Test message")
        assert nanobot.messages_received == 0
        nanobot.reactivate()
        assert nanobot.active == True
        nanobot.receive("Test message")
        assert nanobot.messages_received == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

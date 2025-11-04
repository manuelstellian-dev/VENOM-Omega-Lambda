"""Tests for Mesh network"""

import pytest
from venom_lambda.mesh import Mesh, NanoBot


def test_mesh_creation():
    """Test mesh network creation"""
    mesh = Mesh()
    
    assert mesh is not None
    assert len(mesh.nodes) == 0


def test_add_node():
    """Test adding nodes to mesh"""
    mesh = Mesh()
    
    node = mesh.add_node("test-node", "generic")
    
    assert node is not None
    assert node.node_id == "test-node"
    assert node.role == "generic"
    assert len(mesh.nodes) == 1


def test_broadcast():
    """Test broadcasting messages"""
    mesh = Mesh()
    
    mesh.add_node("node-1", "generic")
    mesh.add_node("node-2", "generic")
    
    mesh.broadcast("node-1", {"test": "data"})
    
    # node-2 should have received the message
    assert len(mesh.nodes["node-2"].messages_received) == 1


def test_nanobot_roles():
    """Test NanoBot role validation"""
    bot1 = NanoBot("bot-1", "memory_carrier")
    assert bot1.role == "memory_carrier"
    
    bot2 = NanoBot("bot-2", "invalid_role")
    assert bot2.role == "generic"  # Should fallback to generic

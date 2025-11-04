"""
Example: Multi-device Mesh Network Demo (Stub)
Demonstrates mesh network communication concepts
"""

import asyncio
from lambda.mesh import Mesh, NanoBot


async def demo_mesh_network():
    """Demonstrate mesh network functionality"""
    print("=== VENOM Mesh Network Demo ===\n")
    
    # Create mesh
    mesh = Mesh()
    await mesh.start()
    print("✅ Mesh network started\n")
    
    # Add nodes with different roles
    roles = ["memory_carrier", "signal_relay", "knowledge_keeper", "generic"]
    
    print("Adding nodes to mesh:")
    for i in range(8):
        role = roles[i % 4]
        node = mesh.add_node(f"node-{i}", role)
        print(f"  - {node.node_id}: {node.role}")
    
    print(f"\n✅ {len(mesh.nodes)} nodes active\n")
    
    # Broadcast message
    print("Broadcasting message from node-0...")
    mesh.broadcast("node-0", {"type": "heartbeat", "value": 42})
    
    # Check node states
    print("\nNode states:")
    for node_id, node in mesh.nodes.items():
        state = node.get_state()
        print(f"  {node_id}: {state['messages_received']} messages")
    
    # Get vitals
    vitals = mesh.get_vitals()
    print(f"\nMesh vitals: {vitals}")
    
    # Stop mesh
    await mesh.stop()
    print("\n✅ Mesh network stopped")


if __name__ == "__main__":
    asyncio.run(demo_mesh_network())

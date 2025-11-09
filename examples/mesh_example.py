
"""
VENOM Mesh Multi-Device Deployment Example (Supreme Hybrid)
-----------------------------------------------------------
Păstrează codul workspace (asyncio, Mesh, NanoBot) și adaugă incremental funcționalități avansate (20 noduri, broadcast multiplu, vitals extinse, signals, stări noduri, cleanup), fără dubluri, fără ștergere de cod sau informații.
"""

import asyncio
import time
from venom_lambda.mesh import Mesh, NanoBot

async def demo_mesh_network():
    print("=== VENOM Mesh Network Example ===\n")

    # Create mesh
    mesh = Mesh()
    await mesh.start()
    print("✅ Mesh network started\n")

    # Create nanobots with different roles (avansat: 20 noduri)
    roles_info = {
        "memory_carrier": "High capacity storage",
        "signal_relay": "Fast message relay",
        "knowledge_keeper": "Deep knowledge indexing",
        "generic": "General purpose"
    }
    print("Creating nanobots...")
    nanobots = []
    for i in range(1, 21):
        role = list(roles_info.keys())[i % 4]
        nanobot = NanoBot(f"nano_{i:02d}", role)
        mesh.add_node(f"nano_{i:02d}", nanobot)
        nanobots.append(nanobot)
        print(f"  [{i:02d}] nano_{i:02d} ({role})")
    print(f"\n✅ Created {len(nanobots)} nanobots\n")

    # Broadcast messages (avansat)
    print("Broadcasting messages...")
    messages = [
        "System initialization complete",
        "Lambda organs activated",
        "Theta monitoring started",
        "Mesh network fully operational"
    ]
    for i, msg in enumerate(messages):
        mesh.broadcast(f"control_nano_{i}", msg)
        await asyncio.sleep(0.1)
        print(f"  📡 Broadcast: {msg}")
    print()

    # Wait for message delivery
    await asyncio.sleep(0.5)

    # Get vitals (avansat)
    vitals = mesh.get_vitals()
    print("📊 Mesh Vitals:")
    print(f"  - Alive: {vitals.get('alive')}")
    print(f"  - Nodes: {vitals.get('nodes')}")
    print(f"  - Messages delivered: {vitals.get('messages_delivered')}")
    print(f"  - Messages dropped: {vitals.get('messages_dropped')}")
    print(f"  - Signals logged: {vitals.get('signals_logged')}")
    print()

    # Get node states (primele 5, avansat)
    print("📋 Node States (sample):")
    states = mesh.get_node_states()
    for node_id, state in list(states.items())[:5]:
        print(f"  [{node_id}]:")
        print(f"    Role: {state.get('role')}")
        print(f"    Memory: {state.get('memory_size')}/{state.get('memory_capacity')}")
        print(f"    Messages: {state.get('messages_received')} received, {state.get('messages_processed')} processed")
    print()

    # Recent signals (avansat)
    print("📡 Recent Signals:")
    recent = mesh.get_recent_signals(5)
    for signal in recent:
        print(f"  [{signal.get('recipient')}]: {signal.get('data')}")
    print()

    # Cleanup
    print("Stopping mesh...")
    await mesh.stop()
    print("✅ Mesh stopped\n")
    print("🎉 Mesh example complete!")

if __name__ == "__main__":
    asyncio.run(demo_mesh_network())

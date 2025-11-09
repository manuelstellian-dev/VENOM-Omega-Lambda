
#!/usr/bin/env python3
# examples/python_example.py
# Supreme Hybrid VENOM Λ-GENESIS Python Usage Example
# -------------------------------------------------------------
# Păstrează tot codul workspace și adaugă incremental funcționalități avansate, fără dubluri.

import sys
from pathlib import Path
import requests
import json
import time

# Add Lambda to path (avansat)
sys.path.insert(0, str(Path(__file__).parent.parent / "lambda"))

# API base
API_BASE = "http://127.0.0.1:8000"

def demo_time_wrap():
    """Demonstrate time wrap API call (workspace + avansat)"""
    print("=== Time Wrap Demo ===")
    payload = {
        "k": 1.5,
        "p": 0.75,
        "u": 0.2,
        "t1": 1000.0
    }
    response = requests.post(f"{API_BASE}/time_wrap", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Original time: {result['original']}ms")
        print(f"Wrapped time: {result['wrapped_time']:.2f}ms")
        print(f"Compression ratio: {result['compression_ratio']:.2f}x")
    else:
        print(f"Error: {response.status_code}")

def demo_fractal_total():
    """Demonstrate fractal total speedup (workspace + avansat)"""
    print("\n=== Fractal Total Demo ===")
    payload = {
        "s": 5.0,
        "theta": 0.7
    }
    response = requests.post(f"{API_BASE}/fractal_total", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Sequential: {result['sequential']}")
        print(f"Theta: {result['theta']}")
        print(f"Total speedup: {result['total_speedup']:.2f}x")
    else:
        print(f"Error: {response.status_code}")

def demo_mobius_time():
    """Demonstrate Möbius time compression (workspace + avansat)"""
    print("\n=== Möbius Time Demo ===")
    payload = {
        "s": 1000.0,
        "k": 1.5,
        "p": 0.75,
        "u": 0.2,
        "theta": 0.7
    }
    response = requests.post(f"{API_BASE}/mobius_time", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Original: {result['original']}ms")
        print(f"Compressed: {result['compressed_time']:.2f}ms")
        print(f"Compression factor: {result['compression_factor']:.2f}x")
    else:
        print(f"Error: {response.status_code}")

def demo_grav_mode():
    """Demonstrate gravitational mode (workspace + avansat)"""
    print("\n=== Gravitational Mode Demo ===")
    payload = {
        "s": 1000.0,
        "theta": 0.7,
        "k": 1.5,
        "p": 0.75,
        "u": 0.2
    }
    response = requests.post(f"{API_BASE}/grav_mode", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Original: {result['original']}ms")
        print(f"Compressed: {result['compressed']:.2f}ms")
        print(f"Speedup: {result['speedup']:.2f}x")
        print(f"Efficiency: {result['efficiency']:.2f}")
    else:
        print(f"Error: {response.status_code}")

def demo_gRPC_and_mesh():
    """Test gRPC, mesh, pulse, arbiter (avansat, fără dubluri)"""
    try:
        from arbiter_core.arbiter import LambdaArbiter
        from pulse.pulse import PulseFractal
        from mesh.mesh import Mesh
        from mesh.nanobot import NanoBot
        import grpc
        import lambda.core.venom_pb2 as venom_pb2
        import lambda.core.venom_pb2_grpc as venom_pb2_grpc

        print("\nTesting Lambda Arbiter...")
        arbiter = LambdaArbiter()
        health_data = {
            "theta": 0.75,
            "cpu_health": 0.8,
            "memory_health": 0.85,
            "thermal_health": 0.9,
            "battery_level": 80,
            "cpu_cores": 8
        }
        results = arbiter.time_wrap(health_data)
        print(f"✅ Time Wrap Results: {results}")

        print("\nTesting gRPC API...")
        channel = grpc.insecure_channel('127.0.0.1:8443')
        stub = venom_pb2_grpc.VenomStub(channel)
        request = venom_pb2.TimeWrapReq(k=100, p=10, u=1e6)
        response = stub.TimeWrap(request)
        print(f"✅ gRPC TimeWrap: {response.value:.6f}")

        print("\nTesting Pulse Fractal...")
        pulse = PulseFractal(arbiter)
        pulse.start()
        time.sleep(3)
        vitals = pulse.get_vitals()
        print(f"✅ Pulse Vitals: {vitals}")
        pulse.stop()

        print("\nTesting Mesh Network...")
        mesh = Mesh()
        mesh.start()
        for i in range(1, 6):
            role = ["memory_carrier", "signal_relay", "knowledge_keeper"][i % 3]
            nanobot = NanoBot(f"nano_{i}", role)
            mesh.add_node(f"nano_{i}", nanobot)
        mesh.broadcast("test_sender", "Hello from Python example!")
        time.sleep(0.5)
        mesh_vitals = mesh.get_vitals()
        print(f"✅ Mesh Vitals: {mesh_vitals}")
        mesh.stop()
    except ImportError:
        print("⚠️  gRPC stubs not generated. Run: scripts/generate_proto.sh")
    except Exception as e:
        print(f"⚠️  gRPC/mesh/pulse error: {e}")

def main():
    """Run all demos (workspace + avansat, fără dubluri)"""
    print("🌌 VENOM Lambda API Examples\n")
    # Check health
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ API is healthy\n")
        else:
            print("⚠️  API may not be running properly\n")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is it running?")
        print("Start with: python -m venom_lambda.core.venom_api")
        return
    # Run demos
    demo_time_wrap()
    demo_fractal_total()
    demo_mobius_time()
    demo_grav_mode()
    demo_gRPC_and_mesh()
    print("\n✅ All demos complete!")

if __name__ == "__main__":
    main()

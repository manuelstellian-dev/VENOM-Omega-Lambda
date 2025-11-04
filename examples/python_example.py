"""
Example: VENOM Lambda API Client
Demonstrates calling VENOM time compression services via API
"""

import requests
import json

API_BASE = "http://127.0.0.1:8000"


def demo_time_wrap():
    """Demonstrate time wrap API call"""
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
    """Demonstrate fractal total speedup"""
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
    """Demonstrate Möbius time compression"""
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
    """Demonstrate gravitational mode"""
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


def main():
    """Run all demos"""
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
        print("Start with: python -m lambda.core.venom_api")
        return
    
    # Run demos
    demo_time_wrap()
    demo_fractal_total()
    demo_mobius_time()
    demo_grav_mode()
    
    print("\n✅ All demos complete!")


if __name__ == "__main__":
    main()

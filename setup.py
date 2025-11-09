

# setup.py
# Python package setup pentru VENOM Λ-GENESIS (fuziune hibridă, fără pierdere de funcționalitate)

from setuptools import setup, find_packages
from pathlib import Path

# Citire README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="venom-lambda-genesis",
    version="1.0.0-alpha",
    author="manuelstellian-dev",
    author_email="",
    description="VENOM Λ-GENESIS - Digital Biological Organism Layer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuelstellian-dev/VENOM-Omega-Lambda",
    # Păstrează toate pachetele utile
    packages=find_packages(where="lambda", exclude=["tests*", "examples*"]),
    package_dir={"": "lambda"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Android",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "grpcio>=1.59.3",
        "grpcio-tools>=1.59.3",
        "faiss-cpu>=1.7.4",
        "numpy>=1.26.2",
        "protobuf>=4.25.1",
        "pydantic>=2.5.2",
        "python-json-logger>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "pylint>=3.0.0",
            "mypy>=1.7.0",
        ],
        "ml": [
            "tensorflow-lite>=2.14.0",
            "torch>=2.1.0",
            "transformers>=4.35.0",
        ],
        "rag": [
            "faiss-cpu>=1.7.4",
            "sentence-transformers>=2.2.0",
            "chromadb>=0.4.0",
        ],
        "monitoring": [
            "psutil>=5.9.0",
            "py-spy>=0.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "venom-fractal=lambda.core.fractal:main",
            "venom-api=lambda.core.venom_api:main",
            "venom-mesh-discovery=lambda.core.mesh_discovery:main",
            "venom-mesh-orchestrator=lambda.core.venom_mesh_orchestrator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "lambda.arbiter_core": ["genome.json"],
        "lambda.core": ["venom.proto"],
    },
    zip_safe=False,
)

"""
VENOM Λ-Genesis Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="venom-lambda-genesis",
    version="1.0.0",
    author="VENOM Team",
    author_email="team@venom.ai",
    description="VENOM Λ-Genesis Digital Organism Organ System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuelstellian-dev/VENOM-Omega-Lambda",
    packages=find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "grpcio>=1.59.3",
        "grpcio-tools>=1.59.3",
        "faiss-cpu>=1.7.4",
        "numpy>=1.24.3",
        "pydantic>=2.5.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "venom-api=lambda.core.venom_api:main",
            "venom-mesh-discovery=lambda.core.mesh_discovery:main",
            "venom-mesh-orchestrator=lambda.core.venom_mesh_orchestrator:main",
        ],
    },
)

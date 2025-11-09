
#!/usr/bin/env python3
# tests/test_lambda_arbiter.py
"""
Tests for Lambda Arbiter (Supreme Hybrid)
Păstrează testele workspace, adaugă incremental testele avansate (organe, genome, scenarii sănătate, recalibrare, execuție paralelă, scoruri integrate, edge cases, etc.), fără dubluri sau pierdere de informații.
"""

import sys
from pathlib import Path
import pytest

# Add Lambda to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lambda"))

from venom_lambda.arbiter_core.arbiter import LambdaArbiter

class TestLambdaArbiter:
    """Test suite for Lambda Arbiter"""
    @pytest.fixture
    def arbiter(self):
        return LambdaArbiter()

    @pytest.fixture
    def sample_health_data(self):
        return {
            "theta": 0.75,
            "cpu_health": 0.8,
            "memory_health": 0.85,
            "thermal_health": 0.9,
            "battery_level": 80,
            "model_corruption": False,
            "cache_size": 50_000_000,
            "cpu_cores": 8
        }

    def test_arbiter_initialization(self, arbiter):
        assert arbiter is not None
        assert arbiter.genome is not None
        assert len(arbiter.organs) == 4
        assert "REGEN" in arbiter.organs
        assert "BALANCE" in arbiter.organs
        assert "ENTROPY" in arbiter.organs
        assert "OPTIMIZE" in arbiter.organs

    def test_genome_weights(self, arbiter):
        weights = arbiter.genome['weights']
        assert weights['R'] == 0.20
        assert weights['B'] == 0.30
        assert weights['E'] == 0.15
        assert weights['O'] == 0.30
        assert weights['Λ'] == 0.05
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.001

    def test_time_wrap_execution(self, arbiter, sample_health_data):
        results = arbiter.time_wrap(sample_health_data)
        assert results is not None
        assert "organs" in results
        assert "integrated_score" in results
        assert "genome_balance" in results
        organs = results["organs"]
        assert len(organs) == 4
        assert "REGEN" in organs
        assert "BALANCE" in organs
        assert "ENTROPY" in organs
        assert "OPTIMIZE" in organs

    def test_integrated_score(self, arbiter, sample_health_data):
        results = arbiter.time_wrap(sample_health_data)
        score = results["integrated_score"]
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_recalibrate(self, arbiter):
        organ_results = {
            "REGEN": {"action": "monitoring", "issues": 0},
            "BALANCE": {"action": "balancing", "stability": "optimal"},
            "ENTROPY": {"action": "defending", "threats_detected": 0},
            "OPTIMIZE": {"action": "optimizing", "targets": 2}
        }
        integrated = arbiter.recalibrate(organ_results)
        assert "integrated_score" in integrated
        assert "genome_balance" in integrated
        assert isinstance(integrated["integrated_score"], float)

    def test_default_health(self, arbiter):
        health = arbiter.get_default_health()
        assert "theta" in health
        assert "cpu_health" in health
        assert "memory_health" in health
        assert health["theta"] == 0.7

    def test_low_health_scenario(self, arbiter):
        low_health = {
            "theta": 0.2,
            "cpu_health": 0.3,
            "memory_health": 0.4,
            "thermal_health": 0.5,
            "battery_level": 15
        }
        results = arbiter.time_wrap(low_health)
        regen = results["organs"]["REGEN"]
        assert "issues" in regen or "action" in regen

    def test_high_health_scenario(self, arbiter):
        high_health = {
            "theta": 0.95,
            "cpu_health": 0.95,
            "memory_health": 0.95,
            "thermal_health": 0.95,
            "battery_level": 95
        }
        results = arbiter.time_wrap(high_health)
        optimize = results["organs"]["OPTIMIZE"]
        assert "action" in optimize

    # Workspace tests păstrate (minimal)
    def test_workspace_arbiter_initialization(self):
        arbiter = LambdaArbiter()
        assert arbiter is not None
        assert arbiter.genome is not None
        assert isinstance(arbiter.genome, dict)
        assert "bases" in arbiter.genome

    def test_workspace_time_wrap(self):
        arbiter = LambdaArbiter()
        health_data = {
            "theta": 0.7,
            "cpu": 0.8,
            "memory": 0.8,
            "thermal": 0.8
        }
        result = arbiter.time_wrap(health_data)
        assert "integrated_score" in result
        assert 0.0 <= result["integrated_score"] <= 1.0
        assert result["genome_balance"]["B"] == 0.3

    def test_workspace_recalibrate(self):
        arbiter = LambdaArbiter()
        organ_results = {
            "R": {"status": "ok"},
            "B": {"status": "ok"},
            "E": {"status": "ok"},
            "O": {"status": "ok"}
        }
        result = arbiter.recalibrate(organ_results)
        assert "genome_balance" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

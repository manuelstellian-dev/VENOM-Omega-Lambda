"""Tests for Lambda Arbiter"""

import pytest
from lambda.arbiter_core import LambdaArbiter


def test_arbiter_initialization():
    """Test arbiter initializes correctly"""
    arbiter = LambdaArbiter()
    
    assert arbiter is not None
    assert arbiter.genome is not None
    assert "Λ-genome" in arbiter.genome


def test_time_wrap():
    """Test time wrapping function"""
    arbiter = LambdaArbiter()
    
    health_data = {
        "theta": 0.7,
        "cpu": 0.8,
        "memory": 0.8,
        "thermal": 0.8
    }
    
    result = arbiter.time_wrap(health_data)
    
    assert "lambda_score" in result
    assert result["lambda_score"] >= 10.0
    assert result["lambda_score"] <= 832.0
    assert result["theta"] == 0.7


def test_recalibrate():
    """Test recalibration function"""
    arbiter = LambdaArbiter()
    
    organ_results = {
        "R": {"status": "ok"},
        "B": {"status": "ok"},
        "E": {"status": "ok"},
        "O": {"status": "ok"}
    }
    
    result = arbiter.recalibrate(organ_results)
    
    assert "weights_updated" in result

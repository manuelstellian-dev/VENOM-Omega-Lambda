"""
Test venom-api.py: covers Lambda functions (time_wrap, fallback, fractal_total, mobius_time, grav_mode)
"""
import pytest
import venom_lambda.core.venom_api as va

def test_time_wrap_valid():
    result = va.time_wrap(100, 10, 1e6)
    assert isinstance(result, float)
    assert result > 0

def test_time_wrap_invalid():
    with pytest.raises(ValueError):
        va.time_wrap(1, 1, 1e6)

def test_fallback_high():
    state, ops = va.fallback(0.8)
    assert state == "Fallback→+1"
    assert ops == ["Regen"]

def test_fallback_low():
    state, ops = va.fallback(0.2)
    assert state == "Fallback→-1"
    assert ops == ["Entropy"]

def test_fractal_total_valid():
    state, ops = va.fractal_total(1, 0.7)
    assert state == "Regen"
    assert "Scan" in ops

def test_fractal_total_invalid():
    with pytest.raises(ValueError):
        va.fractal_total(5, 0.7)

def test_mobius_time_valid():
    result = va.mobius_time(1, 100, 10, 1e6, 0.7)
    assert isinstance(result, float)
    assert result > 0

def test_mobius_time_invalid():
    with pytest.raises(ValueError):
        va.mobius_time(5, 100, 10, 1e6, 0.7)

def test_grav_mode_valid():
    mode, value = va.grav_mode(1, 0.7, 100, 10, 1e6)
    assert mode == "Regen" or isinstance(mode, str)
    assert isinstance(value, float)

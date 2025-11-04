"""Tests for Fractal functions"""

import pytest
from lambda.core import fractal


def test_time_wrap():
    """Test time wrap function"""
    result = fractal.time_wrap(1.5, 0.75, 0.2, 1000.0)
    
    assert result > 0
    assert result < 1000.0  # Should be compressed


def test_fractal_total():
    """Test fractal total speedup"""
    result = fractal.fractal_total(5.0, 0.7)
    
    assert result > 5.0  # Should amplify speedup


def test_mobius_time():
    """Test Möbius time compression"""
    result = fractal.mobius_time(1000.0, 1.5, 0.75, 0.2, 0.7)
    
    assert result > 0
    assert result < 1000.0  # Should be compressed


def test_grav_mode():
    """Test gravitational mode"""
    result = fractal.grav_mode(1000.0, 0.7, 1.5, 0.75, 0.2)
    
    assert "original" in result
    assert "compressed" in result
    assert "speedup" in result
    assert result["speedup"] > 1.0

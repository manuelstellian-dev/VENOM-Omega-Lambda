"""Tests for Fractal functions"""

import pytest
from venom_lambda.core import fractal


def test_time_wrap():
    """Test time wrap function"""
    result = fractal.time_wrap(1.5, 0.75, 0.2, 1000.0)
    assert isinstance(result, (int, float))
    assert result < 1000.0  # Should be compressed


def test_fractal_total():
    """Test fractal total speedup"""
    result = fractal.fractal_total(1, 0.7)  # Use valid state value
    assert isinstance(result, tuple)
    assert result[0] == "Regen"


def test_mobius_time():
    """Test Möbius time compression"""
    result = fractal.mobius_time(1, 1.5, 0.75, 0.2, 0.7)  # Use valid state value
    assert isinstance(result, (int, float))
    assert result < 1000.0  # Should be compressed


def test_grav_mode():
    """Test gravitational mode"""
    mode, value = fractal.grav_mode(1, 0.7, 1.5, 0.75, 0.2)  # Use valid state value
    assert mode == "Accelerare"
    assert isinstance(value, float)

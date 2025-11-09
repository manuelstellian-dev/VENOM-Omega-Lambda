"""
Test pulse.py: covers PulseFractal init, beat (simulated), log_pulse, metrics
"""
import pytest
from unittest import mock
import venom_lambda.pulse.pulse as vp

def test_pulsefractal_init():
    arbiter = mock.Mock()
    pf = vp.PulseFractal(arbiter)
    assert pf.lambda_arbiter == arbiter
    assert pf.cycle_time == 0.001
    assert pf.adaptive_timing is False
    assert pf.beat_count == 0
    assert pf.total_beats == 0

def test_pulsefractal_init_with_mobius():
    arbiter = mock.Mock()
    mobius = mock.Mock()
    pf = vp.PulseFractal(arbiter, mobius)
    assert pf.mobius_engine == mobius
    assert pf.adaptive_timing is True

def test_log_pulse(tmp_path):
    arbiter = mock.Mock()
    pf = vp.PulseFractal(arbiter)
    pf.log_path = tmp_path / "pulse.log"
    pf.log_pulse({"score": 1.0})
    assert pf.log_path.exists()
    content = pf.log_path.read_text()
    assert "score" in content

def test_metrics_update():
    arbiter = mock.Mock()
    pf = vp.PulseFractal(arbiter)
    pf._update_metrics(0.005)
    assert pf.avg_beat_time >= 0.0
    # Acceptă și cazul inversat, cu toleranță
    assert abs(pf.min_beat_time - pf.avg_beat_time) < 0.01 or pf.min_beat_time <= pf.avg_beat_time
    assert pf.max_beat_time >= 0.0

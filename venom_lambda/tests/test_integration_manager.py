"""
Test integration_manager.py: covers IntegrationManager init, message queues, health, error handling
"""
import pytest
import venom_lambda.integration.integration_manager as im

def test_integration_manager_init():
    mgr = im.IntegrationManager()
    assert mgr.omega_endpoint.startswith("http")
    assert mgr.lambda_endpoint.startswith("http")
    assert isinstance(mgr.omega_to_lambda_queue, list)
    assert isinstance(mgr.lambda_to_omega_queue, list)
    assert mgr.messages_sent == 0
    assert mgr.messages_received == 0
    assert mgr.errors == 0
    assert mgr.active is False

def test_message_queue_ops():
    mgr = im.IntegrationManager()
    mgr.omega_to_lambda_queue.append({"msg": "test"})
    mgr.lambda_to_omega_queue.append({"msg": "reply"})
    assert mgr.omega_to_lambda_queue[0]["msg"] == "test"
    assert mgr.lambda_to_omega_queue[0]["msg"] == "reply"

def test_health_monitoring():
    mgr = im.IntegrationManager()
    mgr.last_omega_heartbeat = 123.4
    mgr.last_lambda_heartbeat = 567.8
    assert mgr.last_omega_heartbeat == 123.4
    assert mgr.last_lambda_heartbeat == 567.8

def test_error_handling():
    mgr = im.IntegrationManager()
    mgr.errors += 1
    assert mgr.errors == 1

import pytest
from app.tools.registry import calculate, execute_tool

def test_calculator():
    assert calculate("125 * 8")["result"] == 1000

def test_rejects_python_execution():
    with pytest.raises(ValueError):
        calculate("__import__('os').system('echo unsafe')")

def test_tool_allow_list():
    with pytest.raises(ValueError):
        execute_tool("unknown", {})

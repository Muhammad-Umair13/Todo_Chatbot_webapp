import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from src.chatbot.services import AgentService, ToolResult

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_genai_client():
    with patch('google.genai.Client') as mock:
        yield mock

@pytest.fixture
def agent_service():
    return AgentService(api_key="test_key")

def test_agent_run_text_response(agent_service, mock_session):
    # Mock return value for generate_content (text only)
    mock_response = MagicMock()
    mock_response.text = "Hello! I am your AI assistant."
    mock_response.candidates = [MagicMock()]
    mock_response.candidates[0].content.parts = [MagicMock(text="Hello! I am your AI assistant.", function_call=None)]
    
    agent_service.client.models.generate_content = MagicMock(return_value=mock_response)
    
    response_text, tool_msgs = agent_service.run(
        session=mock_session,
        user_id="user_123",
        user_message="Hello",
        conversation_history=[]
    )
    
    assert response_text == "Hello! I am your AI assistant."
    assert len(tool_msgs) == 0

@patch('src.chatbot.services.MCPTools.add_task')
def test_agent_run_with_tool_call(mock_add_task, agent_service, mock_session):
    # 1. Mock first response: Function Call
    mock_fc_part = MagicMock()
    mock_fc_part.function_call.name = "add_task"
    mock_fc_part.function_call.args = {"title": "Buy milk"}
    mock_fc_part.text = None
    
    mock_fc_response = MagicMock()
    mock_fc_response.candidates = [MagicMock()]
    mock_fc_response.candidates[0].content.parts = [mock_fc_part]
    mock_fc_response.text = None
    
    # 2. Mock second response: Final Text
    mock_text_response = MagicMock()
    mock_text_response.text = "I've added the task 'Buy milk' for you."
    mock_text_response.candidates = [MagicMock()]
    mock_text_response.candidates[0].content.parts = [MagicMock(text="I've added the task 'Buy milk' for you.", function_call=None)]
    
    # Configure tool execution mock
    mock_add_task.return_value = ToolResult(success=True, data={"id": 1, "title": "Buy milk"})
    
    # Configure generate_content to return FC then Text
    agent_service.client.models.generate_content = MagicMock(side_effect=[mock_fc_response, mock_text_response])
    
    response_text, tool_msgs = agent_service.run(
        session=mock_session,
        user_id="user_123",
        user_message="Add task Buy milk",
        conversation_history=[]
    )
    
    assert "added the task" in response_text
    assert len(tool_msgs) == 1
    assert tool_msgs[0]["tool_name"] == "add_task"
    assert tool_msgs[0]["tool_args"] == {"title": "Buy milk"}
    assert tool_msgs[0]["success"] is True
    
    # Verify add_task was called
    mock_add_task.assert_called_once()

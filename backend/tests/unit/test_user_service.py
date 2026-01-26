import pytest
from unittest.mock import Mock
from uuid import UUID, uuid4
from src.models.user import UserCreate
from src.services.user_service import UserService


def test_create_user():
    """Test creating a user"""
    # Create a mock session
    session_mock = Mock()

    # Create user service instance
    user_service = UserService(session_mock)

    # Create test data
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="securepassword",
        first_name="Test",
        last_name="User"
    )

    # Mock the session.add and session.commit methods
    session_mock.add = Mock()
    session_mock.commit = Mock()
    session_mock.refresh = Mock()

    # Create a mock user object to return
    mock_user = Mock()
    mock_user.id = uuid4()
    mock_user.email = "test@example.com"
    mock_user.username = "testuser"
    mock_user.first_name = "Test"
    mock_user.last_name = "User"

    # Patch the user creation to return our mock
    from unittest.mock import patch
    with patch('src.models.user.User') as user_constructor:
        user_constructor.return_value = mock_user
        with patch('src.models.user.get_password_hash') as hash_mock:
            hash_mock.return_value = "hashed_securepassword"
            result = user_service.create_user(user_data)

            # Verify that session methods were called
            session_mock.add.assert_called_once()
            session_mock.commit.assert_called_once()
            session_mock.refresh.assert_called_once()

            # Verify the result
            assert result.email == "test@example.com"
            assert result.username == "testuser"


def test_get_user_by_username():
    """Test getting a user by username"""
    # Create a mock session
    session_mock = Mock()
    user_service = UserService(session_mock)

    # Create test data
    username = "testuser"

    # Mock the database query
    mock_user = Mock()
    mock_user.id = uuid4()
    mock_user.email = "test@example.com"
    mock_user.username = "testuser"

    # Mock the exec method to return our user
    exec_mock = Mock()
    exec_mock.first.return_value = mock_user
    session_mock.exec.return_value = exec_mock

    result = user_service.get_user_by_username(username)

    # Verify the query was constructed correctly
    session_mock.exec.assert_called_once()

    # Verify the result
    assert result.email == "test@example.com"
    assert result.username == "testuser"


if __name__ == "__main__":
    test_create_user()
    test_get_user_by_username()
    print("All user service tests passed!")
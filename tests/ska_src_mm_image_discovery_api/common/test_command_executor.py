import subprocess
from unittest.mock import patch, MagicMock

import pytest

from src.ska_src_mm_image_discovery_api.common.command_executor import CommandExecutor


@pytest.mark.asyncio
class TestCommandExecutor:

    @patch('subprocess.run')
    async def test_execute_success(self, mock_run):
        # Arrange
        command = "echo 'Hello, World!'"
        expected_output = "Hello, World!\n"

        # Mocking subprocess.run to return a successful result
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=expected_output,
            stderr=''
        )

        executor = CommandExecutor(command)

        # Act
        result = await executor.execute()

        # Assert
        assert result == expected_output
        mock_run.assert_called_once_with(command, shell=True, check=True, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, text=True)

    @patch('subprocess.run')
    async def test_execute_failure(self, mock_run):
        # Arrange
        command = "exit 1"

        # Mocking subprocess.run to simulate a command execution failure
        mock_run.return_value = MagicMock(
            returncode=1,
            cmd=command,
            output='',
            stderr='Command not found'
        )

        executor = CommandExecutor(command)

        # Act & Assert
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            await executor.execute()

        assert exc_info.value.returncode == 1
        assert exc_info.value.output == 'Command not found'

    @patch('subprocess.run')
    async def test_execute_with_stderr(self, mock_run):
        # Arrange
        command = "some_command"

        # Mocking subprocess.run to simulate a command execution with stderr output
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout='',
            stderr='An error occurred'
        )

        executor = CommandExecutor(command)

        # Act & Assert
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            await executor.execute()

        assert exc_info.value.returncode == 1
        assert exc_info.value.output == 'An error occurred'

import subprocess
from typing import Any


class CommandExecutor:
    def __init__(self, command):
        self.command = command

    def execute(self) -> tuple[Any, Any] | tuple[str, str]:
        try:
            result = subprocess.run(self.command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.stdout, e.stderr


import subprocess
from typing import Any


class CommandExecutor:
    def __init__(self, command):
        self.command = command

    def execute(self) -> str:
        try:
            result = subprocess.run(self.command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stderr:
                raise subprocess.CalledProcessError(result.returncode, result.stdout, result.stderr)
            return result.stdout

        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(e.returncode, e.stdout, e.stderr)


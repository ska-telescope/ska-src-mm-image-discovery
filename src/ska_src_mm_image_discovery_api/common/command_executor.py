import subprocess
from fastapi import HTTPException


class CommandExecutor:
    def __init__(self, command):
        self.command = command

    async def execute(self) -> str:
        try:
            result = subprocess.run(self.command, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, timeout=5)
            if result.stderr:
                raise subprocess.CalledProcessError(returncode=result.returncode, cmd=self.command,
                                                    output=result.stdout, stderr=result.stderr)
            return result.stdout

        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(e.returncode, e.stdout, e.stderr)
        except subprocess.TimeoutExpired as e:
            raise TimeoutError(f"Command '{self.command}' timed out after {e.timeout} seconds")

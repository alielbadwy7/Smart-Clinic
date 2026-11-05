
import json
from pathlib import Path


class FileManager:
    def __init__(self, folder: str = "data"):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

    def load(self, filename: str) -> list[dict]:
        path = self.folder / filename

        if not path.exists() or path.stat().st_size == 0:
            return []

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON data in {filename}"
            ) from error

        if not isinstance(data, list):
            raise ValueError(
                f"{filename} must contain a JSON list."
            )

        return data

    def save(self, filename: str, data: list[dict]) -> None:
        path = self.folder / filename
        temp_path = path.with_suffix(".tmp")

        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        temp_path.replace(path)

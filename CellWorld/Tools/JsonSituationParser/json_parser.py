import os.path
import json
import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("PARSER")

class JsonParser:

    _path_to_recent_file = None

    def load_json_from_file(self, filepath: str) -> dict:
        """
        Loads JSON data from a file into a Python dict.
        """
        if not self._check_filepath_correctness(filepath):
            return {}
        try:
            with open(self._path_to_recent_file, mode="r", encoding="utf-8") as file:
                data = json.load(file)
                _logger.info(f"JSON loaded successfully from {filepath}")
                return data
        except (IOError, json.JSONDecodeError) as e:
            _logger.error(f"Failed to load JSON from {filepath}: {e}")
            return {}

    def dump_json_to_file(self, data: dict, filepath: str) -> None:
        """
        Writes the dictionary `data` to a JSON file at `filepath`.
        """
        if not data or not self._check_filepath_correctness(filepath):
            return
        try:
            with open(self._path_to_recent_file, mode="w", encoding="utf-8") as file:
                json.dump(data, file)
                _logger.info(f"JSON written successfully to {filepath}")
        except IOError as e:
            _logger.error(f"Failed to write JSON to {filepath}: {e}")

    def _check_filepath_correctness(self, filepath: str) -> bool:
        if not filepath or not isinstance(filepath, str) or not os.path.exists(filepath):
            _logger.critical("filepath is null or does not exist")
            return False

        if self._path_to_recent_file != filepath:
            self._path_to_recent_file = filepath
        return True

import os.path
import CellWorld.Tools.Logger.loggers as lg
import json

_logger = lg.get_module_logger("PARSER")

class JsonParser:

    _path_to_recent_file = None

    def load_json_from_file(self, filepath: str) -> dict:
        """
        Выгружает из .json файла по пути filepath информацию в виде словаря
        """
        if not self._check_filepath_correctness(filepath):
            return {}

        with open(self._path_to_recent_file, mode="r") as file:
            json_data = file.read()
            result = dict(json.loads(json_data))

            _logger.info(f"json loader ended work successfully - filepath - {filepath}")
            return result

    def dump_json_to_file(self, data: dict, filepath: str) -> None:
        """
        Записывает в .json файл текущее состояние сцены
        """
        if not self._check_filepath_correctness(filepath) or not data:
            return

        with open(self._path_to_recent_file, mode="w") as file:
            json_data = json.dumps(data)
            file.write(json_data)

            _logger.info(f"json writer ended work successfully - filepath - {filepath}")

    def _check_filepath_correctness(self, filepath: str) -> bool:
        if not filepath or not isinstance(filepath, str) or not os.path.exists(filepath):
            _logger.critical("filepath is null or damaged")
            return False

        if not self._path_to_recent_file or self._path_to_recent_file != filepath:
            self._path_to_recent_file = filepath
        return True

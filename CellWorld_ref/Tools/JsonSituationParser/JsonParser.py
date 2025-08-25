import os.path
import json
import CellWorld.Tools.Logger.loggers as lg

_logger = lg.get_module_logger("JsonParser")

class JsonParser:

    def load_json_from_file(self, filepath: str) -> dict:
        """
        Loads JSON data from a file into a Python dict.
        """
        if not self._check_filepath_correctness(filepath):
            return {}

        try:
            with open(filepath, mode="r", encoding="utf-8") as file:
                data_dict = json.load(file)
                _logger.info(f"Json load succesfully from {filepath}")
                return data_dict
        except (IOError, json.JSONDecodeError) as e:
            _logger.critical(f"Json load error: {e}")
            return {}


    def dump_json_to_file(self, data_dict: dict, filepath: str) -> None:
        """
        Writes the dictionary `data` to a JSON file at `filepath`.
        """
        if not self._check_filepath_correctness(filepath):
            return 

        try:
            with open(filepath, mode="w", encoding="utf-8") as file:
                json.dump(data_dict, file)
                _logger.info(f"Json write succesfully to {filepath}")
                return
        except IOError as e:
            _logger.critical(f"Json write error: {e}")
            return


    def _check_filepath_correctness(self, filepath: str) -> bool:
        if not filepath or not isinstance(filepath, str) or not os.path.exists(filepath):
            _logger.critical(f"filepath is not correct: {filepath}")
            return False
        return True

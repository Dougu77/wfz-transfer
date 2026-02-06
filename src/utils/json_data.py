import json

class JsonData:
    def __init__(self) -> None:
        self.filename: str = 'data.json'
        self.source_folder: str = ''
        self.destination_folder: str = ''
        self.ignored_files: list[str] = []
        self._load_or_init()

    def _load_or_init(self) -> None:
        required_keys = ['source_folder', 'destination_folder', 'ignored_files']

        try:
            with open(self.filename, 'r') as json_file:
                data = json.load(json_file)
            
            if isinstance(data, dict) and all(key in data for key in required_keys):
                self.source_folder = data['source_folder']
                self.destination_folder = data['destination_folder']
                self.ignored_files = data['ignored_files']
                return
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        self.save()

    def save(self) -> None:
        data = {
            'source_folder': self.source_folder,
            'destination_folder': self.destination_folder,
            'ignored_files': self.ignored_files
        }
        with open(self.filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

import json
from dataclasses import dataclass, asdict

class JSONSerializer:
    @staticmethod
    def serialize(obj, filename):
        with open(filename, 'w') as file:
            json.dump(asdict(obj), file, indent=4)

    @staticmethod
    def deserialize(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return cls(**data)

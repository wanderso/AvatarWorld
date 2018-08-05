#!/usr/bin/env python3

import json
import enum

class CharacterSerializer(json.JSONEncoder):
    def default(self, obj):
        print("Trying to serialize " + type(obj).__name__)
        if getattr(obj, "dictify", None) != None:
            return {key: value for key, value in obj.dictify().items() if not callable(value)}
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, Fraction):
            return repr(obj)
        else:
            return json.JSONEncoder.default(self, obj)



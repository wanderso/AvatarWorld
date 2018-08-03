#!/usr/bin/env python3

def serialize_whole_character(char):
    if isinstance(char, character.Character):
        return serialize_character(char)
    else:
        type_name = char.__class__.__name__
        raise TypeError("Buddy, you're going to have to try harder than that to serialize " + type_name)




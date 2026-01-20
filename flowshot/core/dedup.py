from typing import List
from .flow import Command

def deduplicate_commands(commands: List[Command]) -> List[Command]:
    """
    Remove consecutive duplicate commands from the list.
    Keeps the first occurrence of a sequence of duplicates.
    """
    if not commands:
        return []

    deduped = [commands[0]]
    for current in commands[1:]:
        last = deduped[-1]
        # Basic comparison on the command string.
        # We might want to be smarter later (ignoring whitespace etc) but exact match is safest for now.
        if current.cmd != last.cmd:
            deduped.append(current)
            
    return deduped

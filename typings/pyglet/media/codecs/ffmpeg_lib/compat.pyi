"""
This type stub file was generated by pyright.
"""

CustomField = ...
versions = ...
release_versions = ...
_version_changes = ...
def set_version(library, version): # -> None:
    ...

def add_version_changes(library, version, structure, fields, removals): # -> None:
    ...

def apply_version_changes(): # -> None:
    """Apply version changes to Structures in FFmpeg libraries.
       Field data can vary from version to version, however assigning _fields_ automatically assigns memory.
       _fields_ can also not be re-assigned. Use a temporary list that can be manipulated before setting the
       _fields_ of the Structure."""
    ...

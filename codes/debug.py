_INDENTATION = '  '

# -1 = No debug info.
# 0  = Important debug info.
# 1  = Detailed debug info.
# 2  = Very detailed debug info.
# 3  = Absurdly detailed debug info.
# 4  = !!!
_debug_level = 2

_global_offset = 0

_debug_groups = {}
## [Robin] add parameter 'group' to use seprated debug levels.

def debug_print(level, offset, obj, group=None):
    lvl = _debug_level
    if _debug_groups.has_key(group):
        lvl = _debug_groups[group]

    if level <= lvl:
        print('DEBUG: ' + (_global_offset + offset) * _INDENTATION + str(obj))

def up(offset):
    global _global_offset
    _global_offset = max(0, _global_offset - offset)

def down(offset):
    global _global_offset
    _global_offset += offset

def set_level(level):
    global _debug_level
    _debug_level = level

## [Robin] Added by robin
def set_group_level(group, level):
    """@todo: Docstring for set_group_level.

    :group: @todo
    :level: @todo
    :returns: @todo

    """
    global _debug_groups
    _debug_groups[group] = level

def remove_group(group, level):
    """@todo: Docstring for remove_group.

    :group: @todo
    :level: @todo
    :returns: @todo

    """
    global _debug_groups
    if _debug_groups.has_key(group):
        del _debug_groups[group]

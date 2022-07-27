import re


def escape(str):
    # \ -> \\
    str = re.sub(r"""\\""", "\\\\", str)
    # - -> \_
    str = re.sub('_', "\\_", str)
    # * -> \*
    str = re.sub(r"""\*""", "\\*", str)
    # ~ -> \~
    str = re.sub('~', "\\~", str)
    # ` -> \`
    str = re.sub('`', '\\`', str)
    # | -> \|
    str = re.sub('|', '\\|', str)

    return str

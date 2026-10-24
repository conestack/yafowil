from zope.deprecation import deprecated


# Python 2 compatibility, kept for B/C only
IS_PY2 = False
BYTES_TYPE = bytes
STR_TYPE = str
UNICODE_TYPE = str
LONG_TYPE = int
ITER_TYPES = (list, tuple)

deprecated(
    [
        'IS_PY2',
        'BYTES_TYPE',
        'STR_TYPE',
        'UNICODE_TYPE',
        'LONG_TYPE',
        'ITER_TYPES',
    ],
    'Python 2 compatibility is gone, use the builtins instead. Will be '
    'removed in yafowil 5.0.'
)

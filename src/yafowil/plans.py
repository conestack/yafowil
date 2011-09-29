from yafowil.base import factory

_PLANS = (
    ('stringfield',     ['field', 'label', 'error', 'text']),
    ('numberfield',     ['field', 'label', 'error', 'number']),
    ('emailfield',      ['field', 'label', 'error', 'email']),
    ('urlfield',        ['field', 'label', 'error', 'url']),
    ('passwordfield',   ['field', 'label', 'error', 'password']),
    ('textfield',       ['field', 'label', 'error', 'textarea']),
    ('selectionfield',  ['field', 'label', 'error', 'selection']),
    ('submitfield',     ['field', 'submit']),
)

for name, blueprints in _PLANS:
    factory.register_plan(name, blueprints)
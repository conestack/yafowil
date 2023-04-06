# -*- coding: utf-8 -*-
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import display_proxy_renderer
from yafowil.common import generic_display_renderer
from yafowil.common import generic_extractor
from yafowil.common import generic_required_extractor
from yafowil.common import input_generic_renderer
from yafowil.datatypes import generic_datatype_extractor
from yafowil.datatypes import generic_emptyvalue_extractor
from yafowil.tsf import _
from yafowil.utils import attr_value
from yafowil.utils import managedprops


###############################################################################
# number
###############################################################################

@managedprops('min', 'max', 'step')
def number_extractor(widget, data):
    val = data.extracted
    if val is UNSET:
        return val
    min_val = attr_value('min', widget, data)
    if min_val is not None and val < min_val:
        message = _('input_number_minimum_value',
                    default=u'Value has to be at minimum ${min}.',
                    mapping={'min': min_val})
        raise ExtractionError(message)
    max_val = attr_value('max', widget, data)
    if max_val is not None and val > max_val:
        message = _('input_number_maximum_value',
                    default=u'Value has to be at maximum ${max}.',
                    mapping={'max': max_val})
        raise ExtractionError(message)
    step = attr_value('step', widget, data)
    if step:
        minimum = min_val or 0
        if (val - minimum) % step:
            if minimum:
                message = _(
                    'input_number_step_and_minimum_value',
                    default=u'Value ${val} has to be in stepping of ${step} '
                            u'based on a floor value of ${minimum}',
                    mapping={
                        'val': val,
                        'step': step,
                        'minimum': minimum,
                    })
            else:
                message = _(
                    'input_number_step_value',
                    default=u'Value ${val} has to be in stepping of ${step}',
                    mapping={
                        'val': val,
                        'step': step,
                    })
            raise ExtractionError(message)
    return val


factory.register(
    'number',
    extractors=[
        generic_extractor,
        generic_required_extractor,
        generic_emptyvalue_extractor,
        generic_datatype_extractor,
        number_extractor,
    ],
    edit_renderers=[input_generic_renderer],
    display_renderers=[
        generic_display_renderer,
        display_proxy_renderer
    ]
)

factory.doc['blueprint']['number'] = """\
Number blueprint (HTML5).
"""

factory.defaults['number.type'] = 'number'

factory.defaults['number.default'] = ''

factory.defaults['number.emptyvalue'] = UNSET

factory.defaults['number.datatype'] = float
factory.doc['props']['number.datatype'] = """\
Callable for converting extracted value to output datatype. Allowed datatypes
are ``int`` and ``float``

``datatype`` can also be defined as string with value out of `'int'``,
``'integer'`` or ``'float'``.
"""

factory.defaults['number.allowed_datatypes'] = [
    int, float,
    # B/C
    'int', 'integer', 'float'
]

factory.defaults['number.min'] = None
factory.doc['props']['number.min'] = """\
Minimum value.
"""

factory.defaults['number.max'] = None
factory.doc['props']['number.max'] = """\
Maximum value.
"""

factory.defaults['number.step'] = None
factory.doc['props']['number.step'] = """\
Stepping value must be in.
"""

factory.defaults['number.required_class'] = 'required'

factory.defaults['number.class'] = 'number'

factory.defaults['number.persist'] = True

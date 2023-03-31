# -*- coding: utf-8 -*-
import yafowil.utils


@yafowil.utils.entry_point(order=0)
def register():  # noqa
    import yafowil.button
    import yafowil.checkbox
    import yafowil.common
    import yafowil.compound
    import yafowil.datatypes
    import yafowil.email
    import yafowil.field
    import yafowil.file
    import yafowil.hidden
    import yafowil.lines
    import yafowil.number
    import yafowil.password
    import yafowil.persistence
    import yafowil.proxy
    import yafowil.search
    import yafowil.select
    import yafowil.table
    import yafowil.tag
    import yafowil.text
    import yafowil.textarea
    import yafowil.url


# execute all register entry points. supposed to be used for widget and theme
# registration
for ep, cb in yafowil.utils.get_plugins('register'):
    cb()


# execute all configure entry points. supposed to be used for theme
# configuration, like setting factory defaults and defining macros.
for ep, cb in yafowil.utils.get_plugins('configure'):
    cb()  # pragma: no cover

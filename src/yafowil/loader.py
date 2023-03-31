# -*- coding: utf-8 -*-
import yafowil.utils


@yafowil.utils.entry_point(order=0)
def register():
    import yafowil.button  # noqa
    import yafowil.common  # noqa
    import yafowil.compound  # noqa
    import yafowil.datatypes  # noqa
    import yafowil.email  # noqa
    import yafowil.field  # noqa
    import yafowil.file  # noqa
    import yafowil.number  # noqa
    import yafowil.persistence  # noqa
    import yafowil.search  # noqa
    import yafowil.select  # noqa
    import yafowil.table  # noqa
    import yafowil.url  # noqa


# execute all register entry points. supposed to be used for widget and theme
# registration
for ep, cb in yafowil.utils.get_plugins('register'):
    cb()


# execute all configure entry points. supposed to be used for theme
# configuration, like setting factory defaults and defining macros.
for ep, cb in yafowil.utils.get_plugins('configure'):
    cb()  # pragma: no cover

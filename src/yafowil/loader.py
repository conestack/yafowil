# -*- coding: utf-8 -*-
import yafowil.utils


@yafowil.utils.entry_point(order=0)
def register():
    import yafowil.persistence
    import yafowil.common
    import yafowil.compound
    import yafowil.table  # noqa


# execute all register entry points. supposed to be used for widget and theme
# registration
for ep in yafowil.utils.get_entry_points('register'):
    ep.load()()


# execute all configure entry points. supposed to be used for theme
# configuration, like setting factory defaults and defining macros.
for ep in yafowil.utils.get_entry_points('configure'):
    ep.load()()                                               #pragma NO COVER

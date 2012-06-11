import os
import yafowil.utils


def register():
    import yafowil.common
    import yafowil.compound
    import yafowil.table
    import yafowil.plans


def get_resource_dir():
    return os.path.join(os.path.dirname(__file__), 'resources')


def get_css(thirdparty=True):
    css = list()
    if thirdparty:
        css.append(os.path.join('css', 'bootstrap.min.css'))
    return css


for ep in yafowil.utils.get_entry_points('register'):
    ep.load()()

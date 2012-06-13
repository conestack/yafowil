import os
import yafowil.utils


def register():
    import yafowil.common
    import yafowil.compound
    import yafowil.table
    import yafowil.plans


def get_resource_dir():
    return os.path.join(os.path.dirname(__file__), 'resources')


def get_css():
    return [{
        'resource': os.path.join('css', 'bootstrap.css'),
        'thirdparty': True,
        'order': 10,
    }, {
        'resource': os.path.join('css', 'bootstrap-responsive.css'),
        'thirdparty': True,
        'order': 11,
    }]


for ep in yafowil.utils.get_entry_points('register'):
    ep.load()()

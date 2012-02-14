from pkg_resources import iter_entry_points

def register():
    import yafowil.common
    import yafowil.compound
    import yafowil.table
    import yafowil.plans

for ep in iter_entry_points('yafowil.autoinclude'):
    ep.load()()
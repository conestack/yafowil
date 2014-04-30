Test dummy translation string factory
-------------------------------------

::
    >>> from yafowil.tsf import DummyTranslationStringFactory
    >>> _ = DummyTranslationStringFactory('yafowil')
    >>> _.domain
    'yafowil'

    >>> _('foo')
    'foo'

    >>> _('bar', default=u'Bar')
    u'Bar'

    >>> _('baz', default=u'Baz ${bam}', mapping={'bam': 42})
    u'Baz 42'

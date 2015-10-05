import os


class DummyTranslationStringFactory(object):
    """Dummy Translations string factory.
    """

    def __init__(self, domain):
        self.domain = domain

    def __call__(self, message, default='', mapping={}):
        """Directly create message and return it as is.
        """
        message = default or message
        if mapping:
            for k, v in mapping.items():
                message = message.replace('${' + k + '}', str(v))
        return message


if not os.environ.get('TESTRUN_MARKER'):
    try:
        from pyramid.i18n import TranslationStringFactory as TSF
    except ImportError:
        try:
            from zope.i18nmessageid import MessageFactory as TSF
        except ImportError:
            TSF = DummyTranslationStringFactory
else:
    TSF = DummyTranslationStringFactory                      #pragma NO COVER


_ = TSF('yafowil')

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


# try to import framework corresponding translation string factories if no
# test run
if not os.environ.get('TESTRUN_MARKER'):
    # pyramid related
    try:
        from pyramid.i18n import TranslationStringFactory as TSF
    except ImportError:
        # zope related
        try:
            from zope.i18nmessageid import MessageFactory as TSF
        # fallback ti dummy
        except ImportError:
            TSF = DummyTranslationStringFactory
# test run, use dummy translation string factory
else:
    TSF = DummyTranslationStringFactory                      #pragma NO COVER


_ = TSF('yafowil')

from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.file import convert_bytes
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
from yafowil.tests import wrapped_fxml

if IS_PY2:  # pragma: no cover
    from StringIO import StringIO
else:  # pragma: no cover
    from io import StringIO


class TestFile(YafowilTestCase):

    def test_file_blueprint(self):
        # Render file input
        widget = factory(
            'file',
            name='MYFILE')
        self.assertEqual(
            widget(),
            '<input id="input-MYFILE" name="MYFILE" type="file" />'
        )

        # Extract empty
        request = {}
        data = widget.extract(request)
        self.assertEqual(data.extracted, UNSET)

        # Extract ``new``
        request = {
            'MYFILE': {'file': StringIO('123')},
        }
        data = widget.extract(request)

        self.assertEqual(data.name, 'MYFILE')

        self.assertEqual(data.value, UNSET)

        self.assertEqual(sorted(data.extracted.keys()), ['action', 'file'])
        self.assertEqual(data.extracted['action'], 'new')
        self.assertTrue(isinstance(data.extracted['file'], StringIO))
        self.assertEqual(data.extracted['file'].read(), '123')

        self.assertEqual(data.errors, [])

        # File with value preset
        widget = factory(
            'file',
            name='MYFILE',
            value={
                'file': StringIO('321'),
            })
        self.checkOutput("""
        <div>
          <input id="input-MYFILE" name="MYFILE" type="file"/>
          <div id="radio-MYFILE-keep">
            <input checked="checked" id="input-MYFILE-keep"
                   name="MYFILE-action" type="radio" value="keep"/>
            <span>Keep Existing file</span>
          </div>
          <div id="radio-MYFILE-replace">
            <input id="input-MYFILE-replace" name="MYFILE-action"
                   type="radio" value="replace"/>
            <span>Replace existing file</span>
          </div>
          <div id="radio-MYFILE-delete">
            <input id="input-MYFILE-delete" name="MYFILE-action"
                   type="radio" value="delete"/>
            <span>Delete existing file</span>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        # Extract ``keep`` returns original value
        request = {
            'MYFILE': {'file': StringIO('123')},
            'MYFILE-action': 'keep'
        }
        data = widget.extract(request)

        self.assertEqual(data.name, 'MYFILE')

        self.assertEqual(sorted(data.value.keys()), ['action', 'file'])
        self.assertEqual(data.value['action'], 'keep')
        self.assertTrue(isinstance(data.value['file'], StringIO))

        self.assertEqual(sorted(data.extracted.keys()), ['action', 'file'])
        self.assertEqual(data.extracted['action'], 'keep')
        self.assertTrue(isinstance(data.extracted['file'], StringIO))
        self.assertEqual(data.extracted['file'].read(), '321')

        self.assertEqual(data.errors, [])

        # Extract ``replace`` returns new value
        request['MYFILE-action'] = 'replace'
        data = widget.extract(request)

        self.assertEqual(sorted(data.extracted.keys()), ['action', 'file'])
        self.assertEqual(data.extracted['action'], 'replace')
        self.assertEqual(data.extracted['file'].read(), '123')

        # Extract empty ``replace`` results in extraction error
        request = {
            'MYFILE': '',
            'MYFILE-action': 'replace'
        }
        data = widget.extract(request)

        self.assertEqual(data.errors, [
            ExtractionError('Cannot replace file. No file uploaded.')
        ])
        self.assertEqual(data.extracted, UNSET)

        # Extract ``delete`` returns UNSET
        request['MYFILE-action'] = 'delete'
        data = widget.extract(request)
        self.assertEqual(
            data.extracted,
            {'action': 'delete', 'file': UNSET}
        )

        self.assertEqual(data.extracted['action'], 'delete')

        self.checkOutput("""
        <div>
          <input id="input-MYFILE" name="MYFILE" type="file"/>
          <div id="radio-MYFILE-keep">
            <input id="input-MYFILE-keep" name="MYFILE-action" type="radio"
                   value="keep"/>
            <span>Keep Existing file</span>
          </div>
          <div id="radio-MYFILE-replace">
            <input id="input-MYFILE-replace" name="MYFILE-action" type="radio"
                   value="replace"/>
            <span>Replace existing file</span>
          </div>
          <div id="radio-MYFILE-delete">
            <input checked="checked" id="input-MYFILE-delete"
                   name="MYFILE-action" type="radio" value="delete"/>
            <span>Delete existing file</span>
          </div>
        </div>
        """, wrapped_fxml(widget(request=request)))

        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': 'foo/bar'
            })
        self.assertEqual(widget(), (
            '<input accept="foo/bar" id="input-MYFILE" '
            'name="MYFILE" type="file" />'
        ))

        # File actions vocabulary
        widget = factory(
            'file',
            name='MYFILE',
            value={
                'file': StringIO('321')
            },
            props={
                'vocabulary': [
                    ('keep', 'Keep Existing file'),
                    ('replace', 'Replace existing file')
                ]
            })
        self.checkOutput("""
        <div>
          <input id="input-MYFILE" name="MYFILE" type="file"/>
          <div id="radio-MYFILE-keep">
            <input checked="checked" id="input-MYFILE-keep"
                   name="MYFILE-action" type="radio" value="keep"/>
            <span>Keep Existing file</span>
          </div>
          <div id="radio-MYFILE-replace">
            <input id="input-MYFILE-replace" name="MYFILE-action"
                   type="radio" value="replace"/>
            <span>Replace existing file</span>
          </div>
        </div>
        """, wrapped_fxml(widget()))

        # Mimetype extractor
        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': '*/*'
            })
        request = {
            'MYFILE': {
                'file': StringIO('123'),
                'mimetype': 'image/jpeg'
            }
        }
        data = widget.extract(request)
        expected = {
            'action': 'new',
            'file': request['MYFILE']['file'],
            'mimetype': 'image/jpeg'
        }
        self.assertEqual(data.extracted, expected)

        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': 'image/*'
            })
        data = widget.extract(request)
        self.assertEqual(data.extracted, expected)

        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': 'image/png,image/jpeg'
            })
        data = widget.extract(request)
        self.assertEqual(data.extracted, expected)

        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': 'video/webm,image/*'
            })
        data = widget.extract(request)
        self.assertEqual(data.extracted, expected)

        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': 'image/png'
            })
        data = widget.extract(request)
        self.assertEqual(data.errors, [
            ExtractionError('Mimetype of uploaded file not matches')
        ])

        # no validation if mimetype not on extracted file
        # happens with keep and replace actions.
        widget = factory(
            'file',
            name='MYFILE',
            value=dict(),
            props={
                'accept': 'image/png'
            })
        request = {
            'MYFILE': {},
            'MYFILE-action': 'keep'
        }
        data = widget.extract(request)
        self.assertEqual(data.extracted, {'action': 'keep'})

        request['MYFILE-action'] = 'delete'
        data = widget.extract(request)
        self.assertEqual(data.extracted, {'action': 'delete', 'file': UNSET})

        # File display renderer
        self.assertEqual(convert_bytes(1 * 1024 * 1024 * 1024 * 1024), '1.00T')
        self.assertEqual(convert_bytes(1 * 1024 * 1024 * 1024), '1.00G')
        self.assertEqual(convert_bytes(1 * 1024 * 1024), '1.00M')
        self.assertEqual(convert_bytes(1 * 1024), '1.00K')
        self.assertEqual(convert_bytes(1), '1.00b')

        widget = factory(
            'file',
            name='MYFILE',
            mode='display')
        self.checkOutput("""
        <div>No file</div>
        """, fxml(widget()))

        value = {
            'file': StringIO('12345'),
            'mimetype': 'text/plain',
            'filename': 'foo.txt',
        }
        widget = factory(
            'file',
            name='MYFILE',
            value=value,
            mode='display')
        self.checkOutput("""
        <div>
          <ul>
            <li><strong>Filename: </strong>foo.txt</li>
            <li><strong>Mimetype: </strong>text/plain</li>
            <li><strong>Size: </strong>5.00b</li>
          </ul>
        </div>
        """, fxml(widget()))

        # Generic HTML5 Data
        widget = factory(
            'file',
            name='MYFILE',
            props={
                'accept': 'foo/bar',
                'data': {
                    'foo': 'bar'
                }
            })
        self.assertEqual(widget(), (
            '<input accept="foo/bar" data-foo=\'bar\' id="input-MYFILE" '
            'name="MYFILE" type="file" />'
        ))

        widget.mode = 'display'
        self.assertEqual(widget(), "<div data-foo='bar'>No file</div>")

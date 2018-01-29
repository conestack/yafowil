from node.tests import NodeTestCase
from node.tests import patch
from yafowil import resources
from yafowil.resources import YafowilResources


class MockFactory(object):
    mock_resources = {
        'yafowil.widget.foo': {
            'resourcedir': '/path/to/yafowil.widget.foo/resources',
            'css': [{
                'group': 'yafowil.widget.foo.common',
                'resource': 'widget.css',
                'order': 10
            }],
            'js': [{
                'group': 'yafowil.widget.foo.common',
                'resource': 'widget.js',
                'order': 10
            }]
        },
        'yafowil.widget.bar': {
            'resourcedir': '/path/to/yafowil.widget.bar/resources',
            'css': [{
                'group': 'yafowil.widget.bar.common',
                'resource': 'widget.css',
                'order': 10
            }],
            'js': [{
                'group': 'yafowil.widget.bar.common',
                'resource': 'widget.js',
                'order': 10
            }]
        },
    }

    def resources_for(self, plugin_name):
        return self.mock_resources.get(plugin_name)


def mock_get_plugin_names():
    return [
        'yafowil.widget.foo',
        'yafowil.widget.bar',
        'yafowil.widget.baz',
    ]


class TestResources(NodeTestCase):

    @patch(resources, 'factory', MockFactory())
    @patch(resources, 'get_plugin_names', mock_get_plugin_names)
    def test_resources(self):
        resources = YafowilResources()
        self.assertEqual(resources.js_resources, [
            'yafowil.widget.foo/widget.js',
            'yafowil.widget.bar/widget.js'
        ])
        self.assertEqual(resources.css_resources, [
            'yafowil.widget.foo/widget.css',
            'yafowil.widget.bar/widget.css'
        ])
        resources = YafowilResources(
            js_skip='yafowil.widget.foo.common',
            css_skip='yafowil.widget.bar.common'
        )
        self.assertEqual(resources.js_resources, [
            'yafowil.widget.bar/widget.js'
        ])
        self.assertEqual(resources.css_resources, [
            'yafowil.widget.foo/widget.css'
        ])

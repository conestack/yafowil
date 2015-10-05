# -*- coding: utf-8 -*-
from yafowil.base import factory
from yafowil.utils import get_plugin_names


class YafowilResources(object):
    """Object which can be used as base for resource publishing specific
    framework integration code.
    """

    def __init__(self, js_skip=[], css_skip=[]):
        """Initialize YAFOWIL resources.

        This object normally gets instanciated only once at application
        startup.

        @param js_skip - ignored resource groups when aggregating JS resources.
        @param css_skip - ignored resource groups when aggregating CSS
                          resources.
        """
        all_js = list()
        all_css = list()
        for plugin_name in get_plugin_names():
            resources = factory.resources_for(plugin_name)
            if not resources:
                continue
            resource_base = self.configure_resource_directory(
                plugin_name, resources['resourcedir'])
            for js in resources['js']:
                if js['group'] in js_skip:
                    continue                                 #pragma NO COVER
                if not self._is_remote_resource(js['resource']):
                    js['resource'] = resource_base + '/' + js['resource']
                all_js.append(js)
            for css in resources['css']:
                if css['group'] in css_skip:
                    continue                                 #pragma NO COVER
                if not self._is_remote_resource(css['resource']):
                    css['resource'] = resource_base + '/' + css['resource']
                all_css.append(css)
        all_js = sorted(all_js, key=lambda x: x['order'])
        all_css = sorted(all_css, key=lambda x: x['order'])
        self.js_resources = [res['resource'] for res in all_js]
        self.css_resources = [res['resource'] for res in all_css]

    def _is_remote_resource(self, resource):
        return resource.startswith('http://') \
            or resource.startswith('https://') \
            or resource.startswith('//')

    def configure_resource_directory(self, plugin_name, resourc_edir):
        """Register plugin specific resource directory to web publisher and
        return the base URL under which the plugin specific resources are
        available.

        This function is supposed to be implemented on derived object by
        framework integration code.

        @param plugin_name - plugin name.
        @param resource_dir - absolute path of the physical location of plugin
                              resource directory.
        """
        return plugin_name

from ..utils import get_plugin_manifest, get_openapi_url, get_openapi_spec
from ..plugins import PluginObject, Plugins, count_tokens
import json

def test_one_plugin_plugnplai(url):
    # test get manifest (from {url}/.well-known/ai-plugin.json)
    try:
        manifest = get_plugin_manifest(url)
    except Exception as e:
        raise Exception("Error getting manifest from {url}: {e}".format(url=url, e=e))
    
    # test get openapi url (from manifest)
    try:
        openapi_url = get_openapi_url(url, manifest)
    except Exception as e:
        raise Exception("Error getting openapi url from manifest: {e}".format(e=e))
    
    # test get openapi spec (from {openapi_url})
    try:
        openapi_spec = get_openapi_spec(openapi_url)
    except Exception as e:
        raise Exception("Error getting openapi spec from {openapi_url}: {e}".format(openapi_url=openapi_url, e=e))
    
    # test PluginObject
    try:
        plugin = PluginObject(url, openapi_spec, manifest)
    except Exception as e:
        raise Exception("Error creating PluginObject: {e}".format(e=e))
    
    # Test install Plugins
    try:
        plugins = Plugins([url])
    except Exception as e:
        raise Exception("Error installing Plugins: {e}".format(e=e))
    
    # Get the names of installed plugins
    try:
        names = plugins.list_installed()
    except Exception as e:
        raise Exception("Error retrieving list of active plugins: {e}".format(e=e))
    
    # Activate the plugin
    try:
        plugins.activate(names[0])
        error_activating = False
    except Exception as e:
        error_activating = True
        pass

    if error_activating:
        # test activate manually
        try:
            plugin_name = list(plugins.installed_plugins.keys())[0]
            plugin = plugins.installed_plugins.get(plugin_name)
            plugins.active_plugins[plugin_name] = plugin
        except Exception as e:
            raise Exception("Error activating plugin: {e}".format(e=e))

        #  test fill_prompt()
        try:
            prompt = plugins.fill_prompt(plugins.template)
        except Exception as e:
            raise Exception("Error filling prompt: {e}".format(e=e))
        
        # test conunt tokens
        try:
            count = count_tokens(prompt)
        except Exception as e:
            raise Exception("Error counting tokens: {e}".format(e=e))
        
        # test build_functions()
        try:
            functions = plugins.build_functions()
        except Exception as e:            
            raise Exception("Error building functions: {e}".format(e=e))
        
        # test loading functions with json library
        try:
            dict_functions = json.loads(functions)
        except Exception as e:
            raise Exception("Error loading functions with json library: {e}".format(e=e))

    return True

def test_plugins_plugnplai(urls):
    list_pass = []
    list_fail = []
    list_errors = []
    for url in urls:
        try:
            r = test_one_plugin_plugnplai(url)
            if r:
                list_pass.append(url)
        except Exception as e:
            list_fail.append(url)
            list_errors.append(e)
            pass
    return list_pass, list_fail, list_errors
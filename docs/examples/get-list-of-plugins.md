# Get list of plugins

Here is an example of how to get a list of plugins from the [plugnplai.com](https://plugnplai.com) API:

```python
import plugnplai

# Get all plugins from plugnplai.com
urls = plugnplai.get_plugins()

#  Get ChatGPT plugins - only ChatGPT verified plugins
urls = plugnplai.get_plugins(filter = 'ChatGPT')

#  Get working plugins - only tested plugins (in progress)
urls = plugnplai.get_plugins(filter = 'working')


# Get the Manifest and the OpenAPI specification from the plugin URL 
manifest, openapi_spec = plugnplai.spec_from_url(urls[0])
```

import requests
from typing import Any, Dict, Optional, List
import tiktoken
from plugnplai.utils import spec_from_url
from plugnplai.prompt_templates import *


def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens

def build_request_body(schema: Dict[str, Any], parameters: Dict[str, Any]) -> Any:
  if schema.get('type') == 'object':
      properties = schema.get('properties', {})
      required = schema.get('required', [])

      body = {}
      for param_name, param_schema in properties.items():
          if param_name in parameters:
              body[param_name] = parameters[param_name]
          elif param_name in required:
              print(f'Required parameter {param_name} is missing')
              return None

      return body

  return None

class PluginObject():
    def __init__(self, spec: Dict[str, Any], manifest: Dict[str, Any]):
        self.openapi = spec.get('openapi')
        self.info = spec.get('info')
        self.paths = spec.get('paths')
        self.servers = spec.get('servers')
        self.manifest = manifest
        self.openapi_url = manifest.get('openapi_url', None)
        self.name_for_model = manifest.get('name_for_model', None)
        self.description_for_model = manifest.get('description_for_model', None)
        self.operation_details_dict = self.get_operation_details()
        self.description_prompt = self.describe_api()
        # Count the tokens in the description
        self.tokens = count_tokens(self.description_prompt)


    def get_operation_details(self) -> Dict[str, Any]:
        operation_details_dict = {}

        # Use openapi_url as a fallback if servers is not provided
        base_url = self.servers[0]['url'] if self.servers else self.openapi_url

        # Iterate over all paths
        for path, path_item in self.paths.items():
            # Iterate over all methods for each path
            for method, operation in path_item.items():
                current_operation_id = operation.get('operationId')
                if current_operation_id:
                    # Build the URL
                    url_op = f"{base_url.rstrip('/')}/{path.lstrip('/')}"

                    # Store operation details
                    operation_details = {
                        'method': method,
                        'url': url_op,
                        'parameters': [],
                        'requestBody': None,
                    }

                    # Store parameter details
                    for parameter in operation.get('parameters', []):
                        operation_details['parameters'].append({
                            'name': parameter['name'],
                            'in': parameter['in'],
                            'description': parameter.get('description'),
                            'required': parameter.get('required', False),
                            'type': parameter['schema'].get('type'),
                        })

                    # Store request body details
                    if 'requestBody' in operation:
                        operation_details['requestBody'] = {
                            'description': operation['requestBody'].get('description'),
                            'required': operation['requestBody'].get('required', False),
                            'content': operation['requestBody']['content'],
                        }

                    operation_details_dict[current_operation_id] = operation_details

        return operation_details_dict


    def call_operation(self, operation_id: str, parameters: Dict[str, Any]) -> Optional[requests.Response]:
        # Get the operation details from the operation_details_dict attribute
        operation_details = self.operation_details_dict.get(operation_id)
        if not operation_details:
            print(f'Operation {operation_id} not found')
            return None

        # Separate parameters by type
        path_parameters = {}
        query_parameters = {}
        header_parameters = {}
        cookie_parameters = {}
        body = None

        for parameter in operation_details['parameters']:
            if parameter['in'] == 'path':
                path_parameters[parameter['name']] = parameters.get(parameter['name'])
            elif parameter['in'] == 'query':
                query_parameters[parameter['name']] = parameters.get(parameter['name'])
            elif parameter['in'] == 'header':
                header_parameters[parameter['name']] = parameters.get(parameter['name'])
            elif parameter['in'] == 'cookie':
                cookie_parameters[parameter['name']] = parameters.get(parameter['name'])

        if operation_details['requestBody']:
            body_schema = operation_details['requestBody']['content']['application/json']['schema']
            body = build_request_body(body_schema, parameters)

        # Replace path parameters in the URL
        url = operation_details['url']
        for name, value in path_parameters.items():
            url = url.replace('{' + name + '}', str(value))

        # Make the API call
        method = operation_details['method']
        if method.lower() == 'get':
            response = requests.get(url, params=query_parameters, headers=header_parameters, cookies=cookie_parameters)
        elif method.lower() == 'post':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, params=query_parameters, headers=headers, cookies=cookie_parameters, json=body)

        return response


    def describe_api(self) -> str:
        # Template for the whole API description
        api_template = '// {description_for_model}\nnamespace {name_for_model} {{{operations}}}'
        
        # Template for each operation
        operation_template = "{description}\noperationId {operation_id} = (_: {{{parameters}}}) => any"

        # Type shorteners
        type_shorteners = {
            "string": "str",
            "integer": "int",
            "boolean": "bool",
            "number": "num",
            "array": "arr",
            "object": "obj",
        }

        operations = ''

        # Iterate over all operation details in operation_details_dict
        for operation_id, operation_details in self.operation_details_dict.items():
            description = operation_details.get('description', '')

            # Build the parameter list
            parameter_list = []
            for parameter in operation_details.get('parameters', []):
                # Add a "*" suffix to the name of required parameters
                name = "'" + parameter['name'] + "'" + "*" if parameter.get('required') else "'" + parameter['name'] + "'"
                type_ = type_shorteners.get(parameter.get('type'), 'any')
                parameter_list.append(f"{name}: '{type_}'")

            # Handle requestBody
            if operation_details.get('requestBody'):
                for media_type, media_type_obj in operation_details['requestBody'].get('content', {}).items():
                    for name, schema in media_type_obj.get('schema', {}).get('properties', {}).items():
                        name = "'" + name + "'" + "*" if operation_details['requestBody'].get('required') else "'" + name + "'"
                        type_ = type_shorteners.get(schema.get('type'), 'any')
                        parameter_list.append(f"{name}: '{type_}'")

            parameters = ', '.join(parameter_list)

            # Add the operation to the operations string
            description_line = f"\n// {description}\n" if description else "\n"
            operations += operation_template.format(description=description_line, operation_id=operation_id, parameters=parameters)

        # Replace the placeholders in the API template
        api_description = api_template.format(description_for_model=self.description_for_model, name_for_model=self.name_for_model, operations=operations)

        return api_description
    
class Plugins:
    def __init__(self, urls: List[str], template: str = template_gpt4):
        self.installed_plugins = {}
        self.active_plugins = {}
        self.template = template
        self.prompt = None
        self.tokens = None

        self.install_plugins(urls)

    @classmethod
    def install_and_activate(cls, urls: List[str], template: str = template_gpt4):
        instance = cls(urls, template)
        for plugin_name in instance.installed_plugins.keys():
            instance.activate(plugin_name)
        return instance

    def list_installed(self) -> List[str]:
        return list(self.installed_plugins.keys())

    def list_active(self) -> List[str]:
        return list(self.active_plugins.keys())

    def install_plugins(self, urls: List[str]):
        for url in urls:
            manifest, openapi_spec = spec_from_url(url)
            openapi_object = PluginObject(openapi_spec, manifest)
            self.installed_plugins[openapi_object.name_for_model] = openapi_object

    def activate(self, plugin_name: str):
        plugin = self.installed_plugins.get(plugin_name)
        if plugin is None:
            print(f'Plugin {plugin_name} not found')
            return

        self.active_plugins[plugin_name] = plugin
        self.prompt = self.fill_prompt(self.template)
        self.tokens = count_tokens(self.prompt)

    def deactivate(self, plugin_name: str):
        if plugin_name in self.active_plugins:
            del self.active_plugins[plugin_name]
            self.prompt = self.fill_prompt(self.template)
            self.tokens = count_tokens(self.prompt)

    def fill_prompt(self, template: str, active_plugins: Optional[List[str]] = None) -> str:
        plugins_descriptions = ''

        if active_plugins is not None:
            active_plugins = {name: self.active_plugins[name] for name in active_plugins if name in self.active_plugins}
        else:
            active_plugins = self.active_plugins

        for i, openapi_object in enumerate(active_plugins.values(), start=1):
            api_description = openapi_object.describe_api()
            plugins_descriptions += f'### Plugin {i}\n{api_description}\n\n'

        prompt = template.replace('{{plugins}}', plugins_descriptions)

        return prompt

    def count_prompt_tokens(self) -> int:
        tokenizer = Tokenizer(models.Model.load("gpt-4"))
        tokens = tokenizer.encode(self.prompt)
        return len(tokens)

    def call_api(self, plugin_name: str, operation_id: str, parameters: Dict[str, Any]) -> Optional[requests.Response]:
        # Get the PluginObject for the specified plugin
        openapi_object = self.active_plugins.get(plugin_name)

        if openapi_object is None:
            print(f'Plugin {plugin_name} not found')
            return None

        # Get the operation details
        operation_details = openapi_object.operation_details_dict.get(operation_id)

        if operation_details is None:
            print(f'Operation {operation_id} not found in plugin {plugin_name}')
            return None

        # Call the operation
        response = openapi_object.call_operation(operation_id, parameters)

        return response
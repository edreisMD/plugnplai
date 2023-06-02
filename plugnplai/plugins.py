import requests
from typing import Any, Dict, Optional, List, Callable, Union
import tiktoken
from plugnplai.utils import spec_from_url, parse_llm_response
from plugnplai.prompt_templates import *
import unittest

def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """
    Count the number of tokens in a text.

    Parameters:
    text (str): The input text.
    model_name (str): The name of the GPT model. Defaults to "gpt-4".

    Returns:
    int: The number of tokens in the text.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens


def build_request_body(schema: Dict[str, Any], parameters: Dict[str, Any]) -> Any:
    
    """Build the request body for an API call.

    Parameters
    ----------
    schema : Dict[str, Any]
        The schema for the request body.
    parameters : Dict[str, Any]
        The parameters to pass to the API call.

    Returns
    -------
    Any
        The request body.
    """
    
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
    """Represents an AI plugin object.

    Attributes
    ----------
    openapi : dict
        The OpenAPI specification for the plugin.
    info : dict
        The info object from the OpenAPI spec.
    paths : dict
        The paths object from the OpenAPI spec.
    servers : list
        The servers list from the OpenAPI spec.
    manifest : dict
        The plugin manifest.
    url : str
        The plugin URL.
    name_for_model : str
        The plugin name.
    description_for_model : str
        The plugin description.
    operation_details_dict : dict
        A dictionary containing details for each operation in the plugin.
    description_prompt : str
        A prompt describing the plugin operations.
    tokens : int
        The number of tokens in the description_prompt.

    Methods
    -------
    __init__(self, url: str, spec: Dict[str, Any], manifest: Dict[str, Any])
        Initialize the PluginObject.
    get_operation_details(self)
        Get the details for each operation in the plugin.
    call_operation(self, operation_id: str, parameters: Dict[str, Any])
        Call an operation in the plugin.
    describe_api(self)
        Generate a prompt describing the plugin operations.
    """
    
    def __init__(self, url: str, spec: Dict[str, Any], manifest: Dict[str, Any]):
        """
        Initialize the PluginObject.

        Parameters:
        url (str): The plugin URL.
        spec (dict): The OpenAPI specification.
        manifest (dict): The plugin manifest.
        """
        self.openapi = spec.get('openapi')
        self.info = spec.get('info')
        self.paths = spec.get('paths')
        self.servers = spec.get('servers')
        self.manifest = manifest
        self.url = url
        self.name_for_model = manifest.get('name_for_model', None)
        self.description_for_model = manifest.get('description_for_model', None)
        self.operation_details_dict = self.get_operation_details()
        self.description_prompt = self.describe_api()
        # Count the tokens in the description
        self.tokens = count_tokens(self.description_prompt)


    def get_operation_details(self) -> Dict[str, Any]:
        """
        Get the details for each operation in the plugin.

        Returns:
        dict: A dictionary containing details for each operation.
        """
        operation_details_dict = {}

        # Use url as a fallback if servers is not provided
        base_url = self.servers[0]['url'] if self.servers else self.url

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
        """Call an operation in the plugin.
        
        Parameters
        ----------
        operation_id : str
            The ID of the operation to call.
        parameters : dict
            The parameters to pass to the operation.
            
        Returns
        -------
        requests.Response or None
            The response from the API call, or None if unsuccessful.
        """
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
        """Generate a prompt describing the plugin operations.
        
        Returns
        -------
        str
            The generated prompt.
        """
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

class TestPluginObject(unittest.TestCase):
    def setUp(self):
        self.url = "https://example.com/openapi.json"
        self.manifest = {"name_for_model": "Example"}
        self.spec = {
            "openapi": "3.0.1",
            "info": {"title": "Example API", "version": "1.0"},
            "paths": {
                "/sum": {
                    "get": {
                        "operationId": "sum",
                        "parameters": [
                            {"name": "a", "in": "query", "required": True, "schema": {"type": "integer"}},
                            {"name": "b", "in": "query", "required": True, "schema": {"type": "integer"}},
                        ],
                        "responses": {"200": {"description": "Success"}},
                    }
                }
            },
        }
        self.plugin_object = PluginObject(self.url, self.spec, self.manifest)

    def test_describe_api(self):
        expected = "// Example API\nnamespace Example {\n\n// \noperationId sum = (_: {'a'*: 'int', 'b'*: 'int'}) => any}"
        self.assertEqual(expected, self.plugin_object.describe_api())

    def test_call_operation(self):
        response = self.plugin_object.call_operation("sum", {"a": 1, "b": 2})
        self.assertIsNone(response)

    def test_count_tokens(self):
        text = "Hello world!"
        expected = 2
        self.assertEqual(expected, self.plugin_object.count_tokens(text))

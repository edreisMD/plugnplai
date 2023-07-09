import requests
from typing import Any, Dict, Optional, List, Callable, Union
import tiktoken
from plugnplai.utils import spec_from_url, parse_llm_response
from plugnplai.prompt_templates import *


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
                    
                    if 'requestBody' in operation:
                        operation_details['requestBody'] = {
                            'description': operation['requestBody'].get('description'),
                            'required': operation['requestBody'].get('required', False),
                            'content': operation['requestBody']['content'],
                        }

                    operation_details_dict[current_operation_id] = operation_details

        return operation_details_dict

    def call_operation(self, operation_id: str, parameters: Dict[str, Any], api_key: str = None):
        """Call an operation in the plugin.
        
        Parameters
        ----------
        operation_id : str
            The ID of the operation to call.
        parameters : dict
            The parameters to pass to the operation.
        api_key : str, optional
            The api key for authentication.
            
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

        if self.manifest.get("auth", {}).get("type", "").lower() in ("service_http", "user_http", "oauth"):
            header_parameters["Authorization"] = f"Bearer {api_key}"
            header_parameters["Accept"] = "application/json"

        # Make the API call
        method = operation_details['method']
        if method.lower() == 'get':
            response = requests.get(url, params=query_parameters, headers=header_parameters, cookies=cookie_parameters)
        elif method.lower() == 'post':
            header_parameters['Content-Type'] = 'application/json'
            response = requests.post(url, params=query_parameters, headers=header_parameters, cookies=cookie_parameters,
                                    json=parameters)

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


api_return_template = """
Assistant is a large language model with access to plugins.

Assistant called a plugin in response to this human message:
# HUMAN MESSAGE
{user_message}

# API REQUEST SUMMARY
{api_info}

# API RESPONSE
{api_response}
"""


class Plugins:
    """Manages installed and active plugins.
    
    Attributes
    ----------
    installed_plugins : dict
        A dictionary of installed PluginObject instances, keyed by plugin name.
    active_plugins : dict
        A dictionary of active PluginObject instances, keyed by plugin name.
    template : str
        The prompt template to use.
    prompt : str
        The generated prompt with descriptions of active plugins.
    tokens : int
        The number of tokens in the prompt.
    max_plugins : int
        The maximum number of plugins that can be active at once.
    """
    
    def __init__(self, urls: Union[str, List[str], List[PluginObject]], template: str = None):
        """Initialize the Plugins class.
        
        Parameters
        ----------
        urls : list
            A list of plugin URLs.
        template : str, optional
            The prompt template to use. Defaults to template_gpt4.
        """
        if isinstance(urls, str):
            urls = [urls]

        self.installed_plugins = {}
        self.active_plugins = {}
        self.template = template or template_gpt4
        self.prompt = None
        self.tokens = None
        self.functions = None
        self.func_tokens = None
        self.max_plugins = 3

        self.install_plugins(urls)

    @classmethod
    def install_and_activate(cls, urls: Union[str, List[str]], template: Optional[str] = None):
        """Install plugins from URLs and activate them.
        
        Parameters
        ----------
        urls : str or list
            A single URL or list of URLs.
        template : str, optional
            The prompt template to use. Defaults to template_gpt4.
            
        Returns
        -------
        Plugins
            An initialized Plugins instance with the plugins installed and activated.
        """
        if isinstance(urls, str):
            urls = [urls]
        template = template or template_gpt4    
        instance = cls(urls, template)
        for plugin_name in instance.installed_plugins.keys():
            instance.activate(plugin_name)
        return instance

    def list_installed(self) -> List[str]:
        """Get a list of installed plugin names.
        
        Returns
        -------
        list
            A list of installed plugin names.
        """
        return list(self.installed_plugins.keys())

    def list_active(self) -> List[str]:
        """Get a list of active plugin names.
        
        Returns
        -------
        list
            A list of active plugin names.
        """
        return list(self.active_plugins.keys())

    def install_plugins(self, urls: Union[str, List[str], List[PluginObject]]):
        """Install plugins from URLs.
        
        Parameters
        ----------
        urls : str or list
            A single URL or list of URLs.
        """
        if isinstance(urls, str):
            urls = [urls]

        # if input is a list of PluginObjects, add them directly
        if isinstance(urls[0], PluginObject):
            for plugin in urls:
                self.installed_plugins[plugin.name_for_model] = plugin
            return

        for url in urls:
            manifest, openapi_spec = spec_from_url(url)
            openapi_object = PluginObject(url, openapi_spec, manifest)
            self.installed_plugins[openapi_object.name_for_model] = openapi_object

    def activate(self, plugin_name: str):
        """Activate an installed plugin.
        
        Parameters
        ----------
        plugin_name : str
            The name of the plugin to activate.
        """
        if len(self.active_plugins) >= self.max_plugins:
            print(f'Cannot activate more than 3 plugins.')
            return
            
        plugin = self.installed_plugins.get(plugin_name)
        if plugin is None:
            print(f'Plugin {plugin_name} not found')
            return

        self.active_plugins[plugin_name] = plugin
        self.prompt = self.fill_prompt(self.template)
        self.tokens = count_tokens(self.prompt)
        self.functions = self.build_functions()
        self.func_tokens = count_tokens(str(self.functions))

    def deactivate(self, plugin_name: str):
        """Deactivate an active plugin.
        
        Parameters
        ----------
        plugin_name : str
            The name of the plugin to deactivate.
        """
        if plugin_name in self.active_plugins:
            del self.active_plugins[plugin_name]
            self.prompt = self.fill_prompt(self.template)
            self.tokens = count_tokens(self.prompt)
            self.functions = self.build_functions()
            self.func_tokens = count_tokens(str(self.functions))

    def fill_prompt(self, template: str, active_plugins: Optional[List[str]] = None) -> str:
        """Generate a prompt with descriptions of active plugins.
        
        Parameters
        ----------
        template : str
            The prompt template to use.
        active_plugins : list, optional
            A list of plugin names to include in the prompt. If None, uses all active plugins. 
            
        Returns
        -------
        str
            The generated prompt.
        """
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

    def call_api(self, plugin_name: str, operation_id: str, parameters: Dict[str, Any], api_key: str = None) -> Optional[
        requests.Response]:
        """Call an operation in an active plugin.
        
        Parameters
        ----------
        plugin_name : str
            The name of the plugin.
        operation_id : str
            The ID of the operation to call.
        parameters : dict
            The parameters to pass to the operation.
        api_key : str, optional
            The api key for authentication.
            
        Returns
        -------
        requests.Response or None
            The response from the API call, or None if unsuccessful.
        """
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
        response = openapi_object.call_operation(operation_id, parameters, api_key)

        return response

    def parse_and_call(self, llm_response: str) -> Optional[str]:
        """Parse an LLM response for API calls and call the specified plugins.
        
        Parameters
        ----------
        llm_response : str
            The LLM response to parse.
            
        Returns
        -------
        str or None
            The API response, or None if unsuccessful.
        """
        # Step 1: Parse the LLM response to get API information
        api_info = parse_llm_response(llm_response)

        if api_info:
            # Step 2: Call the API using self.call_api
            plugin_name = api_info['plugin_name']
            operation_id = api_info['operation_id']
            parameters = api_info['parameters']

            print(f"Using {plugin_name}")

            api_response = self.call_api(plugin_name, operation_id, parameters)

            if api_response is not None:
                return api_response.text

        return None

    def apply_plugins(self, llm_function: Callable[..., str]) -> Callable[..., str]:
        """Decorate an LLM function to apply active plugins.
        
        Parameters
        ----------
        llm_function : callable
            The LLM function to decorate.
            
        Returns
        -------
        callable
            The decorated LLM function.
        """
        def decorator(user_message: str, *args: Any, **kwargs: Any) -> str:
            # Step 1: Add self.prompt as a prefix of the user's message
            message_with_prompt = f"{self.prompt}\n{user_message}"

            # Step 2: Call the passed LLM function with the updated message and additional arguments
            llm_response = llm_function(message_with_prompt, *args, **kwargs)

            # Step 3: Check if the response contains '<API>'
            if '<API>' in llm_response:
                # Step 4: Parse the LLM response to get API information
                api_info = parse_llm_response(llm_response)

                if api_info:
                    # Step 5: Call the API using self.call_api
                    plugin_name = api_info['plugin_name']
                    operation_id = api_info['operation_id']
                    parameters = api_info['parameters']

                    print(f"Using {plugin_name}")

                    api_response = self.call_api(plugin_name, operation_id, parameters)

                if api_response is not None:
                    # Step 6: Build a new call to the passed LLM function with API response summary
                    llm_summary = api_return_template.format(
                        user_message=user_message,
                        api_info=api_info,
                        api_response=api_response
                    )

                    # Step 7: Return the updated response
                    return llm_function(llm_summary, *args, **kwargs)

            # Return the original LLM response if no API calls were made
            return llm_response

        return decorator

    def build_functions(self) -> List[Dict[str, Any]]:
        '''Generate a list of JSON objects describing the active plugins.

        Returns
        -------
        list
            A list of JSON objects, each describing an active plugin.
        '''
        functions_list = []
        for plugin in self.active_plugins.values():
            for operation_id, operation in plugin.operation_details_dict.items():
                function = {
                    'name': plugin.name_for_model + "__opid__" + operation_id,
                    'description': plugin.description_for_model,
                }
                
                if operation['parameters'] != []:
                    function['parameters'] = {}
                    for parameter in operation['parameters']:
                        name = parameter.get('name')
                        function['parameters'][name] = {
                            'type': parameter.get('type'),
                            'description': parameter.get('description', ""),
                            'required': parameter.get('required')
                        }
                else:
                    if operation['requestBody'] != None:
                        function['parameters'] = {}
                        function['parameters']["type"] = "object"
                        function['parameters']["properties"] = {}
                        function['parameters']["required"] = []

                        for media_type, media_type_obj in operation['requestBody'].get('content', {}).items():
                            for name, schema in media_type_obj.get('schema', {}).get('properties', {}).items():
                                function['parameters']['properties'][name] = {
                                    'type': schema.get('type'),
                                    'description': schema.get('description', ""),
                                }
                                if schema.get('required'):
                                    function['parameters']['required'].append(name)
                                
                functions_list.append(function)
        return functions_list

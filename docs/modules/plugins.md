## count_tokens(text: str, model_name: str = "gpt-4") -> int

Count the number of tokens in a text.

### Parameters
- `text` (str): The input text.
- `model_name` (str): The name of the GPT model. Defaults to "gpt-4".

### Returns
- `int`: The number of tokens in the text.


## build_request_body(schema: Dict[str, Any], parameters: Dict[str, Any]) -> Any

Build the request body for an API call.

### Parameters
- `schema` (Dict[str, Any]): The schema for the request body.
- `parameters` (Dict[str, Any]): The parameters to pass to the API call.

### Returns
- `Any`: The request body.


## PluginObject

Represents an AI plugin object.

### Attributes
- `openapi` (dict): The OpenAPI specification for the plugin.
- `info` (dict): The info object from the OpenAPI spec.
- `paths` (dict): The paths object from the OpenAPI spec.
- `servers` (list): The servers list from the OpenAPI spec.
- `manifest` (dict): The plugin manifest.
- `url` (str): The plugin URL.
- `name_for_model` (str): The plugin name.
- `description_for_model` (str): The plugin description.
- `operation_details_dict` (dict): A dictionary containing details for each operation in the plugin.
- `description_prompt` (str): A prompt describing the plugin operations.
- `tokens` (int): The number of tokens in the description_prompt.

### Methods
- `__init__(self, url: str, spec: Dict[str, Any], manifest: Dict[str, Any])`: Initialize the PluginObject.
- `get_operation_details(self)`: Get the details for each operation in the plugin.
- `call_operation(self, operation_id: str, parameters: Dict[str, Any])`: Call an operation in the plugin.
- `describe_api(self)`: Generate a prompt describing the plugin operations.


## call_operation(operation_id: str, parameters: Dict[str, Any]) -> Optional[requests.Response]

Call an operation in the plugin.

### Parameters
- `operation_id` (str): The ID of the operation to call.
- `parameters` (dict): The parameters to pass to the operation.

### Returns
- `requests.Response` or `None`: The response from the API call, or `None` if unsuccessful.


## describe_api() -> str

Generate a prompt describing the plugin operations.

### Returns
- `str`: The generated prompt.


## Plugins

Manages installed and active plugins.

### Attributes
- `installed_plugins` (dict): A dictionary of installed PluginObject instances, keyed by plugin name.
- `active_plugins` (dict): A dictionary of active PluginObject instances, keyed by plugin name.
- `template` (str): The prompt template to use.
- `prompt` (str): The generated prompt with descriptions of active plugins.
- `tokens` (int): The number of tokens in the prompt.
- `max_plugins` (int): The maximum number of plugins that can be active at once.

### Methods
- `__init__(self, urls: List[str], template: str = None)`: Initialize the Plugins class.
- `install_and_activate(cls, urls: Union[str, List[str]], template: Optional[str] = None)`: Install plugins from URLs and activate them.
- `list_installed(self) -> List[str]`: Get a list of installed plugin names.
- `list_active(self) ->

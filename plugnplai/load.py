import json
import os

import jsonref
import requests
import yaml


def get_plugins(filter: str = None, provider: str = "plugnplai"):
    if provider == "plugnplai":
        base_url = "https://www.plugnplai.com/_functions/getUrls"
        # Construct the endpoint URL based on the filter argument
        if filter in ["working", "ChatGPT"]:
            url = f'{base_url.strip("/")}/{filter}'
        else:
            url = base_url
        # Make the HTTP GET request
        response = requests.get(url)
        # Check if the response status code is successful (200 OK)
        if response.status_code == 200:
            # Parse the JSON response and return the result
            return response.json()
        else:
            # Handle unsuccessful responses
            return f"An error occurred: {response.status_code} {response.reason}"
    elif provider == "pluginso":
        url = "https://plugin.so/api/plugins/list"
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the JSON response and return the result
            return [f"https://{entry['domain']}" for entry in response.json()]
        else:
            # Handle unsuccessful responses
            return f"An error occurred: {response.status_code} {response.reason}"


# given a plugin url, get the ai-plugin.json manifest, in "/.well-known/ai-plugin.json"
def get_plugin_manifest(url: str):
    urlJson = os.path.join(url, ".well-known/ai-plugin.json")
    response = requests.get(urlJson).json()
    return response


# load the OpenAPI specification for the plugin, given the OpenAPI url described in the manifest file
def get_openapi_url(url, manifest):
    openapi_url = manifest["api"]["url"]
    if openapi_url.startswith("/"):
        # remove slash in the end of url if present
        url = url.strip("/")
        openapi_url = url + openapi_url
    return openapi_url


# This code uses the following source: https://github.com/hwchase17/langchain/blob/master/langchain/tools/plugin.py
def marshal_spec(txt: str) -> dict:
    """Convert the yaml or json serialized spec to a dict."""
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return yaml.safe_load(txt)


def get_openapi_spec(openapi_url):
    openapi_spec_str = requests.get(openapi_url).text
    openapi_spec = marshal_spec(openapi_spec_str)
    # Use jsonref to resolve references
    resolved_openapi_spec = jsonref.JsonRef.replace_refs(openapi_spec)
    return resolved_openapi_spec


def spec_from_url(url):
    manifest = get_plugin_manifest(url)
    openapi_url = get_openapi_url(url, manifest)
    openapi_spec = get_openapi_spec(openapi_url)
    return manifest, openapi_spec


def extract_parameters(openapi_spec, path, method):
    parameters = {}

    # Extract path parameters and query parameters
    if "parameters" in openapi_spec["paths"][path][method]:
        for param in openapi_spec["paths"][path][method]["parameters"]:
            param_name = param["name"]
            param_type = param["in"]  # e.g., 'path', 'query', 'header'
            parameters[param_name] = {"type": param_type, "schema": param["schema"]}

    # Extract request body properties
    if "requestBody" in openapi_spec["paths"][path][method]:
        content = openapi_spec["paths"][path][method]["requestBody"]["content"]
        if "application/json" in content:
            json_schema = content["application/json"]["schema"]
            if "properties" in json_schema:
                for prop_name, prop_schema in json_schema["properties"].items():
                    parameters[prop_name] = {"type": "body", "schema": prop_schema}

    return parameters


def extract_all_parameters(openapi_spec):
    all_parameters = {}

    # Mapping of long type names to short names
    type_shorteners = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "number": "num",
        "array": "arr",
        "object": "obj",
    }

    # Iterate over all paths in the specification
    for path, path_item in openapi_spec["paths"].items():
        # Iterate over all methods (e.g., 'get', 'post', 'put') in the path item
        for method, operation in path_item.items():
            # Skip non-method keys such as 'parameters' that can be present in the path item
            if method not in [
                "get",
                "post",
                "put",
                "delete",
                "patch",
                "options",
                "head",
                "trace",
            ]:
                continue

            # Extract the operation ID
            operation_id = operation.get("operationId", f"{method}_{path}")

            # Extract the summary, or use an empty string if it doesn't exist
            summary = operation.get("summary", "")

            # Extract parameters for the current operation
            parameters = extract_parameters(openapi_spec, path, method)

            # Shorten the types in the parameters dictionary
            for param_info in parameters.values():
                param_type = param_info["schema"].get("type")
                if param_type in type_shorteners:
                    param_info["schema"]["type"] = type_shorteners[param_type]

            # Add the extracted information to the dictionary with the operation ID as the key
            all_parameters[operation_id] = {
                "summary": summary,
                "path": path,
                "method": method,
                "parameters": parameters,
            }

    return all_parameters

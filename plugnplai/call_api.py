import json
import re
import requests
from typing import Tuple
from load_plugin import ActivePlugins
import os


class CallApi:
    def __init__(self, llm_response: str, active_plugins: ActivePlugins):
        self.llm_response = llm_response
        self.active_plugins = active_plugins

    def extract_command(self) -> Tuple[str, str]:
        api_split = self.llm_response.split("<|api|>")
        if len(api_split) < 3:
            raise ValueError("API call not found.")
        api_call = api_split[1]

        body_split = api_split[2].split("<|body|>")
        if len(body_split) < 3:
            raise ValueError("API body not found.")
        api_body_str = body_split[1]

        try:
            api_body = json.loads(api_body_str)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in the API body. Content: {api_body_str}")
            return None, None
        
        self.api_pattern = "<|api|>"+api_split[1]+"<|api|>"+"<|body|>"+body_split[1]+"<|body|>"
        self.api_name = api_split[1].split(".")[0]

        return api_call, api_body

    def get_open_api_spec(self, namespace: str) -> dict:
        for plugin in self.active_plugins.Plugins:
            if plugin.name == namespace:
                return plugin.api_spec, plugin.url
        return None

    def build_request(self, api_call: str, api_body: dict) -> dict:
        # Assuming api_call format is "Namespace.Operation", e.g., "KlarnaProducts.productsUsingGET"
        namespace, operation = api_call.split(".")

        # Locate the API endpoint and method in the OpenAPI spec
        open_api_spec, plugin_url = self.get_open_api_spec(namespace)
        for path, methods in open_api_spec["paths"].items():
            for method, spec in methods.items():
                if spec["operationId"] == operation:
                    serverUrl = open_api_spec["servers"][0]["url"] + path
                    return {
                        "url": serverUrl,
                        "method": method.upper(),
                        # "headers": {"Content-Type": "application/json"},
                        "data": api_body,
                    }

    def make_request(self, request):
        response = requests.request(
            method=request["method"],
            url=request["url"],
            # headers=request["headers"],
            params=request["data"],
        )

        # Check if the response content is not empty and valid JSON
        try:
            json_data = response.json()
        except ValueError:
            print(f"Error: Response is not valid JSON. Content: {response.text}")
            print(f"Full response: {response}")
            return None

        return json_data    

    def process(self) -> str:
        try:
            api_call, api_body = self.extract_command()
        except ValueError as e:
            print(e)
            return self.llm_response.split("<|api|>")[0] + str(e)
        if api_call:
            request = self.build_request(api_call, api_body)
            response = self.make_request(request)
            message_to_user = f"Calling {self.api_name} API..."

            return response, re.sub(self.api_pattern, str(response), message_to_user)
        return self.llm_response

if __name__ == "__main__":
    # Load the ActivePlugins object as shown in your code
    with open("plugnplai/plugins.json", "r") as f:
        plugins_urls = json.load(f)
    active_plugins = ActivePlugins.from_urls_list(plugins_urls)
    print(active_plugins)

    llm_response = "<|api|>KlarnaProducts.productsUsingGET<|api|><|body|>{\n  \"q\": \"shirt\",\n  \"size\": \"1\"\n}<|body|>"
    call_api = CallApi(llm_response, active_plugins)
    processed_response = call_api.process()
    print(processed_response)
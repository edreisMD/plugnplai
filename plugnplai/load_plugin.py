# This code uses the following source:
# Title: langchain
# Author: hwchase17
# License: MIT
# URL: https://github.com/hwchase17/langchain/blob/master/langchain/tools/plugin.py
# Accessed on: 04/12/2023

import os
import requests
import json
import yaml
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ApiConfig(BaseModel):
    type: str
    url: str
    has_user_authentication: Optional[bool] = False

class PluginJson(BaseModel):
    """AI Plugin Definition."""

    schema_version: str
    name_for_model: str
    name_for_human: str
    description_for_model: str
    description_for_human: str
    auth: Optional[dict] = None
    api: ApiConfig
    logo_url: Optional[str]
    contact_email: Optional[str]
    legal_info_url: Optional[str]

    @classmethod
    def from_url(cls, url: str):
        """Instantiate AIPlugin from a URL."""
        response = requests.get(url).json()
        return cls(**response)

def marshal_spec(txt: str) -> dict:
    """Convert the yaml or json serialized spec to a dict."""
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return yaml.safe_load(txt)

def build_prompt_description(pluginJson, open_api_spec) -> str:
        """Build the prompt description for the plugin."""

        prompt_description = ""

        summary_plugin = f"// {pluginJson.description_for_model}"
        prompt_description += summary_plugin
        namespace_title = f"\nnamespace {pluginJson.name_for_model}"+" {"
        prompt_description += namespace_title
        content_paths = open_api_spec["paths"]
        
        for path, methods in content_paths.items():
            for method, info in methods.items():
                summary_method = f"\n\n// {info['summary']}"
                prompt_description += summary_method

                if "parameters" in info:
                    parameters = info["parameters"]
                    parametersDict = {}
                    for parameter in parameters:
                        par_name = parameter['name']
                        par_type = parameter['schema']['type']
                        parametersDict[par_name] = par_type

                    parametersStr = f"_: {parametersDict}"
                else:
                    parametersStr = ""

                method_schema = f"\noperationId {info['operationId']} = ({parametersStr}) => any" 

                prompt_description += method_schema 

        prompt_end = "\n}"
        prompt_description += prompt_end
            
        return prompt_description

class Plugin(BaseModel):
    
    name: str
    url: str
    description_for_model: str
    plugin_json: PluginJson
    prompt: str
    api_spec: dict

    @classmethod
    def plugin_from_url(cls, url: str) -> "Plugin":
        jsonURL = os.path.join(url, ".well-known/ai-plugin.json")
        pluginJson = PluginJson.from_url(jsonURL)

        if pluginJson.api.url.startswith("/"):
            print("starts with /")
            # remove slash in the end of url if present
            if url.endswith("/"):
                pluginJson.api.url = url[:-1] + pluginJson.api.url
            else:
                pluginJson.api.url = url + pluginJson.api.url
            print(pluginJson.api.url)

        open_api_spec_str = requests.get(pluginJson.api.url).text
        open_api_spec = marshal_spec(open_api_spec_str)

        prompt = build_prompt_description(pluginJson, open_api_spec)

        return cls(
            name=pluginJson.name_for_model,
            url = url,
            description_for_model=pluginJson.description_for_model,
            plugin_json=pluginJson,
            prompt=prompt,
            api_spec=open_api_spec
        )


def build_prompt_prefix(plugins) -> str:
    """Return the prompt with descriptions for the loaded APIs."""

    # Get today's date (without time)
    today_date = datetime.today().date()

    prefix_prompt = "Assistant is a large language model."
    prefix_prompt += "\nKnowledge Cutoff: 2021-09"
    prefix_prompt += f"\nCurrent date: {today_date}"
    prefix_prompt += "\nBellow are the APIs you have access to. Use one when it is useful to complete the task. To call an API add \"namespace.operationId\" between <|api|> tokens followed by the body for the call in between <|body|> tokes, e.g.:\n\n<|api|>speak.explainPhrase<|api|><|body|>{\n \"foreign_phrase\": \"cup\"\n \"learning_language\": \"English\",\n \"native_language\": \"English\",\n \"full_query\": \"what cup means?\"\n}<|body|>"

    for plugin in plugins:
        prefix_prompt += "\n\n"
        prefix_prompt += plugin.prompt
    return prefix_prompt

class InstallPlugins(BaseModel):

    Plugins: list
    Prompt: str
    
    @classmethod
    def from_urls_list(cls, urls: list) -> list:
        """Load the plugins from list."""

        plugins = []
        for url in urls:
            plugins.append(Plugin.plugin_from_url(url))
        prompt = build_prompt_prefix(plugins)
        return cls(Plugins=plugins, Prompt=prompt)


# if __name__ == "__main__":
#     # test one case
#     plugin = Plugin.plugin_from_url("https://chatgpt-todo-pluginfirst.edreismd.repl.co")

if __name__ == "__main__":
    # read the file with the list of plugins at ./plugins.json
    with open("plugnplai/plugins.json", "r") as f:
        plugins_urls = json.load(f)
    plugins = InstallPlugins.from_urls_list(plugins_urls)
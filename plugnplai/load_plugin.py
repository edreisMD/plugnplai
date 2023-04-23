# This code uses the following source:
# Title: langchain
# Author: hwchase17
# License: MIT
# URL: https://github.com/hwchase17/langchain/blob/master/langchain/tools/plugin.py
# Accessed on: 04/12/2023

import json
import os
from datetime import datetime
from typing import Optional

import requests
from pydantic import BaseModel

from plugnplai.utils.load import extract_all_parameters, get_openapi_spec


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


def build_prompt_description(pluginJson, open_api_spec) -> str:
    """Build the prompt description for the plugin."""

    parameters_dict = extract_all_parameters(open_api_spec)

    prompt_description = ""

    summary_plugin = f"// {pluginJson.description_for_model}"
    prompt_description += summary_plugin
    namespace_title = f"\nnamespace {pluginJson.name_for_model}" + " {"
    prompt_description += namespace_title

    for operationId in parameters_dict:
        info = parameters_dict[operationId]
        summary_method = f"\n\n// {info['summary']}"
        prompt_description += summary_method

        parameters = info["parameters"]
        parametersDict = {}
        for parameter in parameters:
            par_type = parameters[parameter]["schema"]["type"]
            parametersDict[parameter] = par_type
        parametersStr = f"_: {parametersDict}"
        method_schema = f"\noperationId {operationId} = ({parametersStr}) => any"
        prompt_description += method_schema

    prompt_end = "\n}"
    prompt_description += prompt_end

    return prompt_description

    # for method, info in methods.items():
    #     if "summary" in info:
    #         summary_method = f"\n\n// {info['summary']}"
    #     else:
    #         summary_method = "\n\n"
    #     prompt_description += summary_method

    #     if "parameters" in info:
    #         parameters = info["parameters"]
    #         parametersDict = {}
    #         for parameter in parameters:
    #             par_name = parameter['name']
    #             par_type = parameter['schema']['type']
    #             parametersDict[par_name] = par_type

    #         parametersStr = f"_: {parametersDict}"
    #     else:
    #         parametersStr = ""

    #     method_schema = f"\noperationId {info['operationId']} = ({parametersStr}) => any"

    #     prompt_description += method_schema


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

        open_api_spec = get_openapi_spec(pluginJson.api.url)

        prompt = build_prompt_description(pluginJson, open_api_spec)

        return cls(
            name=pluginJson.name_for_model,
            url=url,
            description_for_model=pluginJson.description_for_model,
            plugin_json=pluginJson,
            prompt=prompt,
            api_spec=open_api_spec,
        )


def build_prompt_prefix(plugins) -> str:
    """Return the prompt with descriptions for the loaded APIs."""

    # Get today's date (without time)
    today_date = datetime.today().date()

    prefix_prompt = "Assistant is a large language model."
    prefix_prompt += "\nKnowledge Cutoff: 2021-09"
    prefix_prompt += f"\nCurrent date: {today_date}"
    prefix_prompt += "\nBellow are the APIs you have access to. Use one when it is useful to complete the task."
    prefix_prompt += 'To call an API write "namespace.operationId" between [API] followed by the parameters for the call between [PARAMS] in the response to the user, following this pattern:'
    prefix_prompt += """
[API]namespace.operationId[API]
[PARAMS]
{
"parameter1": "query1",
"parameter2": "query2",
"parameter3": "query3"
}
[PARAMS]
"""
    n = 1
    for plugin in plugins:
        prefix_prompt += "\n\n// Plugin " + str(n) + ":\n\n"
        prefix_prompt += plugin.prompt
        n += 1
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

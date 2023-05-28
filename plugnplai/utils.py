import json
import ast
import os

import jsonref
import requests
import yaml
import re

def make_request_get(url: str, timeout=5):
    """Makes a GET request to the specified URL.

    Args:
        url (str): The URL to make a request to.
        timeout (int, optional): Timeout in seconds. Defaults to 5.

    Returns:
        requests.Response: The response from the request.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
        return None
    return response

def get_plugins(filter: str = None, verified_for = None, category: str = None, provider: str = "plugnplai"):
    """Gets a list of plugin URLs from a provider.

    Args:
        filter (str, optional): Filter to apply. Options are "working" or "ChatGPT". Defaults to None.
        verified_for (str, optional): Filter to plugins verified for a framework. Options are "langchain" or "plugnplai". Defaults to None.
        category (str, optional): Category to filter for. Defaults to None.
        provider (str, optional): Provider to get plugins from. Options are "plugnplai" or "pluginso". Defaults to "plugnplai".

# given a plugin url, get the ai-plugin.json manifest, in "/.well-known/ai-plugin.json"
def get_plugin_manifest(url: str):
    urlJson = os.path.join(url, ".well-known/ai-plugin.json")
    response = make_request_get(urlJson)
    return response.json()

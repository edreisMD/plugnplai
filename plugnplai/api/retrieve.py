import requests

def make_request_get(url: str):
    """Helper function to make a GET request.

    Args:
        url (str): URL to make the GET request to.

    Returns:
        Response: HTTP response object.
    """
    response = requests.get(url)
    return response

def retrieve(text: str, available_plugins: list):
    """Retrieve top plugins based on the provided text query.

    Args:
        text (str): Text query to find the top plugins.
        available_plugins (list): List of available plugin names.

    Returns:
        list/dict/str: Returns a list of top plugins if successful, dictionary of error info if unsuccessful, or error message if exception is caught.
    """
    base_url = "https://www.plugnplai.com/_functions"
    # Construct the endpoint URL based on the text query
    url = f'{base_url.strip("/")}/retrieve?text={text}'
    # Make the HTTP GET request
    try:
        response = make_request_get(url)
        # Check if the response status code is successful (200 OK)
        if response.status_code == 200:
            # Parse the JSON response
            plugins = response.json()
            # Filter plugins to only include ones that are in the list of available plugins
            filtered_plugins = [plugin for plugin in plugins if plugin in available_plugins]
            return filtered_plugins
        elif response.status_code in [400, 500]:
            # Handle unsuccessful responses
            return response.json()  # Assuming the API returns error info in JSON format
        else:
            # Handle other potential status codes
            return f"An error occurred: {response.status_code} {response.reason}"
    except requests.exceptions.RequestException as e:
        return str(e)

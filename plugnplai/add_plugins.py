from typing import Any, Callable

from plugnplai.call_api import CallApi


class AddPlugins:
    def __init__(self, active_plugins):
        self.active_plugins = active_plugins

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            # Call the original function (GPT-4 API call)
            llm_response = func(*args, **kwargs)

            # Check for the specific pattern (**) in the response
            if "[API]" not in llm_response:
                return llm_response

            # Use the CallApi class to make an API call based on the response
            call_api = CallApi(llm_response, self.active_plugins)
            response, message_to_user = call_api.process()

            # Call the original function again with the result of the API call
            return func(message_to_user, **kwargs)

        return wrapper

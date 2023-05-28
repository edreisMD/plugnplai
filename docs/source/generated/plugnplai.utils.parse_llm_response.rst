plugnplai.utils.parse_llm_response
===================================

.. autofunction:: plugnplai.utils.parse_llm_response

The ``parse_llm_response()`` function parses an LLM response to extract an API call.

Parameters
----------

- ``llm_response`` (required): The response from the LLM.

Return Value
------------

A dict containing:

- ``plugin_name``: The name of the plugin
- ``operation_id``: The operation ID of the API call 
- ``parameters``: The parameters for the API call

For example:

.. code-block:: python

   >>> from plugnplai import parse_llm_response
   >>> llm_response = '[API]KlarnaProducts.productsUsingGET[/API]\n[PARAMS]{\n    "q": "t-shirt", \n    "size": 3\n}[/PARAMS]'
   >>> call_dict = parse_llm_response(llm_response)
   >>> call_dict
   {'plugin_name': 'KlarnaProducts', 
    'operation_id': 'productsUsingGET', 
    'parameters': {'q': 't-shirt', 'size': 3}}



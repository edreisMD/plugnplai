plugnplai.utils.spec_from_url
==============================

.. autofunction:: plugnplai.utils.spec_from_url

The ``spec_from_url()`` function returns an OpenAPI specification from a plugin URL.

Parameters
----------

- ``url`` (required): The URL of the plugin.

Return Value
------------

A tuple containing:

- The plugin manifest (a dict)
- The OpenAPI specification (a dict)

For example:

.. code-block:: python

   >>> import plugnplai as pl
   >>> manifest, spec = pl.spec_from_url('https://trip.com')
   >>> manifest
   {'name': 'Trip', 
    'description': 'Plugin for users to effortlessly get customized travel product recommendation and itinerary planning including hotels and flights using chatGPT.', 
    'author': 'Trip.com', 
    'version': '1.0.0'}
   >>> spec
   {'openapi': '3.0.2', 
    'info': {'title': 'Trip Plugin', 'description': 'This is the OpenAPI specification for the Trip plugin.', 'version': '1.0.0'},
   # Rest of spec...



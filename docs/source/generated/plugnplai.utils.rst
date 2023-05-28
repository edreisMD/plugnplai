plugnplai.utils
==============

.. automodule:: plugnplai.utils
   :members:
   :undoc-members:
   :show-inheritance:

The ``utils`` module contains utility functions for PlugnPlai.

get_plugins()
-------------

.. autofunction:: get_plugins

The ``get_plugins()`` function returns a list of plugin URLs from the PlugnPlai directory. It takes the following parameters:

- ``category`` (optional): Filter plugins by category. Options are ``travel``, ``shopping``, ``weather``, ``language``, ``knowledge``, ``productivity``.
- ``filter`` (optional): Filter plugins by ``working`` (only tested plugins) or ``ChatGPT`` (only ChatGPT verified plugins).

For example:

.. code-block:: python

   >>> import plugnplai as pl
   >>> urls = pl.get_plugins(category='travel')
   >>> urls
   ['https://llmsearch.endpoint.getyourguide.com', 
    'https://gogaffl.com', 
    'https://trip.com', 
    'https://api.yelp.com', 
    'https://gps-telecom.com']



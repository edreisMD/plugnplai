plugnplai.utils.get_plugins
============================

.. autofunction:: plugnplai.utils.get_plugins

The ``get_plugins()`` function returns a list of plugin URLs from the PlugnPlai directory.

Parameters
----------

- ``category`` (optional): Filter plugins by category. Options are:

  - ``travel``
  - ``shopping`` 
  - ``weather``
  - ``language``
  - ``knowledge``
  - ``productivity``

- ``filter`` (optional): Filter plugins by:

  - ``working`` (only tested plugins) 
  - ``ChatGPT`` (only ChatGPT verified plugins)

Return Value
------------

A list of plugin URLs. For example:

.. code-block:: python

   >>> import plugnplai as pl
   >>> urls = pl.get_plugins(category='travel')
   >>> urls
   ['https://llmsearch.endpoint.getyourguide.com', 
    'https://gogaffl.com', 
    'https://trip.com', 
    'https://api.yelp.com', 
    'https://gps-telecom.com']



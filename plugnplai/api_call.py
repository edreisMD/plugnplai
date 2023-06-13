'''
The aim is to build utilitarian functions here to call the different types of API auth
'''

# def make_request_get(url: str, timeout=5):
#     """Make an HTTP GET request.

#     Args:
#         url (str): URL to make request to.
#         timeout (int, optional): Timeout in seconds. Defaults to 5.

#     Returns:
#         requests.Response: Response from request.
#     """
#     try:
#         response = requests.get(url, timeout=timeout)
#         response.raise_for_status()  # Raises stored HTTPError, if one occurred.
#     except requests.exceptions.HTTPError as errh:
#         print ("Http Error:",errh)
#     except requests.exceptions.ConnectionError as errc:
#         print ("Error Connecting:",errc)
#     except requests.exceptions.Timeout as errt:
#         print ("Timeout Error:",errt)
#     except requests.exceptions.RequestException as err:
#         print ("Something went wrong",err)
#         return None
#     return response



# def call_operation(self, operation_id: str, parameters: Dict[str, Any]) -> Optional[requests.Response]:
#         """Call an operation in the plugin.
        
#         Parameters
#         ----------
#         operation_id : str
#             The ID of the operation to call.
#         parameters : dict
#             The parameters to pass to the operation.
            
#         Returns
#         -------
#         requests.Response or None
#             The response from the API call, or None if unsuccessful.
#         """
#         # Get the operation details from the operation_details_dict attribute
#         operation_details = self.operation_details_dict.get(operation_id)
#         if not operation_details:
#             print(f'Operation {operation_id} not found')
#             return None

#         # Separate parameters by type
#         path_parameters = {}
#         query_parameters = {}
#         header_parameters = {}
#         cookie_parameters = {}
#         body = None

#         for parameter in operation_details['parameters']:
#             if parameter['in'] == 'path':
#                 path_parameters[parameter['name']] = parameters.get(parameter['name'])
#             elif parameter['in'] == 'query':
#                 query_parameters[parameter['name']] = parameters.get(parameter['name'])
#             elif parameter['in'] == 'header':
#                 header_parameters[parameter['name']] = parameters.get(parameter['name'])
#             elif parameter['in'] == 'cookie':
#                 cookie_parameters[parameter['name']] = parameters.get(parameter['name'])

#         if operation_details['requestBody']:
#             body_schema = operation_details['requestBody']['content']['application/json']['schema']
#             body = build_request_body(body_schema, parameters)

#         # Replace path parameters in the URL
#         url = operation_details['url']
#         for name, value in path_parameters.items():
#             url = url.replace('{' + name + '}', str(value))

#         # Make the API call
#         method = operation_details['method']
#         if method.lower() == 'get':
#             response = requests.get(url, params=query_parameters, headers=header_parameters, cookies=cookie_parameters)
#         elif method.lower() == 'post':
#             headers = {'Content-Type': 'application/json'}
#             response = requests.post(url, params=query_parameters, headers=headers, cookies=cookie_parameters, json=body)

#         return response
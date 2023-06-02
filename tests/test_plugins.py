import unittest
from plugnplai.plugins import PluginObject

class TestPluginObject(unittest.TestCase):
    def setUp(self):
        self.url = "https://example.com/openapi.json"
        self.manifest = {"name_for_model": "Example"}
        self.spec = {
            "openapi": "3.0.1",
            "info": {"title": "Example API", "version": "1.0"},
            "paths": {
                "/sum": {
                    "get": {
                        "operationId": "sum",
                        "parameters": [
                            {"name": "a", "in": "query", "required": True, "schema": {"type": "integer"}},
                            {"name": "b", "in": "query", "required": True, "schema": {"type": "integer"}},
                        ],
                        "responses": {"200": {"description": "Success"}},
                    }
                }
            },
        }
        self.plugin_object = PluginObject(self.url, self.spec, self.manifest)

    def test_describe_api(self):
        expected = "// Example API\nnamespace Example {\n\n// \noperationId sum = (_: {'a'*: 'int', 'b'*: 'int'}) => any}"
        self.assertEqual(expected, self.plugin_object.describe_api())

    def test_call_operation(self):
        response = self.plugin_object.call_operation("sum", {"a": 1, "b": 2})
        self.assertIsNone(response)

    def test_count_tokens(self):
        text = "Hello world!"
        expected = 2
        self.assertEqual(expected, self.plugin_object.count_tokens(text))



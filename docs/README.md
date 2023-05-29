# Plugnplai Documentation

Plugnplai is a Python library to integrate AI plugins into large language models (LLMs) such as GPT.

The main features are:

- Get a list of AI plugins from [plugnplai.com](https://plugnplai.com)
- Load plugins manifests and specifications
- Generate a prompt to describe the plugins to the LLM
- Parse the LLM response to call the plugins APIs
- Customize the prompt template

To get started, check the [Quickstart](get-started/quickstart.md) guide.

The full documentation is organized into the following sections:

- [Get Started](get-started/quickstart.md)
- [Examples](examples/index.md)
- [API Reference](reference/modules.rst)

## Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) for details on how to contribute.

## License

```bash
cd docs
make html
```

The docs HTML files are now generated under `docs/_build/html` directory, you can preview
it locally with the following command:

```bash
python -m http.server 8000 -d _build/html
```

And open your browser at http://0.0.0.0:8000/ to view the generated docs.


##### Watch Docs

During development, it is advisable to utilize sphinx-autobuild, which offers a live-reloading server. This server automatically rebuilds the documentation and refreshes any open pages whenever changes are saved. This feature facilitates a shorter feedback loop, thereby enhancing productivity when writing documentation.

Simply run the following command from Plugnplai project's root directory: 
```bash
make watch-docs
```

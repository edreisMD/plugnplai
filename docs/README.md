# Plugnplai Documentation

## A guide for docs contributors

The `docs` directory contains the sphinx source text for Plugnplai's documentation.

This guide is made for anyone who's interested in running the docs locally, or
contributing to the docs.

## Build Docs

If you haven't already, clone the Plugnplai Github repo to a local directory:


Install all dependencies required for building docs (mainly `sphinx` and its extension):

```bash
pip install -r docs/requirements.txt
```

Build the sphinx docs:

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
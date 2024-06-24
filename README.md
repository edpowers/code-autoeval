### Code Autogeneration with Unit tests + 100% Coverage

#### Overview:
This library aims to solve the basic problem with LLMs of an inability to test in a local environment, and iterate on the result. Instead of copying/pasting error codes, it would be great to have the LLM iterate based on the error codes already provided.

Other major changes:
1. Having the LLM construct fake testing data using the faker library.
2. Writing unit tests and achieving 100% coverage for the generated code.

#### Requirements
1. A working poetry installation. Please see [Poetry Installation](https://python-poetry.org/docs/) for steps to install.
2. A backend LLM or OpenAI url to supply as environment variable: OPENAI_BASE_URL
3. The model name environment variable: OPENAI_MODEL_NAME

#### Installation
Requires Poetry. When specifying individual libraries for the code-autogen, those need to be installed within the environment as well.

Run git clone of the repository:
```
git clone https://github.com/edpowers/code-autoeval.git
```

Navigate to the repository base:
```
cd code-autoeval
```

Assuming poetry is installed:
```
poetry install
```

Can also install dev dependencies by running:
```
poetry install --with dev
```

#### Examples:
workbooks/example.py
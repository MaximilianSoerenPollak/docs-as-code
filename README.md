# docs-as-code

Docs-as-code tooling for Eclipse S-CORE

## Overview

The S-CORE docs Sphinx configuration and build code.

> [!NOTE]
> This repository offers a [DevContainer](https://containers.dev/).
> For setting this up read [eclipse-score/devcontainer/README.md#inside-the-container](https://github.com/eclipse-score/devcontainer/blob/main/README.md#inside-the-container).

## Building documentation

#### Run a documentation build:

#### Integrate latest score main branch

```bash
bazel run //docs:incremental_latest
```

#### Access your documentation at:

- `_build/` for incremental

#### Getting IDE support

Create the virtual environment via `bazel run //docs:ide_support`.\
If your IDE does not automatically ask you to activate the newly created environment you can activate it.

- In VSCode via `ctrl+p` => `Select Python Interpreter` then select `.venv_docs/bin/python`
- In the terminal via `source .venv_docs/bin/activate`

#### Format your documentation with:

```bash
bazel test //src:format.check
bazel run //src:format.fix
```

#### Find & fix missing copyright

```bash
bazel run //:copyright-check
bazel run //:copyright.fix
```

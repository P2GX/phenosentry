# phenosentry

A Python package for ensuring data quality in phenopackets and collections of phenopackets.

## Features
- Validate phenopacket with quality checks

## Installation

Install with [Poetry](https://python-poetry.org/):

```bash
poetry add phenosentry
```
or with pip:

```bash
pip install phenosentry
```

### Installing with command-line interface

Use of the command-line interface requires installing `phenosentry` with the `cli` extra:

```bash
poetry add phenosentry[cli]
```


## Usage

Phenosentry can be used either as a library or as a command-line application.


### Example usage as a library

An example of a library usage:

```python
from pathlib import Path

from phenosentry.io import read_phenopacket
from phenosentry.model import AuditorLevel
from phenosentry.validation import get_phenopacket_auditor

# Read a phenopacket.
path = "path/to/phenopacket.json"
phenopacket = read_phenopacket(path=Path(path))

# Prepare the auditor and a notepad for recording the validation issues.
auditor = get_phenopacket_auditor()
notepad = auditor.prepare_notepad("validation")

# Audit the phenopacket.
auditor.audit(
    item=phenopacket,
    notepad=notepad,
)

# Inspect the notepad for errors.
if notepad.has_errors_or_warnings(include_subsections=True):
    print("Invalid Phenopacket")
    notepad.summarize()
else:
    print("Valid Phenopacket")
```


### Example CLI usage

We can validate a phenopacket by invoking the `validate` command.

```bash
phenosentry validate --path data/example-phenopacket.json
```

The command should point out presence of a forbidden character `\t` in the phenopacket's identifier.

# Development
Run tests with:

```bash
poetry run pytest
```

Format the code with:

```bash
poetry run ruff format
```

Run linting with:

```bash
poetry run ruff check phenosentry
```

# License 
MIT License
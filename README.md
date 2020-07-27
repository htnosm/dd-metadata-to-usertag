# dd-metadata-to-usertag
Add Datadog host's metadata to user tag

## Description

* Preserve existing user tags
* Tag key with the same name updates the value
* Specify the metadata to be tags in include_keys.yml
    * metadata can be referenced from [Infrastructure] -> [Infrastructure List] -> "JSON API permalink"

## Requirements

* python 3.8+
* [DataDog/datadogpy: The Datadog Python library](https://github.com/DataDog/datadogpy)
* PyYAML

## Installation

### From pip

```
pip install git+https://github.com/htnosm/dd-metadata-to-usertag.git
```

### From source

```
python setup.py install

or

pip install .
```

## Usage

```bash
export DD_API_KEY=""
export DD_APP_KEY=""

# Help
dd_add_metadata -h
# DryRun
dd_add_metadata
# Add or Update
dd_add_metadata -a
```

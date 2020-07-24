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

```
virtualenv -p python3 .venv
. ./.venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
cd dd_add_metadata/

export DD_API_KEY=""
export DD_APP_KEY=""

# Help
python dd_add_metadata.py -h
# DryRun
python dd_add_metadata.py -d
# Update
python dd_add_metadata.py
```

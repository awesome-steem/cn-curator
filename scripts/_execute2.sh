#!/bin/sh

set -e

# set to Hive node
export API_NODE=https://anyx.io

pipenv run invoke recipe.info -r cn-reader
pipenv run invoke recipe.vote -r cn-reader

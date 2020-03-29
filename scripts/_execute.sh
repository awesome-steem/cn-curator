#!/bin/sh

set -e

pipenv run invoke recipe.info -r cn-reader
pipenv run invoke recipe.vote -r cn-reader

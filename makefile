# Set variables. --- {{{
SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PYTHON_FILES := $(shell find . -iname "*.py")
# --- }}}

# Project management. --- {{{
all: run

run: $(PYTHON_FILES)

clean:
	find . -iname '*.pyc' -print0 | xargs -0 rm -f
	find . -iname '__pycache__' -print0 | xargs -0 rm -rf
	find ./output/ -type f -not -path '*/\.*' -print0 | xargs -0 rm -f

%.py: .FORCE
	MPLBACKEND=agg \
	JOBLIB_TEMP_FOLDER=/tmp/ \
		python3 $@

.FORCE:
# --- }}}

.PHONY: all clean run install backup kill_connections

#  vim: set filetype=make fileformat=unix wrap spell spelllang=en_us :

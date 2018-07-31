# Set variables. --- {{{
SHELL := /bin/bash

NOW := $(shell date -u +%Y-%m-%d_%Hh%Mm%Ss)
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BASENAME := $(shell basename $(ROOT_DIR))

PYTHON_FILES := $(shell  find . \
        -not -path "*bonus_assignment_01_fiji_earthquakes*" \
        -not -path "*05_data*" \
        -not -path "*instructor*" \
        -not -iname "*instructor*" \
        -iname "*.py")
        #  -path "*05_data*" \
# --- }}}

# Project management. --- {{{
all: run

run: $(PYTHON_FILES)

install:
	# TODO: https://github.com/matplotlib/basemap
	# Requires GEOS.
	# TODO: pip install

clean:
	find . -iname '*.pyc' -print0 | xargs -0 rm -f
	find . -iname '__pycache__' -print0 | xargs -0 rm -rf
	find ./output/ -type f -not -path '*/\.*' -print0 | xargs -0 rm -f

%.py: .FORCE
	cd $$(dirname $@) && \
		PYTHONPATH=$(PYTHONPATH):$(ROOT_DIR)/lib \
		MPLBACKEND=agg \
		JOBLIB_TEMP_FOLDER=/tmp/ \
			python3 $$(basename $@)

export_results: .FORCE
	(find . -size '-100k' -type f -print0 ;\
	 find . -iname '.gitkeep' -type f -print0) |\
		tar -cvzf \
		"$(shell dirname $(ROOT_DIR))/$(NOW)_$(BASENAME)_export_results.tar.gz" \
		--null -T -

.FORCE:
# --- }}}

.PHONY: all clean run install backup kill_connections

#  vim: set filetype=make fileformat=unix wrap spell spelllang=en_us :

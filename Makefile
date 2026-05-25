PYTHON ?= python3

ASSET_SOURCES := $(shell find assets -type f 2>/dev/null)
ASSET_TARGETS := $(patsubst assets/%,build/assets/%,$(ASSET_SOURCES))

.PHONY: all clean docs serve

all: $(ASSET_TARGETS) docs

docs: $(ASSET_TARGETS)
	$(PYTHON) tools/gen_docs.py

build/assets/%: assets/%
	@mkdir -p $(dir $@)
	cp -p $< $@

clean:
	rm -rf build

serve: all
	$(PYTHON) -m http.server 8000 --directory build

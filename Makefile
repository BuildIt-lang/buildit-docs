BASE_DIR=$(shell pwd)
SRC_DIR=$(BASE_DIR)/src
BUILD_DIR?=$(BASE_DIR)/build

$(shell mkdir -p $(BUILD_DIR))

TEMPLATE_DIR=$(BASE_DIR)/template

SRCS=$(wildcard $(SRC_DIR)/*.md)
OBJS=$(subst $(SRC_DIR),$(BUILD_DIR),$(SRCS:.md=.html))

TEMPLATES=$(wildcard $(TEMPLATE_DIR)/*.html)
ASSETS=$(BUILD_DIR)/style.css

all: $(OBJS) $(ASSETS)

$(BUILD_DIR)/%.html: $(SRC_DIR)/%.md $(TEMPLATES)
	bash -c 'cat $(TEMPLATE_DIR)/top.html <(markdown $<) $(TEMPLATE_DIR)/bottom.html > $@'

$(BUILD_DIR)/style.css: $(TEMPLATE_DIR)/style.css
	cp $< $@

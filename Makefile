BASE_DIR=$(shell pwd)
SRC_DIR=$(BASE_DIR)/src
BUILD_DIR?=$(BASE_DIR)/build

$(shell mkdir -p $(BUILD_DIR))

TEMPLATE_DIR=$(BASE_DIR)/template

SRCS=$(wildcard $(SRC_DIR)/*.md)
OBJS=$(subst $(SRC_DIR),$(BUILD_DIR),$(SRCS:.md=.html))

TEMPLATES=$(wildcard $(TEMPLATE_DIR)/*.html)
ASSETS=$(BUILD_DIR)/style.css $(BUILD_DIR)/logo-buildit.png

#
STYLE_HASH=$(shell md5sum $(TEMPLATE_DIR)/style.css | cut -f1 -d" ")
#

all: $(OBJS) $(ASSETS)

$(BUILD_DIR)/%.html: $(SRC_DIR)/%.md $(TEMPLATES) $(ASSETS)
	bash -c 'cat $(TEMPLATE_DIR)/top.html <(markdown $<) $(TEMPLATE_DIR)/bottom.html > $@'	
	sed 's/STYLE_HASH/$(STYLE_HASH)/g' -i $@
	sed 's/\\k{\([a-z#]*\)}/<span class="code-keyword">\1<\/span>/g' -i $@

$(BUILD_DIR)/%: $(TEMPLATE_DIR)/%
	cp $< $@


clean: 
	- rm -rf $(BUILD_DIR)

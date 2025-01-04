#!/bin/bash

INPUT_FILE=$1
TEMPLATE_DIR=$2
OUTPUT_FILE=$3

STYLE_HASH=$(md5sum $TEMPLATE_DIR/style.css | cut -f1 -d" ")

cat $TEMPLATE_DIR/top.html <(sed -f make/presubs.txt $INPUT_FILE | markdown) $TEMPLATE_DIR/bottom.html > $OUTPUT_FILE

sed 's/STYLE_HASH/'$STYLE_HASH'/g' -i $OUTPUT_FILE
sed -f make/subs.txt -i $OUTPUT_FILE

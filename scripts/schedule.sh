#!/bin/sh

SCRAPYD_URL=$1
SCRAPYD_PROJECT=$2

curl -s $SCRAPYD_URL/listspiders.json?project=$SCRAPYD_PROJECT \
| jq -r '.spiders[]' \
| xargs -I{} curl -s $SCRAPYD_URL/schedule.json -d project=$SCRAPYD_PROJECT -d spider={}

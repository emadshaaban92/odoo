#!/bin/sh

script="$0"
basename="$(dirname $script)"

$basename/disable.sh
$basename/enable.sh

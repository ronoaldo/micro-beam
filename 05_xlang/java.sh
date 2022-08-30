#!/bin/bash
set -x

# Helper para invocar o Maven com todos os parâmetros
main=$1
shift
pipeline_args="$@"

case $@ in
    *DataflowRunner*) MVN_ARGS="-Pdataflow-runner" ;;
esac

mvn -f ./java $MVN_ARGS \
    compile exec:java \
    -Dexec.mainClass="$main" \
    -Dexec.args="${pipeline_args}"

#!/bin/bash
set -e

FAIL=0
GO_RUNNER="${GO_RUNNER:-direct}"

# Show info message
info() {
    echo "$(date +"%Y-%m-%d %H:%M:%S")  INFO: $*"
}

# Show error message and mark test as failed
error() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR: $*"
    FAIL=$((FAIL+1))
}

# Check if failed on exit
on_exit() {
    RET=$?
    if [ "$RET" -ne 0 ] ; then
        error "Execution failed with exit code $RET"
        exit $RET
    fi

    if [ "$FAIL" -gt 0 ] ; then
        error "Some integration tests failed"
        exit 1
    fi

    info "All integration tests passed"
}

# Catch errors on exit
trap 'on_exit' EXIT

# Run pipeline integration test
run_pipeline() {
    local dir="$1"
    info "--- RUN: Running test into $dir"
    pushd "$dir" || exit 1
    
    if [ -f pipeline.py ]; then
        info "     pipeline.py"
        python pipeline.py || error "--- FAIL: pipeline.py $dir"
    fi

    # Using the direct runner until https://github.com/apache/beam/issues/29180 gets fixed
    if [ -f pipeline.go ]; then
        go run pipeline.go --runner=${GO_RUNNER} || error "--- FAIL: pipeline.go $dir"
    fi
    if [ -f go/pipeline.go ]; then
        go run go/pipeline.go --runner=${GO_RUNNER} || error "--- FAIL: go/pipeline.go $dir"
    fi

    popd || exit 1
    info "--- PASS: $dir"
}

# Test Case #1
run_pipeline "01_hello-world"

# Test Case #2
run_pipeline "02_schemas"

# shellcheck disable=2015
# Test Case #3
03_jdbc/db/run.sh && run_pipeline "03_jdbc" || error "--- FAIL: unable to setup database"

# Test Case #5
run_pipeline "05_xlang"

#!/bin/bash

set -e

PROTO_ROOT="protos"
PROTO_GEN_DIR="$PROTO_ROOT/gen"
PROTO_CONTRACTS_DIR="$PROTO_ROOT/contracts"

rm -rf "$PROTO_GEN_DIR"
mkdir -p "$PROTO_GEN_DIR"

python -m grpc_tools.protoc \
  -I"$PROTO_ROOT" \
  -I"$PROTO_CONTRACTS_DIR" \
  --python_out="$PROTO_GEN_DIR" \
  --grpc_python_out="$PROTO_GEN_DIR" \
  --mypy_out="$PROTO_GEN_DIR" \
  $(find "$PROTO_CONTRACTS_DIR" -name "*.proto")

find "$PROTO_GEN_DIR" -type d -exec touch {}/__init__.py \;

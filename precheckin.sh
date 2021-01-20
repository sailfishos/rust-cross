#!/bin/sh
# The base rust package provides the native packages
ARCHS="armv7hl aarch64"

for x in $ARCHS; do
	sed "s/@ARCH@/$x/g" rust-cross-template.spec > rust-cross-$x.spec
done

# -*- coding: utf-8 -*-
name = "openexr"
version = "3.3.3"
authors = ["ILM", "ASWF"]
description = "OpenEXR image file format library"

requires = [
    "imath-3.2.0",
    "zlib-1.2.13",
]

variants = []

build_requires = [
    "cmake-3.26.5",
    "gcc-11.5.0",
]

build_command = "python {root}/rezbuild.py {install}"

def commands():
    env.OPENEXR_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.prepend("{root}/lib64")
    env.LIBRARY_PATH.prepend("{root}/lib64")
    env.CPATH.prepend("{root}/include")
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PKG_CONFIG_PATH.prepend("{root}/lib64/pkgconfig")

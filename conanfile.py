#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Conan receipt package for USB Library
"""
import os
from conans import ConanFile, VisualStudioBuildEnvironment, AutoToolsBuildEnvironment, tools


class LibUSBConan(ConanFile):
    """Download libusb source, build and create package
    """
    name = "libusb"
    version = "0.1.12"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    homepage = "https://github.com/libusb/libusb"
    url = "http://github.com/bincrafters/conan-libusb"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "https://github.com/libusb/libusb/blob/master/COPYING"
    description = "A cross-platform library to access USB devices"
    source_subfolder = "source_subfolder"
    exports = ["LICENSE.md"]

    def source(self):
        host_url = "https://ufpr.dl.sourceforge.net/project/libusb/libusb-0.1%20%28LEGACY%29"
        release_name = "%s-%s" % (self.name, self.version)
        tools.get("{0}/{1}/{2}.tar.gz".format(host_url, self.version, release_name))
        os.rename(release_name, self.source_subfolder)

    def configure(self):
        if self.settings.os != "Linux":
            raise Exception("libusb legacy is only supported on Linux.")
        del self.settings.compiler.libcxx

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True
        env_build.flags.append('-w')
        with tools.environment_append(env_build.vars):
            configure_args = ['--prefix=%s' % self.package_folder]
            with tools.chdir(self.source_subfolder):
                env_build.configure(args=configure_args)
                env_build.make(args=["all"])
                env_build.make(args=["install"])

    def package(self):
        self.copy("COPYING", src=self.source_subfolder, dst="licenses", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.libs.append("pthread")

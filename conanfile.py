from conans import ConanFile, tools
import os, posixpath
import sys
import re

def TO_CMAKE_PATH(path):
    if tools.os_info.is_windows:
    # this is meant to be the same as CMake's SystemTools::ConvertToUnixSlashes
        return posixpath.normpath('/'.join(path.split(os.path.sep)))
    else:
        return os.path.normpath(path)

class CmakeModulesConan(ConanFile):
    name = "cmake-conan"
    version = "0.15+FOCUS.1"
    description = "CMake wrapper for conan C and C++ package manager"
    url = "https://github.com/conan-io/cmake-conan"

    scm = {
        "type": "git",
        "url": "https://github.deere.com/FOCUS/cmake-modules.git",
        "revision": "auto"
    }

    def package(self):
        self.copy("LICENSE")
        self.copy("conan.cmake*")
        self.copy("cmake-conan-config.cmake")

    def deploy(self):
        # https://cmake.org/help/latest/manual/cmake-packages.7.html#user-package-registry
        self.output.info("Registering find_package(cmake-conan) to %s" % self.package_folder)
        if tools.os_info.is_windows:
            import winreg
            winreg.SetValue(winreg.HKEY_CURRENT_USER,"SOFTWARE\\Kitware\\CMake\\Packages\\cmake-conan",winreg.REG_SZ, self.package_folder)
        elif tools.os_info.is_linux:
            tools.save(os.path.expanduser("~/.cmake/packages/cmake-conan/package_folder"), self.package_folder + "\n")

        # find the conan install which launched this deploy(), and remember it for conan_cmake_run
        conan_command = sys.argv[0]
        if re.search('conan(?:\\.exe)?$', conan_command, re.IGNORECASE): # make sure we actually got conan(.exe)?, not python
            self.output.info("set(CONAN_COMMAND \"%s\")" % TO_CMAKE_PATH(conan_command))
            tools.save(os.path.join(self.package_folder, "deploy/conan.cmake"),
                       "set(CONAN_COMMAND \"%s\")\n" % TO_CMAKE_PATH(conan_command))

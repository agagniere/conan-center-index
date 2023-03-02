from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMakeDeps, CMakeToolchain, CMake

import os

config = {
    'ENABLE_PYTHON_API': 'OFF',
    'ENABLE_EXAMPLES': 'OFF',
    'ENABLE_UTILS': 'OFF',
    'ENABLE_TESTS': 'OFF',
    'ENABLE_USB': 'OFF',
    'ENABLE_B100': 'OFF',
    'ENABLE_B200': 'OFF',
    'ENABLE_X400': 'OFF',
    'ENABLE_SIM': 'OFF',
    'ENABLE_MPMD': 'OFF',
    'ENABLE_USRP1': 'OFF',
    'ENABLE_USRP2': 'OFF',
    'ENABLE_N300': 'OFF',
    'ENABLE_N320': 'OFF',
    'ENABLE_E300': 'OFF',
    'ENABLE_E320': 'OFF',
    'ENABLE_OCTOCLOCK': 'OFF',
    'ENABLE_DOXYGEN': 'OFF',
    'ENABLE_MANUAL': 'OFF',
    'ENABLE_MAN_PAGES': 'OFF',
}

class UhdConan(ConanFile):
    name = "uhd"
    license = "GPLv3"
    url = "https://github.com/EttusResearch/uhd.git"
    description = "Universal Software Radio Peripheral"
    topics = ("sdr", "usrp")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "CMakeDeps"
    requires = "boost/[>=1.65.0]"

    def source(self):
        git = Git(self, self.source_folder)
        git.clone(self.url, '.', ['--depth=1', '--sparse', '--filter=blob:none', '--branch', self.version])
        git.run('sparse-checkout init --cone')
        git.run('sparse-checkout set host')

    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(config,
                        os.path.join(self.source_folder, 'host'))
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="host/include")
        self.copy("*.hpp", dst="include", src="host/include")
        self.copy("*.ipp", dst="include", src="host/include")
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["uhd"]

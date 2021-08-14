import versioneer
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


PACKAGE_NAME = "openscm_ar6_wg1_data_compilation"

DESCRIPTION = (
    "Code for compiling AR6 WG1 data for use with scmdata and related packages like pyam"
)

SOURCE_DIR = "src"

ENTRY_POINTS = {"console_scripts": ["openscm-ar6-wg1-data-compilation = openscm_ar6_wg1_data_compilation.cli:cli"]}


class Utils(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        pytest.main(self.test_args)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": Utils})


setup(
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    name=PACKAGE_NAME,
    description=DESCRIPTION,
    packages=find_packages(SOURCE_DIR),  # no exclude as only searching in `src`
    package_dir={"": SOURCE_DIR},
    entry_points=ENTRY_POINTS,
)

"""
PolyGraph installation setup
"""

import setuptools

VERSION = "1"

setuptools.setup(
    name="polygraphs",
    version=VERSION,
    description="PolyGraphs",
    long_description="",
    author="Alexandros Koliousis",
    author_email="ak@akoliousis.com",
    url="https://github.com/alexandroskoliousis/polygraphs",
    license="MIT",
    keywords="test test",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=["torch", "dgl", "notebook", "matplotlib", "PyYaml", "pandas"],
    python_requires=">=3",
    package_data={'polygraphs': ['logging.yaml']},
)

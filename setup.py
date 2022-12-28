""" zombpyg is a game in which you can program simple bots or train more complex agents, 
    which have to survive and fight against hordes of zombies
"""

import io
from os.path import dirname, join
from zombpyg import __version__

# Always prefer setuptools over distutils
from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


setup(
    name="zombpyg",
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,
    description="zombpyg is a programming game, where player bots or agents cooperate against zombie hordes",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/jvstinian/zombpyg",
    # This should be your name or the name of the organization which owns the project.
    author="jvstinian",
    author_email="jvstinian@gmail.com",
    # Classifiers help users find your project by categorizing it.
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: pygame",
        "License :: Other/Proprietary License", # Using this as no license provided
        "Programming Language :: Python :: 3",
    ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="game programming_game",  
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.6",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://caremad.io/posts/2013/07/setup-vs-requirement/
    install_requires=[
        "numpy",
        "gym",
        "pygame"
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={"dev": [], "test": []},
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    package_data={  # Optional
        "zombpyg": [],
    },
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'zombpyg=zombpyg.play:main',
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/jvstinian/zombpyg/issues",
        "Source": "https://github.com/jvstinian/zombpyg",
    },
)

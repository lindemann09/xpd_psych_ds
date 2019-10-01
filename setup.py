#!/usr/bin/env python3
"""
Installer
"""

from setuptools import setup
import codecs
import os
from sys import version_info as _vi

import xpd_psych_ds

package_name = "xpd_psych_ds"

install_requires = []

if _vi.major< 1:
    raise RuntimeError("{0} requires Python 3 or larger.".format(package_name))

def readme():
    directory = os.path.dirname(os.path.join(
        os.getcwd(), __file__, ))
    with codecs.open(
        os.path.join(directory, "README.md"),
        encoding="utf8",
        mode="r",
        errors="replace",
        ) as file:
        return file.read()


if __name__ == '__main__':

    setup(
        name = package_name,
        version=xpd_psych_ds.__version__,
        description=xpd_psych_ds.description,
        author="Oliver Lindemann",
        author_email='oliver@expyriment.org',
        license='MIT Licence',
        url='http://expyriment.github.io/DIF',
        packages=[package_name],
        package_data={'': ['specs/*']},
        include_package_data=True,
        setup_requires=[],
        install_requires=install_requires,
        entry_points={
            'console_scripts': ['xpd_psych_ds={0}.cli:run'.format(
                package_name)],
            },
        keywords = "", #ToDo
        classifiers=[ #ToDO
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering"
        ],
        long_description=readme(),
        long_description_content_type='text/markdown'
    )

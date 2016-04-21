"""Setup for Office Video XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-officevideo',
    version='0.6',
    description='Office Video XBlock for adding videos from Office 365 Video to courseware',
    packages=[
        'officevideo',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'officevideo = officevideo:OfficeVideoXBlock',
        ]
    },
    package_data=package_data("officevideo", ["static", "public"]),
)

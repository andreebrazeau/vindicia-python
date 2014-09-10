from setuptools import setup
import os.path
import re

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as README:
    DESCRIPTION = README.read()

VERSION_RE = re.compile("^__version__ = '(.+)'$",
                        flags=re.MULTILINE)
with open(os.path.join(os.path.dirname(__file__),
                       'vindicia', '__init__.py')) as PACKAGE:
    VERSION = VERSION_RE.search(PACKAGE.read()).group(1)

more_install_requires = list()
try:
    import ssl
except ImportError:
    more_install_requires.append('ssl')

requires = [
    'suds-jurko',
    ]

tests_require = [
    'nose',
    'mock',
    ]

setup(
    name='vindicia',
    version=VERSION,
    description="A python client wrapper to the Vindicia api.",
    long_description=DESCRIPTION,
    author='Andree Brazeau',
    author_email='andreebrazeau@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=['vindicia'],
    install_requires=requires,
    tests_require=tests_require,
    test_suite='unittest2.collector',
    zip_safe=True,
)

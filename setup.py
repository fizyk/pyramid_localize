"""pyramid_localize installation file."""

import os
from setuptools import setup, find_packages

here = os.path.dirname(__file__)


def read(fname):
    """Read file (fname)."""
    return open(os.path.join(here, fname)).read()


requirements = [
    'pyramid_basemodel',
    'tzf.pyramid_yml >=0.2',
    'pyramid >=1.5a1',
    'pyramid_mako',
    'pycountry>=16.11.08'  # major api change since 1.20
]

test_requires = [
    'pytest>=3.3.0',
    'pytest-pyramid>=0.3.1',
    'pytest-cov>=2.6.0',
    'mock>=2.0.0'
]

extras_require = {
    'docs': ['sphinx'],
    'tests': test_requires,
    'babel': ['Babel >= 1.0']
}

setup(
    name='pyramid_localize',
    version='0.1.0',
    description='''Package to provide translation methods for pyramid,
        and means to reload translations without stopping the application''',
    long_description=(
        read('README.rst') + '\n\n' + read('CHANGES.rst')
    ),
    keywords='python template',
    author='Grzegorz Sliwinski',
    author_email='username: fizyk, domain: fizyk.net.pl',
    url='https://github.com/fizyk/pyramid_localize',
    license="MIT License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requires,
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,
    message_extractors={'pyramid_localize': [
                          ('**.py', 'python', None),
                          ('resources/templates/**.mako', 'mako', None),
                          ('resources/static/**', 'ignore', None)]},
    extras_require=extras_require,
)

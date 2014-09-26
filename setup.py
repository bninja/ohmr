import re
import setuptools


setuptools.setup(
    name='ohmr',
    version=(
        re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open('ohmr.py').read())
        .group(1)
    ),
    url='https://github.com/bninja/ohmr',
    license='BSD',
    author='deepak',
    author_email='deepak@chopra.in',
    description='Ids for guru meditation.',
    long_description=open('README.rst').read(),
    py_modules=['ohmr'],
    include_package_data=True,
    platforms='any',
    install_requires=[
    ],
    extras_require={
        'tests': [
            'coid >=0.1,<0.2',
            'pytest >=2.5.2,<3',
            'pytest-cov >=1.7,<2',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

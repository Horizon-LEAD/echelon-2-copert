"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

import pathlib
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='e2c',
    version='1.0.0',
    description='Echelon to COPERT connector',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/inlecom/lead/models/echelon-to-copert-connector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='lead, development, echelon, copert, connector',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=[
        'python-dotenv',
        'XlsxWriter'
    ],
    entry_points={
        'console_scripts': [
            'e2c=e2c.__main__:main'
        ],
    },
    project_urls={
        'Source': 'https://gitlab.com/inlecom/lead/models/echelon-to-copert-connector',
        'Issues': 'https://gitlab.com/inlecom/lead/models/echelon-to-copert-connector/issues',
    },
)

from setuptools import setup, find_packages
from shapeshift_cli import __version__

setup(
	name ='shapeshift-cli',
    version = __version__,
    description = 'Unofficial CLI for https://shapeshift.io',
    url = 'https://github.com/sereneblue/shapeshift-cli',
    author = 'sereneblue',
    license = "Apache",
    packages = find_packages(exclude=['docs', 'tests*']),
    classifiers = [
		'Intended Audience :: Developers',
		'Environment :: Console',
		'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
    ],
    keywords = ['bitcoin', 'litecoin', 'cryptocurrency', 'shapeshift cli'],
    install_requires = ['requests', 'docopt'],
    entry_points = {
    	'console_scripts':[
    		'shapeshift-cli=shapeshift_cli.__main__:main'
    	],
    }
)

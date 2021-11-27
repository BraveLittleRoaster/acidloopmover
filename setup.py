from setuptools import setup

DEPENDENCIES = open('requirements.txt', 'r').read().split('\n')
README = open('README.md', 'r').read()

setup(
    name='acidloopmover',
    version='1.0.0',
    description='Move ACID LOOP WAV files from one directory to another.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='HexOffender',
    author_email='robert.paul6@gmail.com',
    url="http://github.com/BraveLittleRoaster/",
    packages=['src'],
    entry_points={
        'console_scripts': ['acidloopmover = src.main:main']
    },
    install_requires=DEPENDENCIES,
    keywords=['Acid Loop WAV', 'WAV', 'File Utility'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
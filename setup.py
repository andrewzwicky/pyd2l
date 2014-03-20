from setuptools import setup, find_packages

setup(
    name='pyd2l',
    version='0.1',
    license='MIT',
    author='Andrew Zwicky',
    install_requires=['beautifulsoup4>=3.2.1','coverage >= 3.7.1', 'nose >= 1.3.0', 'matplotlib >= 1.3.1'],
    description='Data analysis of Dota2Lounge bets to determine betting strategies.',
    long_description=open('README.md').read(),
    packages=find_packages(),
    platforms='any',
    classifiers = [
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities'
        ]
)

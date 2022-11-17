from setuptools import setup, find_packages

setup(
    name='Safepass',
    version='0.1.0',
    packages=find_packages(include=['safepass', 'safepass.*']),
    install_requires=[

    ],
    entry_points={
        'console_scripts': ['safepass=safepass.entry:main']
    }
)
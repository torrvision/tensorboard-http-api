from setuptools import setup

setup(
    name='lapiz',
    description='Lapiz server',
    author='bosr',
    url='https://github.com/bosr/lapiz',
    packages=['lapiz', 'lapiz.blueprints'],
    version='0.5',
    install_requires=[
        "requests",
        "flask"
    ]
)

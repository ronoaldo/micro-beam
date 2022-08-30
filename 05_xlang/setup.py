import setuptools

# Esse arquivo permite executar o pipeline com todas as
# dependências do seu módulo Python.
# https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/#multiple-file-dependencies
setuptools.setup(
    name='micro-beam',
    version='0.1',
    install_requires=[],
    packages=setuptools.find_packages(),
)

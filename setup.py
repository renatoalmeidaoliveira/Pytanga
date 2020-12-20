import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytanga", # Replace with your own username
    version="0.0.1",
    author="Renato Almeida de Oliveira",
    author_email="renato.almeida.oliveira@gmail.com",
    description="Python Library to simplify NETCONF payload creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/renatoalmeidaoliveira/Pytanga-dev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

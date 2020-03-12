import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Roadnoise",  # Replace with your own username
    version="1.0.0",
    author="Hsin-Mao Wu",
    author_email="hsinmao@maoshouse.com",
    description="A project to measure sound pressure levels at geographic locations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.maoshouse.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

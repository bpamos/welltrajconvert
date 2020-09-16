import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="welltrajconvert",
    version="0.0.3",
    author="Brandon Amos",
    author_email="bpamosconsulting@gmail.com",
    description="Well Trajectory Conversion",
    url="https://github.com/bpamos/directional-survey-converter",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=['pandas', 'numpy>=1.19.2', 'pathlib>=1.0.1', 'dataclasses>=0.7', 'matplotlib', 'scipy']
)
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

entry_points = {
    'console_scripts': [
        'caniobserve = caniobserve.caniobserve_exe:cli'
    ]
}

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

version_dict = {}
with open("caniobserve/_version.py") as fp:
    exec(fp.read(), version_dict)
setuptools.setup(
    name='caniobserve',
    version=version_dict["__version__"],
    author='Bryan Brzycki',
    author_email='bbrzycki@berkeley.edu',
    description='Observability utilies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points=entry_points,
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)

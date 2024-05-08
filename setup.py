import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='akgeomorph',
    version='0.1.5',
    author='Timm Nawrocki',
    author_email='twnawrocki@alaska.edu',
    description='Functions for calculation of geomorphology metrics for Alaska.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/accs-uaa/akgeomorph',
    project_urls = {
        "Bug Tracker": "https://github.com/accs-uaa/akgeomorph/issues"
    },
    license='MIT',
    packages=['akgeomorph'],
    install_requires=['requests'],
)

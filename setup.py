import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="faker_clickstream",
    version="0.1.0",
    author="Christos Natsis",
    author_email="christos_na@hotmail.com",
    description="Clickstream Faker Provider for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cnatsis/faker-clickstream",
    project_urls={
        "Issues Tracker": "https://github.com/cnatsis/faker-clickstream/issues",
    },
    install_requires=['Faker'],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    packages=["faker_clickstream"],
    python_requires=">=3.6",
    license='Apache License, Version 2.0',
)

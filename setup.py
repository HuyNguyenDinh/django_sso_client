from setuptools import setup, find_packages

setup(
    name='django_sso_client',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Django',
        'djangorestframework',
        'djangorestframework-simplejwt',
        'Authlib',
    ],
    include_package_data=True,
)
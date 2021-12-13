from setuptools import setup, find_packages


setup(
    name='django-staticfiles-vite',
    version='0.3.0',
    description='',
    url='https://github.com/jorrete/django-staticfiles-vite/',
    author='Jorge Rodríguez-Flores Esparza',
    author_email='jorrete@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django >= 4.0.0',
    ],
    extras_require={
        'dev': [
            'bump2version',
        ]
    },
    zip_safe=False
)

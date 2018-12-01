import setuptools

from gpuview import __version__


def read_readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name='gpuview',
    version=__version__,
    license='MIT',
    description='A lightweight web dashboard for monitoring GPU usage',
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/fgaim/gpuview',
    author='Fitsum Gaim',
    author_email='fitsum@geezlab.com',
    keywords='gpu web-monitoring',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
    ],
    packages=['gpuview'],
    install_requires=['gpustat>=0.5.0', 'bottle>=0.12.14'],
    extras_require={'test': ['pytest']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gpuview=gpuview.app:main',
        ],
    },
    include_package_data=True,
    zip_safe=True,
)

from distutils.core import setup

setup(name='DukeD3MWrapper',
    version='1.1.1',
    description='A wrapper for integrating Duke into the D3M environment',
    packages=['DukeD3MWrapper'],
    install_requires=["numpy",
        "requests",
        "typing",
        "Duke==1.2.0"],
    dependency_links=[
        "git+https://github.com/NewKnowledge/duke@447ad1609086059940c2d1b611cd05373cc33cf2#egg=Duke-1.2.0"
    ],
    entry_points = {
        'd3m.primitives': [
            'distil.duke = DukeD3MWrapper:duke'
        ],
    },
)
from distutils.core import setup

setup(name='DukeD3MWrapper',
    version='1.1.0',
    description='A wrapper for integrating Duke into the D3M environment',
    packages=['DukeD3MWrapper'],
    install_requires=["numpy",
        "requests",
        "typing",
        "Duke==1.2.0"],
    dependency_links=[
        "git+https://github.com/NewKnowledge/duke@88b76798b40c751680946959342d1835ca864508#egg=Duke-1.2.0"
    ],
    entry_points = {
        'd3m.primitives': [
            'distil.duke = DukeD3MWrapper:duke'
        ],
    },
)
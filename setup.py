from distutils.core import setup

setup(name='DukeD3MWrapper',
    version='1.1.0',
    description='A wrapper for integrating Duke into the D3M environment',
    packages=['DukeD3MWrapper'],
    install_requires=["numpy",
        "pandas",
        "requests",
        "typing",
        "gensim",
        "Duke==1.1.0"],
    dependency_links=[
        "git+https://github.com/NewKnowledge/duke-d3m-wrapper@592cb95aadffcbaa6d87a3f14252726fee3a3ff6#egg=Duke-1.1.0"
    ],
    entry_points = {
        'd3m.primitives': [
            'distil.duke = DukeD3MWrapper:duke'
        ],
    },
)
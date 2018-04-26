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
        "git+https://github.com/NewKnowledge/duke@944605ea156bcdccfa0279241cb056302c26c733#egg=Duke-1.1.0"
    ],
    entry_points = {
        'd3m.primitives': [
            'distil.duke = DukeD3MWrapper:duke'
        ],
    },
)
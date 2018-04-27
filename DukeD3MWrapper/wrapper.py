import os.path
import numpy as np
import pandas
import pickle
import requests
import ast
import typing
from json import JSONDecoder
from typing import List

from Duke.agg_functions import *
from Duke.dataset_descriptor import DatasetDescriptor
from Duke.utils import mean_of_rows

from d3m.primitive_interfaces.base import PrimitiveBase, CallResult

from d3m import container, utils
from d3m.metadata import hyperparams, base as metadata_base, params

__author__ = 'Distil'
__version__ = '1.1.0'

Inputs = container.pandas.DataFrame
Outputs =container.List[str]

class Params(params.Params):
    pass


class Hyperparams(hyperparams.Hyperparams):
    pass

class duke(PrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    metadata = metadata_base.PrimitiveMetadata({
        # Simply an UUID generated once and fixed forever. Generated using "uuid.uuid4()".
        'id': "46612a42-6120-3559-9db9-3aa9a76eb94f",
        'version': __version__,
        'name': "duke",
        # Keywords do not have a controlled vocabulary. Authors can put here whatever they find suitable.
        'keywords': ['Dataset Descriptor'],
        'source': {
            'name': __author__,
            'uris': [
                # Unstructured URIs.
                "https://github.com/NewKnowledge/duke-d3m-wrapper",
            ],
        },
        # A list of dependencies in order. These can be Python packages, system packages, or Docker images.
        # Of course Python packages can also have their own dependencies, but sometimes it is necessary to
        # install a Python package first to be even able to run setup.py of another package. Or you have
        # a dependency which is not on PyPi.
         'installation': [{
            'type': metadata_base.PrimitiveInstallationType.PIP,
            'package_uri': 'git+https://github.com/NewKnowledge/duke-d3m-wrapper.git@{git_commit}#egg=DukeD3MWrapper'.format(
                git_commit=utils.current_git_commit(os.path.dirname(__file__)),
            ),
         },
        ],
        # The same path the primitive is registered with entry points in setup.py.
        'python_path': 'd3m.primitives.distil.duke',
        # Choose these from a controlled vocabulary in the schema. If anything is missing which would
        # best describe the primitive, make a merge request.
        'algorithm_types': [
            metadata_base.PrimitiveAlgorithmType.RECURRENT_NEURAL_NETWORK,
        ],
        'primitive_family': metadata_base.PrimitiveFamily.DATA_CLEANING,
    })
    
    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0)-> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)
                
        self._decoder = JSONDecoder()
        self._params = {}

    def fit(self) -> None:
        pass
    
    def get_params(self) -> Params:
        return self._params

    def set_params(self, *, params: Params) -> None:
        self.params = params

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        pass
        
    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:
        """
        Produce a summary for the tabular dataset input
        
        Parameters
        ----------
        inputs : Input pandas frame
        Returns
        -------
        Outputs
            The output is a string summary
        """
        
        """ Accept a pandas data frame, returns a string summary
        frame: a pandas data frame containing the data to be processed
        -> a string summary
        """
        
        frame = inputs

        try:
            dataset_path='/vectorizationdata/KnowledgeGraph2Vec/duke-dev/data/185_baseball.csv'
            tree_path='../ontologies/class-tree_dbpedia_2016-10.json'
            embedding_path='/vectorizationdata/KnowledgeGraph2Vec/duke-dev/embeddings/wiki2vec/en.model'
            row_agg_func=mean_of_rows
            tree_agg_func=parent_children_funcs(np.mean, max)
            source_agg_func=mean_of_rows
            max_num_samples = 1e6
            verbose=True

            duke = DatasetDescriptor(
                dataset=dataset_path,
                tree=tree_path,
                embedding=embedding_path,
                row_agg_func=row_agg_func,
                tree_agg_func=tree_agg_func,
                source_agg_func=source_agg_func,
                max_num_samples=max_num_samples,
                verbose=verbose,
                )

            print('initialized duke dataset descriptor \n')

            return duke.get_dataset_description()

        except:
            return "Failed summarizing data frame"


if __name__ == '__main__':
    client = duke(hyperparams={})
    # frame = pandas.read_csv("https://query.data.world/s/10k6mmjmeeu0xlw5vt6ajry05",dtype='str')
    frame = pandas.read_csv("https://s3.amazonaws.com/d3m-data/merged_o_data/o_4550_merged.csv",dtype='str')
    result = client.produce(inputs = frame)
    print(result)
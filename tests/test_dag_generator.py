import pytest 
import os  
from pathlib import Path
from dagfactory.dag_generator import DagGenerator
from dagfactory.dagfactory import DagFactory
from dagfactory.utils import transform_config, merge_defaults, merge_defaults_updated

dag_config_path="fixtures/dag_factory_task_group.yml"
here = os.path.dirname(__file__)

def get_full_pah(path: str):
    return os.path.join(here, dag_config_path)

@pytest.fixture(scope="session")
def dag_generator():
    full_path=get_full_pah(dag_config_path)
    generator=DagGenerator(config_path=full_path)
    
    yield(generator)

def test_dag_config(dag_generator):
    
    assert dag_generator.dag_factory.config is not None 
    
def test_dag_generator_generate_dags(dag_generator):
    
    dags = dag_generator.generate_dags()
    
    assert dags is not None 
    
def test_transform_config(dag_generator):
    
    config = dag_generator.dag_factory.config
    # merged_config = merge_defaults_updated(config)
    transformed_config = transform_config(config)
    
    assert transformed_config is not None 
    
    
def test_merge_config(dag_generator):
    
    config = dag_generator.dag_factory.config
    merged_config = merge_defaults(config)
    
    assert merged_config is not None
    
    
def test_merge_config_updated(dag_generator):
    
    config = dag_generator.dag_factory.config
    merged_config = merge_defaults_updated(config)
    
    assert merged_config is not None
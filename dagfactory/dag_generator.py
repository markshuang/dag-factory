from dagfactory.dagfactory import DagFactory
from dagfactory.dagbuilder import DagBuilder 
from airflow.models import DAG
from dagfactory.exceptions import DagFactoryException
from typing import Any, Dict, List, Optional, Union 


from jinja2 import Environment, FileSystemLoader
import logging
import yaml
import json
from datetime import date

logging.basicConfig(
    format='%(name)s - %(asctime)s - %(levelname)s - %(message)s', 
    level=logging.DEBUG
)

class DagGenerator:
    
    def __init__(
        self, 
        config_path: Optional[str] = None,
        config: Optional[Dict] = None) -> None:
        
        self.dag_factory = DagFactory(
            config_filepath=config_path,
            config=config
        )
    
    
    def generate_dags(self):
        
        dag_configs: Dict[str, Dict[str, Any]] = self.dag_factory.get_dag_configs()
        default_config: Dict[str, Any] = self.dag_factory.get_default_config()

        dags: Dict[str, Any] = {}

        for dag_name, dag_config in dag_configs.items():
            dag_config["task_groups"] = dag_config.get("task_groups", {})
            dag_builder: DagBuilder = DagBuilder(
                dag_name=dag_name,
                dag_config=dag_config,
                default_config=default_config,
            )
            try:
                dag: Dict[str, Union[str, DAG]] = dag_builder.build()
                dags[dag["dag_id"]]: DAG = dag["dag"]
            except Exception as err:
                raise DagFactoryException(
                    f"Failed to generate dag {dag_name}. verify config is correct"
                ) from err

        return dags
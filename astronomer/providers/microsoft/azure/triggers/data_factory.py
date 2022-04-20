from typing import AsyncIterator, Tuple, Dict, Any

from airflow.triggers.base import BaseTrigger, TriggerEvent
from astronomer.providers.microsoft.azure.hooks.data_factory import AzureDataFactoryHookAsync


class AzureDataFactoryTrigger(BaseTrigger):

    def __init__(
            self,
            run_id: str,
            wait_for_termination: bool,
            resource_group_name: str,
            factory_name: str,
            check_interval: int = 60,
            azure_data_factory_conn_id: str = "azure_data_factory_default",
    ):
        self.azure_data_factory_conn_id = azure_data_factory_conn_id
        self.run_id = run_id
        self.wait_for_termination = wait_for_termination
        self.resource_group_name = resource_group_name
        self.factory_name = factory_name

    def serialize(self) -> Tuple[str, Dict[str, Any]]:
        """Serializes AzureDataFactoryTrigger arguments and classpath."""
        return (
            "astronomer.providers.microsoft.azure.triggers.data_factory.AzureDataFactoryTrigger",
            {
                "azure_data_factory_conn_id": self.azure_data_factory_conn_id,
                "run_id": self.run_id,
                "wait_for_termination": self.wait_for_termination,
            },
        )

    async def run(self) -> AsyncIterator["TriggerEvent"]:
        if not self.wait_for_termination:
            yield TriggerEvent(
                {
                    "status": "success",
                    "message": "",
                    "run_id": self.run_id,
                }
            )
            return
        hook = AzureDataFactoryHookAsync(azure_data_factory_conn_id=self.azure_data_factory_conn_id)
        while True:
            status = hook.get_pipeline_run_status(self.run_id, self.resource_group_name, self.factory_name)
            if

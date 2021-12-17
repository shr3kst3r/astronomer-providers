from airflow.providers.databricks.operators.databricks import (
    XCOM_RUN_ID_KEY,
    XCOM_RUN_PAGE_URL_KEY,
    DatabricksRunNowOperator,
    DatabricksSubmitRunOperator,
)

from astronomer_operators.databricks.triggers.databricks import DatabricksTrigger


class DatabricksSubmitRunOperatorAsync(DatabricksSubmitRunOperator):
    def execute(self, context):
        """
        Logic that the operator uses to execute the Databricks trigger,
        and defer execution as expected. It makes two non-async API calls to
        submit the run, and retrieve the run page URL. It also pushes these
        values as xcom data if do_xcom_push is set to True in the context.
        """
        # Note: This hook makes non-async calls.
        # It is imported from the Databricks base class.
        # Async calls (i.e. polling) are handled in the Trigger.
        hook = self._get_hook()
        self.run_id = hook.submit_run(self.json)

        if self.do_xcom_push:
            context["ti"].xcom_push(key=XCOM_RUN_ID_KEY, value=self.run_id)
        self.log.info("Run submitted with run_id: %s", self.run_id)
        self.run_page_url = hook.get_run_page_url(self.run_id)
        if self.do_xcom_push:
            context["ti"].xcom_push(key=XCOM_RUN_PAGE_URL_KEY, value=self.run_page_url)

        self.log.info("View run status, Spark UI, and logs at %s", self.run_page_url)

        self.defer(
            timeout=self.execution_timeout,
            trigger=DatabricksTrigger(
                conn_id=self.databricks_conn_id,
                task_id=self.task_id,
                run_id=self.run_id,
                retry_limit=self.databricks_retry_limit,
                retry_delay=self.databricks_retry_delay,
                polling_period_seconds=self.polling_period_seconds,
            ),
            method_name="execute_complete",
        )

    def execute_complete(self, context, event=None):  # pylint: disable=unused-argument
        """
        Callback for when the trigger fires - returns immediately.
        Relies on trigger to throw an exception, otherwise it assumes execution was
        successful.
        """
        self.log.info("%s completed successfully.", self.task_id)
        return None


class DatabricksRunNowOperatorAsync(DatabricksRunNowOperator):
    def execute(self, context):
        """
        Logic that the operator uses to execute the Databricks trigger,
        and defer execution as expected. It makes two non-async API calls to
        submit the run, and retrieve the run page URL. It also pushes these
        values as xcom data if do_xcom_push is set to True in the context.
        """
        # Note: This hook makes non-async calls.
        # It is from the Databricks base class.
        hook = self._get_hook()
        self.run_id = hook.run_now(self.json)

        if self.do_xcom_push:
            context["ti"].xcom_push(key=XCOM_RUN_ID_KEY, value=self.run_id)
        self.log.info("Run submitted with run_id: %s", self.run_id)
        self.run_page_url = hook.get_run_page_url(self.run_id)
        if self.do_xcom_push:
            context["ti"].xcom_push(key=XCOM_RUN_PAGE_URL_KEY, value=self.run_page_url)

        self.log.info("View run status, Spark UI, and logs at %s", self.run_page_url)

        self.defer(
            timeout=self.execution_timeout,
            trigger=DatabricksTrigger(
                task_id=self.task_id,
                conn_id=self.databricks_conn_id,
                run_id=self.run_id,
                retry_limit=self.databricks_retry_limit,
                retry_delay=self.databricks_retry_delay,
                polling_period_seconds=self.polling_period_seconds,
            ),
            method_name="execute_complete",
        )

    def execute_complete(self, context, event=None):  # pylint: disable=unused-argument
        """
        Callback for when the trigger fires - returns immediately.
        Relies on trigger to throw an exception, otherwise it assumes execution was
        successful.
        """
        self.log.info("%s completed successfully.", self.task_id)
        return None
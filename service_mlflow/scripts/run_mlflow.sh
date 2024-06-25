mlflow server --backend-store-uri ${BACKEND_STORE_URI} \
              --default-artifact-root ${DEFAULT_ARTIFACT_ROOT} \
              --artifacts-destination ${DEFAULT_ARTIFACTS_DESTINATION} \
              --no-serve-artifacts \
              --host 0.0.0.0 \
              --port ${MLFLOW_CONTAINER_PORT}

def call(String script, String resultDir, String VENV_DIR) {
    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
        sh """
        ${script} --junitxml=${resultDir}.xml
        """
    }
}


def runScript(String script, String resultdir) {
    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
        sh """
        source ${VENV_DIR}/bin/activate
        ${script} --junitxml=${resultdir}.xml
        """
    }
}

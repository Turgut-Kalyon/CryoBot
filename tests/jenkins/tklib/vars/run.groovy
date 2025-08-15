
def call(String script, String resultDir) {
    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
        sh """
        ${script} --junitxml=${resultDir}.xml
        """
    }
}


/**
 * Runs a Python script in a virtual environment.
 *
 * @param script The Python script to run.
 * @param resultDir The directory where the results will be stored.
 */
def call(String script, String resultDir) {
    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
        sh """
        python3 -m venv .venv
        . .venv/bin/activate
        pip install -r requirements.txt
        ${script} --junitxml=${resultDir}.xml
        deactivate
        """
    }
}
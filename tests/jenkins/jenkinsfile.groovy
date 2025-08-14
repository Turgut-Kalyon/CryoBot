
def runScript(String script, String resultDir, String VENV_DIR) {
    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
        sh """
        ${script} --junitxml=${resultDir}.xml
        """
    }
}

pipeline{
    agent any
    environment {
        BUILD_DIR = "${WORKSPACE}/tests"
        UNIT_TEST_SCRIPT = "pytest -v ${BUILD_DIR}/test_unittest.py::TestUnitStorage"
        RESULT_DIR = "${WORKSPACE}/results"
    }

    stages{


        stage('Checkout repository') {
            steps {
                checkout scm
            }
        }

        stage('Run unit tests: storage') {
            steps {
                script {
                    def resultdir = env.RESULT_DIR + "/Test_unittests_storage"
                    runScript(env.UNIT_TEST_SCRIPT, resultdir, env.VENV_DIR)
                }
            }
        }
    }
    post {
        always {
            junit **/results/Test_*.xml
        }
        success {
            echo 'Unit tests completed successfully.'
        }
        failure {
            echo 'Unit tests failed.'
        }
    }
}


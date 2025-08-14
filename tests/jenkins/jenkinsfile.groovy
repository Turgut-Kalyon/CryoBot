
def runScript(String script, String resultDir, String VENV_DIR) {
    sh """
    ${script} --junitxml=${resultDir}/unittest_results.xml
    """
}

pipeline{
    agent any
    environment {
        BUILD_DIR = "${WORKSPACE}/tests"
        UNIT_TEST_SCRIPT = "pytest -v ${BUILD_DIR}/test_unittest.py::UnitTest"
        RESULT_DIR = "/results/"
    }

    stages{


        stage('Checkout repository') {
            steps {
                checkout scm
            }
        }

        stage('Run unit tests') {
            steps {
                script {
                    def resultdir = env.RESULT_DIR + "unittests"
                    runScript(env.UNIT_TEST_SCRIPT, resultdir, env.VENV_DIR)
                }
            }
        }
    }
    post {
        always {
            junit "${RESULT_DIR}/unittest_results.xml"
        }
        success {
            echo 'Unit tests completed successfully.'
        }
        failure {
            echo 'Unit tests failed.'
        }
    }
}


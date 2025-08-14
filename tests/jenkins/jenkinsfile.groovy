pipeline{
    agent any

    environment {
        // Define any environment variables here
        BUILD_DIR = "${WORKSPACE}/tests"
        UNIT_TEST_SCRIPT = "pytest -v tests/unittests.py::UnitTest"
        RESULT_DIR = "/results/"
    }

    stages{
        stage('Checkout repository') {
            steps {
                // Checkout the repository
                checkout scm
            }
        }

        stage('Run unit tests') {
            steps {
                script {
                    sh "${UNIT_TEST_SCRIPT} --junitxml=${env.RESULT_DIR}/unittest_results.xml"
                }
            }
        }
    }
    post {
        always {
            // Archive the test results
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
pipeline{
    agent {
        docker{image 'python:3.13'}
    }
    environment {
        BUILD_DIR = "${WORKSPACE}/tests"
        UNIT_TEST_SCRIPT = "pytest -v ${BUILD_DIR}/unittests.py::UnitTest"
        RESULT_DIR = "/results/"
    }
    options {
        timestamps()
        ansicolor('xterm')
    }

    stages{

        stage('Preparation'){
            steps{
                script{
                    sh '''
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Checkout repository') {
            steps {
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
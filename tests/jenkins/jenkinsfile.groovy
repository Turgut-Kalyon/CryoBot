pipeline{
    agent any

    environment {
        BUILD_DIR = "${WORKSPACE}/tests"
        UNIT_TEST_SCRIPT = "pytest -v tests/unittests.py::UnitTest"
        RESULT_DIR = "/results/"
    }



    stages{

        stage('Preparation'){
            steps{
                script{
                    sh '''
                    apt-get update
                    apt-get install -y python3 python3-pip 
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
@Library('tklib') _

pipeline{
    agent any
    environment {
        BUILD_DIR = "${WORKSPACE}/tests"
        Script_for_UnitTestStorage = "pytest -v ${BUILD_DIR}/unittests/test_unittest_Storage.py::TestUnitStorage"
        Script_for_UnitTestCoinTransfer = "pytest -v ${BUILD_DIR}/unittests/test_unittest_CoinTransfer.py::TestUnitCoinTransfer"
        Script_for_IntigrationTestCracc = "pytest -v ${BUILD_DIR}/Integrationtests/test_integrationtest_Cracc.py::TestCraccIntegration"
        RESULT_DIR = "${WORKSPACE}/results"
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        throttleConcurrentBuilds(maxTotal: 4, maxPerNode: 2)
    }
    stages{


        stage('Checkout repository') {
            steps {
                checkout scm
            }
        }

        stage('Run Unittests'){
            parallel{
                stage('Storage Unit Tests') {
                    steps {
                        script {
                            def resultdir = env.RESULT_DIR + "/Test_unittests_storage"
                            run(env.Script_for_UnitTestStorage, resultdir)
                        }
                    }
                }
                stage('CoinTransfer Unit Tests') {
                    steps {
                        script {
                            def resultdir = env.RESULT_DIR + "/Test_unittests_cointransfer"
                            run(env.Script_for_UnitTestCoinTransfer, resultdir)
                        }
                    }
                }
            }
        }


        stage('Run intigration tests') {
            steps {
                script {
                    def resultdir = env.RESULT_DIR + "/Test_integrationtest_cracc"
                    runInVenv(env.Script_for_IntigrationTestCracc, resultdir)
                }
            }
        }


    }
    post {
        always {
            junit "**/results/Test_*.xml"
            archiveArtifacts artifacts: '**/results/Test_*.xml', allowEmptyArchive: true
            echo 'Unit test results archived.'
        }
        success {
            echo 'Unit tests completed successfully.'
        }
        failure {
            echo 'Unit tests failed.'
        }
    }
}


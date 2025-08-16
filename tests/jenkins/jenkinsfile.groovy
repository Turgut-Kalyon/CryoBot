@Library('tklib') _

pipeline{
    agent any
    environment {
        BUILD_DIR = "${WORKSPACE}/tests"
        Script_for_UnitTestStorage = "pytest -v ${BUILD_DIR}/unittests/test_unittest_Storage.py::TestUnitStorage"
        Script_for_UnitTestCoinTransfer = "pytest -v ${BUILD_DIR}/unittests/test_unittest_CoinTransfer.py::TestUnitCoinTransfer"
        Script_for_IntigrationTestAccount = "pytest -v ${BUILD_DIR}/Integrationtests/test_integrationtest_accountcmd.py::TestAccountIntegration"
        Script_for_IntigrationTestDaily = "pytest -v ${BUILD_DIR}/Integrationtests/test_integrationtests_daily.py::TestDailyIntegration"
        Script_for_IntigrationTestCustomCmd = "pytest -v ${BUILD_DIR}/Integrationtests/test_integrationtest_customtxtcmd.py::TestCustomCmdIntegration"
        RESULT_DIR = "${WORKSPACE}/results"
    }

    stages{


        stage('Checkout repository') {
            steps {
                checkout scm
            }
        }

        stage('Prepare virtual environment') {
            steps {
                script {
                    sh """python3 -m venv .venv
                       . .venv/bin/activate
                       pip install -r requirements.txt
                       deactivate
                       """
                }
            }
        }

        stage('Run Unittests'){
            parallel{
                stage('Storage Unittests') {
                    steps {
                        script {
                            def resultdir = env.RESULT_DIR + "/Test_unittests_storage"
                            runInVenv(env.Script_for_UnitTestStorage, resultdir)
                        }
                    }
                }
                stage('CoinTransfer Unittests') {
                    steps {
                        script {
                            def resultdir = env.RESULT_DIR + "/Test_unittests_cointransfer"
                            runInVenv(env.Script_for_UnitTestCoinTransfer, resultdir)
                        }
                    }
                }
            }
        }


        stage('Run integration tests') {
            parallel {
                stage('AccountCommands integration tests') {
                    steps {
                        script {
                            def resultdir = env.RESULT_DIR + "/Test_integrationtest_cracc"
                            runInVenv(env.Script_for_IntigrationTestAccount, resultdir)
                        }
                    }
                }
                stage('DailyCommand integration tests') {
                    steps {
                        script {
                            def resultdir = env.RESULT_DIR + "/Test_integrationtest_daily"
                            runInVenv(env.Script_for_IntigrationTestDaily, resultdir)
                        }
                    }
                }
                stage('CustomCommand integration tests') {
                    steps {
                        script {
                            def resultdir = env.RESULT_DIR + "/Test_integrationtest_customcmd"
                            runInVenv(env.Script_for_IntigrationTestCustomCmd, resultdir)
                        }
                    }
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


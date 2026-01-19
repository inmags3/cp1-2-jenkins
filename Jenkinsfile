pipeline {
    agent none

    stages {
        stage('Checkout (principal)') {
            agent { label 'principal' }
            steps {
                checkout scm
                sh 'whoami; hostname; echo $WORKSPACE'
                stash name: 'src', includes: '**/*'
            }
        }

        stage('CI en paralelo') {
            parallel {
                stage('Tests + Coverage (agente1)') {
                    agent { label 'agente1' }
                    steps {
                        unstash 'src'
                        sh 'whoami; hostname; echo $WORKSPACE'
                        sh '''
                            set -e
                            python3 -m venv .venv_ci
                            . .venv_ci/bin/activate
                            pip install -U pip
                            pip install -r requirements.txt

                            mkdir -p reports
                            coverage run --branch -m pytest -q --junitxml=reports/junit.xml
                            coverage report -m
                            coverage xml -o coverage.xml
                        '''
                        stash name: 'junit', includes: 'reports/junit.xml'
                        stash name: 'cov', includes: 'coverage.xml'
                    }
                }

                stage('Static (flake8) (agente2)') {
                    agent { label 'agente2' }
                    steps {
                        unstash 'src'
                        sh 'whoami; hostname; echo $WORKSPACE'
                        sh '''
                            set -e
                            python3 -m venv .venv_ci
                            . .venv_ci/bin/activate
                            pip install -U pip
                            pip install -r requirements.txt

                            mkdir -p reports
                            # Si hay warnings, flake8 devuelve exit code != 0.
                            # Con "|| true" el pipeline no se cae y Warnings-NG puede mostrarlos.
                            flake8 app tests --format=pylint --output-file=reports/flake8.log || true
                        '''
                        stash name: 'flake8', includes: 'reports/flake8.log'
                    }
                }

                stage('Security + JMeter (agente3)') {
                    agent { label 'agente3' }
                    steps {
                        unstash 'src'
                        sh 'whoami; hostname; echo $WORKSPACE'
                        sh '''
                            set -e
                            python3 -m venv .venv_ci
                            . .venv_ci/bin/activate
                            pip install -U pip
                            pip install -r requirements.txt

                            mkdir -p reports

                            # Bandit: genera JSON para Warnings-NG
                            bandit -r app -f json -o reports/bandit.json || true

                            # Levantar API para que JMeter pueda atacar endpoints
                            python -m app.api >/tmp/flask.log 2>&1 &
                            API_PID=$!
                            sleep 2

                            # JMeter
                            jmeter -n -t tests/performance/plan.jmx -l jmeter-results.jtl

                            kill $API_PID || true
                        '''
                        stash name: 'bandit', includes: 'reports/bandit.json'
                        stash name: 'jmeter', includes: 'jmeter-results.jtl'
                    }
                }
            }
        }

        stage('Publish reports (principal)') {
            agent { label 'principal' }
            steps {
                unstash 'src'
                unstash 'junit'
                unstash 'cov'
                unstash 'flake8'
                unstash 'bandit'
                unstash 'jmeter'

                // JUnit (tendencia tests)
                junit allowEmptyResults: true, testResults: 'reports/junit.xml'

                // Coverage (tendencia cobertura)
                recordCoverage tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']]

                // Warnings-NG (flake8 + bandit)
                recordIssues tools: [flake8(pattern: 'reports/flake8.log')]
                recordIssues tools: [bandit(pattern: 'reports/bandit.json')]

                // Performance (JMeter)
                perfReport sourceDataFiles: 'jmeter-results.jtl'

                // Artefactos por si acaso
                archiveArtifacts artifacts: 'coverage.xml,reports/*,jmeter-results.jtl', allowEmptyArchive: true
            }
        }
    }
}



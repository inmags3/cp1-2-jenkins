pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                sh 'whoami'
                sh 'hostname'
                sh 'echo $WORKSPACE'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv_ci
                    . .venv_ci/bin/activate
                    pip install -U pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Tests') {
            steps {
                sh '''
                    . .venv_ci/bin/activate
                    pytest -q
                '''
            }
        }

        stage('Coverage') {
            steps {
                sh '''
                    . .venv_ci/bin/activate
                    coverage run --branch -m pytest
                    coverage report -m
                    coverage xml -o coverage.xml
                '''
            }
        }

        stage('Static analysis (flake8)') {
            steps {
                sh '''
                    . .venv_ci/bin/activate
                    flake8 app tests
                '''
            }
        }

        stage('Security scan (bandit)') {
            steps {
                sh '''
                    . .venv_ci/bin/activate
                    bandit -r app
                '''
            }
        }
	stage('Performance (JMeter)') {
	    steps {
		sh '''

	            . .venv_ci/bin/activate

            	    # Arrancamos la API en segundo plano
                    python -m app.api >/tmp/flask.log 2>&1 &
                    API_PID=$!

                    # Esperamos un momento a que levante
                    sleep 2

                    # Ejecutar JMeter usando el binario instalado (5.6.3)
		    /opt/jmeter/bin/jmeter -n -t tests/performance/plan.jmx -l jmeter-results.jtl

                    # Paramos la API
                    kill $API_PID || true
		'''
	    }
	}

    }

    post {
    always {
        archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
        archiveArtifacts artifacts: 'jmeter-results.jtl', fingerprint: true, allowEmptyArchive: true
	}
    }

}

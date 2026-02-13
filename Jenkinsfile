pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    VENV = ".venv"
    REPORTS_DIR = "reports"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup venv + deps') {
      steps {
        sh '''
          set -euxo pipefail

          export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

          which python3
          python3 --version

          python3 -m venv .venv

          . .venv/bin/activate
          python -m pip install --upgrade pip

          pip install "pylint==3.2.7" "pytest==8.3.2"
        '''
      }
    }

    stage('Lint (pylint)') {
      steps {
        sh '''
          set -euxo pipefail
          . .venv/bin/activate

          mkdir -p reports
          pylint src | tee reports/pylint.txt
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'reports/pylint.txt', fingerprint: true
        }
      }
    }

    stage('Unit Tests (pytest)') {
      steps {
        sh '''
          set -euxo pipefail
          . .venv/bin/activate

          mkdir -p reports
          pytest -q --junitxml=reports/junit.xml
        '''
      }
      post {
        always {
          junit 'reports/junit.xml'
          archiveArtifacts artifacts: 'reports/junit.xml', fingerprint: true
        }
      }
    }
  }

  post {
    always {
      script {
        currentBuild.description = "Branch: ${env.BRANCH_NAME}  PR: ${env.CHANGE_ID ?: '-'}"
      }
      cleanWs()
    }
  }
}

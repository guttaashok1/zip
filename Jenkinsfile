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

          echo "BRANCH_NAME=${BRANCH_NAME}  CHANGE_ID=${CHANGE_ID:-}"
          git rev-parse HEAD
          git log -1 --oneline

          # Prove the file content Jenkins is linting
          ls -la src
          grep -n "unused_var" -n src/common_library.py || true
          sed -n '1,120p' src/common_library.py

          # Prove what config pylint is using
          ls -la .pylintrc
          pylint --version

          mkdir -p reports
          pylint --rcfile=.pylintrc -rn -sn src/common_library.py | tee reports/pylint.txt
          exit ${PIPESTATUS[0]}
        '''
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

pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup venv + deps') {
      steps {
        sh '''
          set -euxo pipefail

          # Ensure python3 exists (macOS)
          which python3
          python3 --version

          # Create virtualenv
          python3 -m venv .venv

          # Activate venv
          . .venv/bin/activate

          # Upgrade pip + install tools
          python -m pip install --upgrade pip
          pip install pylint pytest
        '''
      }
    }

    stage('Lint (pylint)') {
      steps {
        sh '''
          set -euxo pipefail
          . .venv/bin/activate
          pylint src
        '''
      }
    }

    stage('Unit Tests (pytest)') {
      steps {
        sh '''
          set -euxo pipefail
          . .venv/bin/activate
          pytest -q
        '''
      }
    }
  }
}

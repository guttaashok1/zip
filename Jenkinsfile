pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Lint (pylint)') {
      steps {
        sh '''
          . .venv/bin/activate
          pylint src || true
        '''
      }
    }

    stage('Unit Tests (pytest)') {
      steps {
        sh '''
          . .venv/bin/activate
          pytest -q
        '''
      }
    }

  }
}

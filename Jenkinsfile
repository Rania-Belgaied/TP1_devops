pipeline {
    agent any

    // Déclenchement automatique à chaque push GitHub (webhook).
    // pollSCM sert de filet de sécurité si le webhook n'arrive pas (Jenkins en local).
    triggers {
        githubPush()
        pollSCM('H/2 * * * *')
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        IMAGE_NAME = 'rania02/counter-app'
        // Tag unique par build : le numéro de build
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --no-cache-dir -r app/requirements.txt
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    cd app
                    pytest -v --junitxml=../test-results.xml
                '''
            }
            post {
                always { junit allowEmptyResults: true, testResults: 'test-results.xml' }
            }
        }

        // Build + push uniquement sur la branche principale
        stage('Docker Build') {
            when {
                expression { (env.BRANCH_NAME ?: env.GIT_BRANCH) in ['main', 'origin/main', 'master', 'origin/master'] }
            }
            steps {
                sh '''
                    docker build -t $IMAGE_NAME:$IMAGE_TAG -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Docker Push') {
            when {
                expression { (env.BRANCH_NAME ?: env.GIT_BRANCH) in ['main', 'origin/main', 'master', 'origin/master'] }
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push $IMAGE_NAME:$IMAGE_TAG
                        docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }
    }

    post {
        always  { sh 'docker logout || true' }
        success { echo "Image publiée : ${IMAGE_NAME}:${IMAGE_TAG} (et :latest)" }
        failure { echo 'Pipeline en échec : voir les logs de l\'étape concernée.' }
    }
}
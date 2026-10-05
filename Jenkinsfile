pipeline {
    // exécute le pipeline sur n'importe quel exécuteur disponible. ici: le conteneur jenkins
    agent any


    // Quand le pipeline démarre-t-il ?
    triggers {
        //démarre dès que Github envoie le webhook après un git push.
        githubPush()
        //secours: jenkins interroge lui-meme GitHub toutes les 2 minutes et lence un build s'il y a un nouveau commit.
        pollSCM('H/2 * * * *')
    }

    //variables disponibles dans toutes les étapes.
    environment {
        IMAGE_NAME = 'rania02/counter-app'
    }

    stages {

        //Etape 1: préparer l'environnement python
        stage('Install Dependencies') {
            steps {
                //crée un env virtuel, l'active et installe les dépendances.
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r app/requirements.txt
                '''
            }
        }


        //Etape 2: tests unitaires avec pytest
        stage('Unit Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    cd app
                    pytest -v
                '''
            }
        }


        //Etape 3: Construire l'image docker à partir du dockerfile
        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }


        //Etape 4: publier l'image sur docker hub
        stage('Docker Push') {
            steps {
                //récupère l'identifiant dockerhub-credentials du coffre de jenkins.
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }
    }

    //Exécuté à la fin du pipeline, quel que soit le résultat.
    post {
        always { sh 'docker logout || true' }
    }
}
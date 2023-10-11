def DOCS_PUBLIC_PATH = "/var/lib/jenkins/userContent/dynolabs-docs"
def active_ocp_cloud = "shared-cluster-46a"

pipeline {

    parameters {
        choice(
            name: 'VersionBump',
            choices: ['NO', 'major', 'minor', 'patch'],
            description: 'Bump the version? (you still need to select Publish to push the new version to PyPI)'
        )
        booleanParam(
            name: 'Publish',
            defaultValue: false,
            description: 'Build, Publish the package to PyPI, and create the GitHub release'
        )
        booleanParam(
            name: 'VersionOverride',
            defaultValue: false,
            description: 'Override the existing package with that version if one already exists in PROD'
        )
    }

    environment {
        PATH = "/home/jenkins/.local/bin:$PATH"
    }

    agent none

    stages {

        stage("Install and Test") {
            matrix {
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '36', '38', '39', '310'
                    }
                }
                agent {
                    kubernetes{
                        yaml libraryResource("podTemplates/jenkins-agent-python-${PYTHON_VERSION}-pod.yaml")
                        cloud "${active_ocp_cloud}"
                    }
                }
                stages {
                    stage("Install") {
                        steps {
                            sh "pip install --upgrade pip"
                            // Integration tests use the tests/testcourse example project to define lab scripts
                            sh "pip install -e '.[git]'"
                            sh "pip install -e tests/testcourse"
                        }
                    }
                    stage("Lint") {
                        steps {
                            sh 'pip install pep8-naming'
                            sh 'make lint'
                        }
                    }
                    stage("Test") {
                        steps {
                            sh 'pip install -r requirements.tests.txt'
                            sh 'make test'
                        }
                    }
                }
            }
        }

        stage("Publish DEV (Stage only)") {
            agent {
                kubernetes{
                    yaml libraryResource("podTemplates/jenkins-agent-python-39-pod.yaml")
                    cloud "${active_ocp_cloud}"
                }
            }
            // Continous deployment to PyPI stage for PRs to "master"
            // It pushes versions numbered as X.Y.Z.dev{BRANCH_NAME}
            when {
                changeRequest target: 'master'
            }

            steps {
                sh "make DEV_VERSION=dev0+${env.BRANCH_NAME.toLowerCase().replaceAll('-','.')} build-dev"

                // Publish to stage
                withCredentials([
                    usernamePassword(
                        credentialsId: 'pypi-stage-uploader',
                        usernameVariable: 'PYPI_USERNAME',
                        passwordVariable: 'PYPI_PASSWORD'
                    )
                ]) {
                    sh "PS_PASSWD='${PYPI_PASSWORD}' make PYPI_USER=${PYPI_USERNAME} publish-stage"
                }
            }
        }

        stage("Bump Version") {
            agent {
                kubernetes{
                    yaml libraryResource("podTemplates/jenkins-agent-python-39-pod.yaml")
                    cloud "${active_ocp_cloud}"
                }
            }
            when {
                beforeAgent true
                allOf {
                    branch "master";
                    expression { params.VersionBump != "NO" }
                }
            }

            steps {
                sh 'pip install bump2version==1.0.1'
                withCredentials([usernamePassword(
                    credentialsId: 'github-bot-account',
                    usernameVariable: 'GIT_USERNAME',
                    passwordVariable: 'GIT_PASSWORD'
                )]) {
                    sh 'git config --global user.email "jenkins@jenkins.prod.nextcle.com"'
                    sh 'git config --global user.name "Jenkins Automation Server"'
                    sh "bumpversion --verbose ${params.VersionBump}"
                    sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/RedHatTraining/rht-labs-core.git HEAD:master --tags"
                }
                stash includes: 'src/labs/version.py', name: 'version'
            }
        }

        stage("Publish PROD & Release") {
            agent {
                kubernetes{
                    yaml libraryResource("podTemplates/jenkins-agent-python-39-pod.yaml")
                    cloud "${active_ocp_cloud}"
                }
            }
            when {
                beforeAgent true
                allOf {
                    //master or version tag
                    branch comparator: 'REGEXP', pattern: 'master|v\\d+\\.\\d+\\.\\d+'
                    expression { params.Publish }
                }
            }

            steps {
                // Get bumped version
                script {
                    try {
                        unstash "version"
                    } catch (e) {
                        echo "Version stash does not exist. Ignoring..."
                    }
                }

                script{
                    // Prevent version override in PyPI prod
                    if (!params.VersionOverride){
                        sh "! python -m infrastructure.ci.pypi.package_exists"
                    }
                }

                sh "make build"

                // Confirmation
                script {
                    version = sh(
                        script: 'python -c "from src.labs.version import __version__;print(__version__)"',
                        returnStdout: true
                    ).trim()

                    tagName = "v${version}"

                    try {
                        timeout(time:5, unit:'MINUTES') {
                            // TODO: restrict to specific users (hint: use the submitter parameter)
                            input "Publish ${tagName} to PyPI and create GitHub release?"
                        }
                    } catch(err) { // timeout reached or input Aborted
                        def user = err.getCauses()[0].getUser()
                        currentBuild.result = 'ABORTED'
                        if('SYSTEM' == user.toString()) { // SYSTEM means timeout
                            error("Input timeout expired, aborting...")
                        } else {
                            error("Pipeline aborted by: [${user}]")
                        }
                    }
                }

                // Publish to stage
                withCredentials([
                    usernamePassword(
                        credentialsId: 'pypi-stage-uploader',
                        usernameVariable: 'PYPI_USERNAME',
                        passwordVariable: 'PYPI_PASSWORD'
                    )
                ]) {
                    sh 'PS_PASSWD=${PYPI_PASSWORD} make PYPI_USER=${PYPI_USERNAME} publish-stage'
                }

                // Publish to prod
                withCredentials([
                    usernamePassword(
                        credentialsId: 'pypi-prod-uploader',
                        usernameVariable: 'PYPI_USERNAME',
                        passwordVariable: 'PYPI_PASSWORD'
                    )
                ]) {
                    //NA is default
                    sh 'PS_PASSWD_PROD=${PYPI_PASSWORD} make publish-prod'

                    //EMEA
                    sh 'PS_PASSWD_PROD=${PYPI_PASSWORD} make PYPI_SERVER_PROD=https://pypi.apps.tools-apac150.prod.ole.redhat.com/repository/labs/ PYPI_USER=${PYPI_USERNAME} publish-prod'

                    //APAC
                    sh 'PS_PASSWD_PROD=${PYPI_PASSWORD} make PYPI_SERVER_PROD=https://pypi.apps.tools-emea150.prod.ole.redhat.com/repository/labs/ PYPI_USER=${PYPI_USERNAME} publish-prod'
                    
                    //China
                    sh 'PS_PASSWD_PROD=${PYPI_PASSWORD} make PYPI_SERVER_PROD=https://pypi.apps.tools-apac152.prod.ole.redhat.com/repository/labs/ PYPI_USER=${PYPI_USERNAME} publish-prod'
                }

                // Create GitHub release
                withCredentials([string(
                    credentialsId: 'jenkins-release-token',
                    variable: 'JENKINS_TOKEN'
                )]) {
                    script {
                        version = sh(
                            script: 'python -c "from src.labs.version import __version__;print(__version__)"',
                            returnStdout: true
                        ).trim()

                        tagName = "v${version}"

                        def release_curl_command = """
                            curl -XPOST -H 'Authorization:token ${JENKINS_TOKEN}' \
                            https://api.github.com/repos/RedHatTraining/rht-labs-core/releases \
                            --data '{ \
                                "tag_name": "${tagName}", \
                                "name": "Release ${tagName}", \
                                "body": "Version ${version}", \
                                "draft": false, \
                                "prerelease": false \
                            }'
                        """

                        release = sh(
                            script: release_curl_command,
                            returnStdout: true
                        ).trim()

                        echo "Release ${version} created"
                        echo release
                    }
                }
            }
        }


        stage('Build documentation HTML and preview') {
            agent {
                kubernetes{
                    yaml libraryResource("podTemplates/jenkins-agent-python-39-pod.yaml")
                    cloud "${active_ocp_cloud}"
                }
            }

            when {
                anyOf {
                    changeset "docs/**"
                    allOf {
                        branch "master";
                        expression { params.Publish }
                    }
                }
            }

            steps {
                // Get bumped version
                script {
                    try {
                        unstash "version"
                    } catch (e) {
                        echo "Version stash does not exist. Ignoring..."
                    }
                }

                sh "pip install --upgrade pip"
                sh "pip install -e '.[git]'"

                // Generate config file to prevent import errors
                sh 'python -c "from labs.labconfig import savecfg;savecfg({\\"rhtlab\\":{\\"course\\":{\\"sku\\":\\"gl006\\"}}})"'

                // Build docs HTML
                dir("docs") {
                    sh "pip install -r requirements.txt"
                    sh "make html"
                }

                // Generate artifacts
                archiveArtifacts("docs/build/html/**/*.*")
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'docs/build/html',
                    reportFiles: 'index.html',
                    reportName: "DynoLabs Documentation HTML",
                    reportTitles: ''
                ])
                stash includes: 'docs/build/html/**/*.*', name: 'html'
            }

            post {
                success {
                    node('built-in'){
                        update_pr_comment(true)
                    }
                }
                failure {
                    node('built-in'){
                        update_pr_comment(false)
                    }
                }
            }
        }

        stage("Publish documentation HTML"){
            agent {
                label 'built-in'
            }

            when {
                beforeAgent true
                allOf {
                    branch "master";
                    expression { params.Publish }
                }
            }

            steps{
                unstash "html"
                // Get bumped version
                script {
                    try {
                        unstash "version"
                    } catch (e) {
                        echo "Version stash does not exist. Ignoring..."
                    }
                }

                // Make sure dynolabs-docs dir exists
                sh "mkdir -p ${DOCS_PUBLIC_PATH}"

                // Publish to dynolabs-docs/{version}
                script {
                    version = sh(
                        script: 'python -c "from src.labs.version import __version__;print(__version__)"',
                        returnStdout: true
                    ).trim()

                    sh "rm -rf ${DOCS_PUBLIC_PATH}/${version}"
                    sh "cp -r docs/build/html ${DOCS_PUBLIC_PATH}/${version}"
                }

                // Point "latest" to the version we just deployed
                sh "ln -sfn ${DOCS_PUBLIC_PATH}/${version} ${DOCS_PUBLIC_PATH}/latest"
            }
        }

    }
}


def update_pr_comment(success) {
    if (env.CHANGE_ID) {
        def existingComment = null;
        def commentContent = null;
        if (success) {
            commentContent = "Docs Built Successfully, preview [here](${env.BUILD_URL}DynoLabs_20Documentation_20HTML)"
        } else {
            commentContent = "Docs Sphinx build failed, see output [here](${env.BUILD_URL}console)"
        }
        try {
            if (pullRequest.comments.size() != 0) {
                for (comment in pullRequest.comments) {
                    if (comment.user == 'redhattraining-jenkins') {
                        existingComment = comment
                        break
                    }
                }
            }
            if (existingComment != null) {
                pullRequest.editComment(existingComment.id, commentContent)
            } else {
                pullRequest.comment(commentContent)
            }
        } catch (err) {
            echo "Error posting comment ${err}"
        }
    }
}

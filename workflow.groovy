parallel(
	"AwsStream":{
		node ('ops-school-dynamic-slave'){
			currentBuild.result = "SUCCESS"

			stage ('Checkout'){
				checkout scm
			}

			stage ('Build'){
				sh 'cd home-assignments/session2 && python cli.py -c --city Jerusalem --forecast TODAY+5'
			}
	}
)

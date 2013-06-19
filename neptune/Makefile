default:
	echo 'service_dev and scss_live'

service_dev:
	python server.py

scss_compile:
	sass --update resources/scss:resources/css

scss_live:
	sass --watch resources/scss:resources/css
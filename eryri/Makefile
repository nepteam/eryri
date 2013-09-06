default:
	@echo 'Static command for NEP Core'
	@echo '  make service:  active the service'
	@echo '  make css:      compile CSS from SCSS'
	@echo '  make css_live: compile CSS from SCSS and update when a file is updated'
	@echo
	@echo 'For more options, run "./console".'

service: css
	@python server.py

css:
	@sass --update resources/scss:resources/css --style compressed

css_live:
	@sass --watch resources/scss:resources/css --style compressed
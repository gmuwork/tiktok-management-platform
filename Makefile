black:
	black ./tiktok_manager --line-length=120

isort:
	isort ./tiktok_manager --profile black

update_reqs:
	pip-compile requirements.in

setup:
	# sets up the local environment for development
	bash setup.sh
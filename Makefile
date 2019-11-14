format:
	isort -rc -y src/**/*.py
	black -l 79 src/
docker_build:
	docker build -t tcga_data_explore .
docker_push:
	docker tag tcga_data_explore bdkech/analytical_tools:tcga_data_explore
	docker push bdkech/analytical_tools:tcga_data_explore

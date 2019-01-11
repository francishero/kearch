#! /bin/bash

USERNAME=$(whoami)

docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/me_gateway_spec.yaml -g python -o /local/me-gateway-client -c /local/openapi-me-gateway-client-config.json
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/me_gateway_spec.yaml -g python-flask -o /local/me-gateway-server -c /local/openapi-me-gateway-server-config.json
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/sp_gateway_spec.yaml -g python -o /local/sp-gateway-client -c /local/openapi-sp-gateway-client-config.json
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/sp_gateway_spec.yaml -g python-flask -o /local/sp-gateway-server -c /local/openapi-sp-gateway-server-config.json

sudo chown -R ${USERNAME}:${USERNAME} me-gateway-client
sudo chown -R ${USERNAME}:${USERNAME} me-gateway-server
sudo chown -R ${USERNAME}:${USERNAME} sp-gateway-client
sudo chown -R ${USERNAME}:${USERNAME} sp-gateway-server

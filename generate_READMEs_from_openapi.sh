#! /bin/bash

widdershins -c packages/sp-gateway/sp_gateway_spec.yaml -o packages/sp-gateway/README.md
widdershins -c packages/me-gateway/me_gateway_spec.yaml -o packages/me-gateway/README.md
widdershins -c packages/sp-classifier/sp_classifier_spec.yaml -o packages/sp-classifier/README.md
widdershins -c packages/sp-admin/sp_admin_spec.yaml -o packages/sp-admin/README.md
widdershins -c packages/sp-crawler-child/sp_crawler_child_spec.yaml packages/sp-crawler-child/README.md
widdershins -c packages/me-admin/me_admin_spec.yaml -o packages/me-admin/README.md
widdershins -c packages/sp-front/sp_front_spec.yaml -o packages/sp-front/README.md
widdershins -c packages/me-front/me_front_spec.yaml -o packages/me-front/README.md
widdershins -c packages/me-evaluater/me_evaluater_spec.yaml -o packages/me-evaluater/README.md

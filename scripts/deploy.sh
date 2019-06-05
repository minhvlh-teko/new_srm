#!/bin/bash
set -e

cd /var/www/api-v2.wms.phongvu.vn/

.venv/bin/pip install -r requirements.txt

sudo systemctl restart api-v2.service


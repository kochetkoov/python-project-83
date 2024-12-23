#!/usr/bin/env bash

make install
psql -U $DATABASE_URL -f database.sql
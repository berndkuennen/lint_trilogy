#!/bin/bash

# create service account
oc create sa my-sa-with-anyuid

# allow the account to run things with any uid
oc adm policy add-scc-to-user anyuid -z my-sa-with-anyuid

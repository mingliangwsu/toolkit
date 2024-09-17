#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 22:03:01 2024

@author: liuming
"""
import requests

def check_service(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("Service is up and running.")
        elif response.status_code == 404:
            print("Service endpoint not found.")
        elif response.status_code == 500:
            print("Service encountered an internal error.")
        else:
            print(f"Service returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking service: {e}")

# URL to check
url = 'https://sdmdataaccess.sc.egov.usda.gov/Tabular/post.rest'
check_service(url)
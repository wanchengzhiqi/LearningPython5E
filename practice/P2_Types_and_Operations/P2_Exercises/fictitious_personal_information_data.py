#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/31

info_data = {"name": {"first_name": "Alex",
                      "middle_name": "J",
                      "last_name": "Mercer"},
             "age": 27,
             "jobs": ["biologist", "geneticist", "GENTECK's employee"],
             "address": {"street": "1234 Elm Street",
                         "city": "New York",
                         "state": "NY",
                         "zip_code": "10001"},
             "email_address": "alexmercer@example.org",
             "phone_numbers": ["555-1234", "555-5678"],
             }

print(f"Name: {info_data['name']['first_name']} {info_data['name']['middle_name']} {info_data['name']['last_name']}")
print(f"Age: {info_data['age']}")
print(f"Jobs: {', '.join(info_data['jobs'])}")
print(f"Address: {info_data['address']['street']}, {info_data['address']['city']}, {info_data['address']['state']} {info_data['address']['zip_code']}")
print(f"Email Address: {info_data['email_address']}")
print(f"Phone Numbers: {', '.join(info_data['phone_numbers'])}")

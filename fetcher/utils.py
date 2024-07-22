import requests
from django.utils.dateparse import parse_datetime
from fetcher.models import Type, VerificationLevel, Country, Users, Analytics, Accounts, Company, Tags, Manager, Resources

def fetch_and_store_data():
    
    resp = {
        "total": 1,
        "data": [
            {
                "analytics": [
                    {
                        "property": "umt",
                        "value": "1111"
                    }
                ],
                "clientId": 2,
                "accounts": [
                    {
                        "accountId": 1,
                        "accountNumber": 123123,
                        "createTime": "2022-01-01T00:00:00+00:00"
                    }
                ],
                "birthday": "2022-01-01T00:00:00+00:00",
                "city": "string",
                "country": {
                    "countryId": 8,
                    "alpha2Code": "US",
                    "alpha3Code": "USA",
                    "countryName": "United States",
                    "numericCode": "840"
                },
                "company": {
                    "fullName": "full name company",
                    "shortName": "short name company"
                },
                "email": "foo@bar.com",
                "internalType": "default",
                "firstName": "Mary",
                "lastName": "Smith",
                "middleName": "Jane",
                "name": "Mary Jane Smith",
                "nickname": "Voronov",
                "locale": "ja_JP",
                "manager": {
                    "id": 1,
                    "enabled": False,
                    "email": "foo@bar.com",
                    "name": "John Smith",
                    "title": "mr.",
                    "phone": "+995577755422",
                    "resources": [
                        {
                            "key": "caption",
                            "locale": "ru_RU",
                            "value": "Lorem"
                        }
                    ],
                    "createTime": "2022-01-01T00:00:00+00:00"
                },
                "phone": "+7 999 200 00 00",
                "riskLevel": "low",
                "status": "active",
                "tags": [
                    "string"
                ],
                "type": {
                    "id": 1,
                    "name": "Individual"
                },
                "verificationLevel": {
                    "id": 1,
                    "name": "Level 1"
                },
                "loggedAt": "2022-01-01T00:00:00+00:00",
                "createTime": "2022-01-01T00:00:00+00:00",
                "updateTime": "2022-01-01T00:00:00+00:00"
            }
        ]
    }

    data = resp['data']  # Use resp directly since it's already a dictionary

    for item in data:
        country_data = item.get('country', {})
        country, created = Country.objects.update_or_create(
            countryId=country_data.get('countryId'),
            defaults={
                'alpha2Code': country_data.get('alpha2Code'),
                'alpha3Code': country_data.get('alpha3Code'),
                'countryName': country_data.get('countryName'),
                'numericCode': country_data.get('numericCode')
            }
        )

        type_data = item.get('type', {})
        user_type, created = Type.objects.update_or_create(
            id=type_data.get('id'),
            defaults={'name': type_data.get('name')}
        )

        verification_data = item.get('verificationLevel', {})
        verification_level, created = VerificationLevel.objects.update_or_create(
            id=verification_data.get('id'),
            defaults={'name': verification_data.get('name')}
        )

        # Check if user with the same clientId already exists
        user, created = Users.objects.update_or_create(
            clientId=item.get('clientId'),  # Use clientId for checking duplicates
            defaults={
                'email': item.get('email'),
                'firstName': item.get('firstName'),
                'lastName': item.get('lastName'),
                'middleName': item.get('middleName'),
                'name': item.get('name'),
                'nickname': item.get('nickname'),
                'birthday': item.get('birthday'),
                'phone': item.get('phone'),
                'internalType': item.get('internalType'),
                'locale': item.get('locale'),
                'riskLevel': item.get('riskLevel'),
                'status': item.get('status'),
                'city': item.get('city'),
                'countryId': country,
                'type': user_type,
                'verificationLevel': verification_level,
                'loggedAt': parse_datetime(item.get('loggedAt')),
                'createTime': parse_datetime(item.get('createTime')),
                'updateTime': parse_datetime(item.get('updateTime'))
            }
        )

        for analytics_data in item.get('analytics', []):
            Analytics.objects.update_or_create(
                userID=user,
                property=analytics_data.get('property'),
                defaults={'value': analytics_data.get('value')}
            )

        for account_data in item.get('accounts', []):
            Accounts.objects.update_or_create(
                userID=user,
                accountId=account_data.get('accountId'),
                defaults={
                    'accountNumber': account_data.get('accountNumber'),
                    'createTime': parse_datetime(account_data.get('createTime'))
                }
            )

        company_data = item.get('company', {})
        Company.objects.update_or_create(
            userID=user,
            defaults={
                'fullName': company_data.get('fullName'),
                'shortName': company_data.get('shortName')
            }
        )

        for tag in item.get('tags', []):
            Tags.objects.update_or_create(
                userId=user,
                defaults={'name': tag}
            )

        manager_data = item.get('manager', {})
        manager, created = Manager.objects.update_or_create(
            id=manager_data.get('id'),
            defaults={
                'enabled': manager_data.get('enabled'),
                'email': manager_data.get('email'),
                'name': manager_data.get('name'),
                'title': manager_data.get('title'),
                'phone': manager_data.get('phone'),
                'userId': user,
                'createTime': parse_datetime(manager_data.get('createTime'))
            }
        )

        for resource_data in manager_data.get('resources', []):
            Resources.objects.update_or_create(
                managerId=manager,
                key=resource_data.get('key'),
                defaults={
                    'locale': resource_data.get('locale'),
                    'value': resource_data.get('value')
                }
            )

from rest_framework import serializers
from fetcher.models import Users, Analytics, Accounts, Company, Tags, Manager, Country, Type, VerificationLevel, Resources

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = '__all__'

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = '__all__'

class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class VerificationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationLevel
        fields = '__all__'

class GetClientListSerializers(serializers.ModelSerializer):
    analytics = AnalyticsSerializer(many=True)
    accounts = AccountsSerializer(many=True)
    company = CompanySerializer()
    tags = serializers.ListField(child=serializers.CharField())
    manager = ManagerSerializer()
    country = CountrySerializer()
    type = TypeSerializer()
    verificationLevel = VerificationLevelSerializer()

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        analytics_data = validated_data.pop('analytics')
        accounts_data = validated_data.pop('accounts')
        company_data = validated_data.pop('company')
        tags_data = validated_data.pop('tags')
        manager_data = validated_data.pop('manager')
        resources_data = manager_data.pop('resources', [])
        country_data = validated_data.pop('country')
        type_data = validated_data.pop('type')
        verification_level_data = validated_data.pop('verificationLevel')

        country, created = Country.objects.get_or_create(**country_data)
        type_obj, created = Type.objects.get_or_create(**type_data)
        verification_level, created = VerificationLevel.objects.get_or_create(**verification_level_data)
        
        user = Users.objects.create(
            countryId=country,
            type=type_obj,
            verificationLevel=verification_level,
            **validated_data
        )

        for analytics_item in analytics_data:
            Analytics.objects.create(userID=user, **analytics_item)
        
        for account_item in accounts_data:
            Accounts.objects.create(userID=user, **account_item)
        
        Company.objects.create(userID=user, **company_data)

        for tag_name in tags_data:
            Tags.objects.create(userId=user, name=tag_name)

        manager = Manager.objects.create(userId=user, **manager_data)
        for resource_item in resources_data:
            Resources.objects.create(managerId=manager, **resource_item)

        return user

from django.db import models

class Type(models.Model):
    name=models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        db_table="type"
        ordering = ('id',)
    
    def __str__(self):
        return "{}".format(self.id)

class VerificationLevel(models.Model):
    name=models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        db_table="verification"
        ordering = ('id',)
    
    def __str__(self):
        return "{}".format(self.id)


class Country(models.Model):
    countryId=models.CharField(max_length=100, default=None, blank=True, null=True)
    alpha2Code=models.CharField(max_length=100, default=None, blank=True, null=True)
    alpha3Code=models.CharField(max_length=100, default=None, blank=True, null=True)
    countryName=models.CharField(max_length=100, default=None, blank=True, null=True)
    numericCode=models.CharField(max_length=100, default=None, blank=True, null=True)
    class Meta:
        db_table="country"
        ordering = ('id',)
    
    def __str__(self):
        return "{}".format(self.id)


class Users(models.Model):
    firstName=models.CharField(max_length=150)
    lastName=models.CharField(max_length=100, default=None, blank=True, null=True)
    middleName=models.CharField(max_length=100, default=None, blank=True, null=True)
    name=models.CharField(max_length=100, default=None, blank=True, null=True)
    nickname=models.CharField(max_length=100, default=None, blank=True, null=True)
    birthday=models.CharField(max_length=100, default=None, blank=True, null=True)
    email=models.EmailField()
    phone=models.CharField(max_length=17)
    
    internalType=models.CharField(max_length=100, default=None, blank=True, null=True)
    locale=models.CharField(max_length=100, default=None, blank=True, null=True)
    riskLevel=models.CharField(max_length=100, default=None, blank=True, null=True)
    status=models.CharField(max_length=100, default=None, blank=True, null=True)
    
    city=models.CharField(max_length=100, default=None, blank=True, null=True)
    countryId=models.ForeignKey(Country, db_column="country_id",on_delete=models.CASCADE, default=None,null=True, related_name="user_country")
    type=models.ForeignKey(Type, db_column="country_type",on_delete=models.CASCADE, default=None,null=True, related_name="user_type")
    verificationLevel=models.ForeignKey(VerificationLevel, db_column="verify_level_id",on_delete=models.CASCADE, default=None,null=True, related_name="user_verify_level")

    clientId=models.CharField(max_length=5, default=None, blank=True, null=True)
    loggedAt=models.DateTimeField("Logged At", auto_now=True)
    createTime=models.DateTimeField('Created Time',auto_now_add=True)
    updateTime=models.DateTimeField("Updated Time", auto_now=True)
    
    class Meta:
        db_table="users"
        ordering = ('-createTime',)
    
    def __str__(self):
        return "{}".format(self.id)


class Analytics(models.Model):
    property=models.CharField(max_length=100, default=None, blank=True, null=True)
    value=models.CharField(max_length=100, default=None, blank=True, null=True)
    userID=models.ForeignKey(Users, db_column="user_id",on_delete=models.CASCADE, default=None,null=True, related_name="analytics_user")
    class Meta:
        db_table="analytics"
        ordering = ('id',)
    
    def __str__(self):
        return "{}".format(self.id)

class Accounts(models.Model):
    accountId=models.CharField(max_length=100, default=None, blank=True, null=True)
    accountNumber=models.PositiveIntegerField()
    userID=models.ForeignKey(Users, db_column="user_id",on_delete=models.CASCADE, default=None,null=True, related_name="accounts_user")
    createTime=models.DateTimeField('Created Time',auto_now_add=True)
    
    class Meta:
        db_table="accounts"
        ordering = ('-createTime',)
    
    def __str__(self):
        return "{}".format(self.id)

class Company(models.Model):
    fullName=models.CharField(max_length=100, default=None, blank=True, null=True)
    shortName=models.CharField(max_length=100, default=None, blank=True, null=True)
    userID=models.ForeignKey(Users, db_column="user_id",on_delete=models.CASCADE, default=None,null=True, related_name="company_user")
    class Meta:
        db_table="company"
        ordering = ('id',)
    
    def __str__(self):
        return "{}".format(self.id)

class Tags(models.Model):
    name=models.CharField(max_length=150, default=None, blank=True, null=True)
    userId=models.ForeignKey(Users, db_column="user_id",on_delete=models.CASCADE, default=None,null=True, related_name="tags_user")
    class Meta:
        db_table="tags"
        ordering = ('id',)
    
    def __str__(self):
        return "{}".format(self.id)

class Manager(models.Model):
    enabled=models.BooleanField(default=False)
    email=models.CharField(max_length=100, default=None, blank=True, null=True)
    name=models.CharField(max_length=100, default=None, blank=True, null=True)
    title=models.CharField(max_length=100, default=None, blank=True, null=True)
    phone=models.CharField(max_length=100, default=None, blank=True, null=True)
    userId=models.ForeignKey(Users, db_column="user_id",on_delete=models.CASCADE, default=None,null=True, related_name="manager_user")
    createTime=models.DateTimeField('Created Time',auto_now_add=True)
    
    class Meta:
        db_table="manager"
        ordering = ('-createTime',)
    
    def __str__(self):
        return "{}".format(self.id)


class Resources(models.Model):
    key=models.CharField(max_length=100, default=None, blank=True, null=True)
    locale=models.CharField(max_length=100, default=None, blank=True, null=True)
    value=models.CharField(max_length=100, default=None, blank=True, null=True)
    managerId=models.ForeignKey(Manager, db_column="manager_id",on_delete=models.CASCADE, default=None,null=True, related_name="resource_manager")
    
    class Meta:
        db_table="resources"
        ordering = ('id',)
    
    def __str__(self):
        return "{}".format(self.id)
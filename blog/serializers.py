from rest_framework import serializers
from .models import Blog
# from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class BlogSerializer(serializers.ModelSerializer):
       class Meta:
        model = Blog
        fields = ['id','title','thumbnail','get_absolute_url','get_edit_url','get_delete_url']
  
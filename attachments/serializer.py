from .models import Like,Comment,Link,Download,Image, Tag,PagePrint
from core.serializers import PersonSerializer,serializers,PageSerializer 
from .models import Area, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=['id','title','longitude','location','latitude','title','get_absolute_url']


  
class PagePrintSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    person=PersonSerializer()
    class Meta:
        model=PagePrint
        fields=['id','page','person','type','printed', 'persian_datetime_added']

       
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields=['id','code','color','area','title','get_absolute_url']


          

class LikeSerializer(serializers.ModelSerializer):
    person=PersonSerializer()
    class Meta:
        model=Like
        fields=['id', 'person']
 
class CommentSerializer2(serializers.ModelSerializer):
    person=PersonSerializer() 
    page=PageSerializer()
    class Meta:
        model=Comment
        fields=['id','reply_to_id','page','person','comment','get_delete_url','persian_datetime_added']
 
 

class CommentSerializer(serializers.ModelSerializer):
    person=PersonSerializer()
    childs=CommentSerializer2(many=True)
    page=PageSerializer()
    class Meta:
        model=Comment
        fields=['id','childs','reply_to_id','get_delete_url','page','person','comment','persian_datetime_added']
 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=['id' , 'title','get_absolute_url']
 
class LinkSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    # person=ProfileSerializer()
    class Meta:
        model=Link
        fields=['id','page', 'url','priority','title','get_edit_url','get_delete_url']
 

 
class ImageSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    # person=ProfileSerializer()
    class Meta:
        model=Image
        fields=['id','page','title', 'thumbnail','get_absolute_url','image','persian_date_added','priority','title','get_edit_url','get_delete_url']
 

class DownloadSerializer(serializers.ModelSerializer):
    page=PageSerializer()
    person=PersonSerializer()
    class Meta:
        model=Download
        fields=['id','page','get_download_url','persian_date_added', 'person','title','get_edit_url','get_delete_url']
 

from rest_framework import serializers

from feedbacks.models import Feedback
from users.serializers import SerializerUsers   


class FeedbackSerializer(serializers.ModelSerializer):
    user = SerializerUsers(read_only=True)
    class Meta:
        model = Feedback

        fields = ['id', 'feedback', 'rate', 'work_id', 'user']
        read_only_fields = ['user', 'work_id']
    
    def validate_rate(self, rate: int):
        if rate < 0 or rate > 10:
            raise serializers.ValidationError('Enter a number between 0 and 10')
        
        return rate

    

from rest_framework import serializers

from institutions.models import Institution, InstitutionInfo


class InstitutionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionInfo

        fields = ['link', 'city', 'state', 'phone', 'cep']



class InstitutionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Institution

        fields = ['id', 'name', 'infos']
    
    infos = InstitutionInfoSerializer(read_only=True)



class InstitutionCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=225)
    city = serializers.CharField(max_length=80, allow_blank=True, allow_null=True, default=None, write_only=True)
    state = serializers.CharField(max_length=80, allow_blank=True, allow_null=True, default=None, write_only=True)
    link = serializers.CharField(max_length=250, allow_blank=True, allow_null=True, default=None, write_only=True)
    phone = serializers.CharField(max_length=80, allow_blank=True, allow_null=True, default=None, write_only=True)
    cep = serializers.CharField(max_length=80, allow_blank=True, allow_null=True, default=None, write_only=True)
    infos = InstitutionInfoSerializer(read_only=True)


    def validate_name(self, name: str):
        name_already_exists = Institution.objects.filter(name__iexact=name)

        if name_already_exists:
            raise serializers.ValidationError('Institution already exists')

        return name


    def create(self, validated_data: dict):
        institution_name = validated_data.pop('name')

        institution_info = InstitutionInfo.objects.create(**validated_data)

        institution = Institution.objects.create(**{'name': institution_name}, infos=institution_info)

        return institution

    
    def update(self, institution: Institution, validated_data: dict):
        name = validated_data.get('name')

        if name:
            validated_data.pop('name')
            setattr(institution, 'name', name)
        
        if validated_data:
            institution_info: InstitutionInfo = institution.infos

            for key, value in validated_data.items():
                setattr(institution_info, key, value)
            
            institution_info.save()
        
        institution.save()

        return institution









      

   
        

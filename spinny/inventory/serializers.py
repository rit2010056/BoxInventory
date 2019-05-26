from rest_framework import serializers
from .models import Box
import rest_framework

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        exclude_fields = kwargs.pop('exclude_fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if exclude_fields:
            # Drop any fields that are not specified in the `fields` argument.
            exclude_fields = set(exclude_fields)

            for field_name in exclude_fields:
                self.fields.pop(field_name)


class BoxesSerializer(DynamicFieldsModelSerializer):

    created_by_name = serializers.CharField(source='created_by',read_only=True)
    updated_by_name = serializers.CharField(source='updated_by',read_only=True)

    class Meta:
        model = Box
        fields = (
                    "length",
                    "width",
                    "height",
                    "volume",
                    "area",
                    "created_by_name",
                    "created_by",
                    "updated_by",
                    "updated_by_name",
                    "created_at",
                    "updated_at"
                )


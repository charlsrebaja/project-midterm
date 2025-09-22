# API Documentation with Swagger/OpenAPI

This project uses Swagger/OpenAPI for API documentation and testing. This document explains how to use the Swagger UI and how to ensure new API endpoints are automatically documented.

## Accessing the Swagger UI

The Swagger UI is available at the following URLs:

- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc UI**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- **OpenAPI Schema**: [http://localhost:8000/swagger.json](http://localhost:8000/swagger.json) or [http://localhost:8000/swagger.yaml](http://localhost:8000/swagger.yaml)

## Using Swagger UI for API Testing

1. Navigate to [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
2. You'll see a list of all available API endpoints grouped by tags (jokes, ciphers, automation)
3. Click on an endpoint to expand it and see details
4. Click the "Try it out" button
5. Fill in the required parameters
6. Click "Execute" to test the API
7. View the response below

## Adding Documentation to New API Endpoints

When adding new API endpoints, follow these steps to ensure they are automatically documented:

### 1. Create a Serializer

Create a serializer for your API request and response in a `serializers.py` file in your app:

```python
from rest_framework import serializers

class MyRequestSerializer(serializers.Serializer):
    field1 = serializers.CharField(required=True, help_text="Description of field1")
    field2 = serializers.IntegerField(required=False, help_text="Description of field2")

class MyResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
```

### 2. Decorate Your View

Use the `@swagger_auto_schema` decorator to document your view:

```python
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from .serializers import MyRequestSerializer, MyResponseSerializer

@swagger_auto_schema(
    method='post',  # or 'get', 'put', etc.
    request_body=MyRequestSerializer,  # for POST, PUT requests
    query_serializer=MyRequestSerializer,  # for GET requests with query params
    operation_description="Description of what this API does",
    responses={
        200: MyResponseSerializer,
        400: "Bad Request",
        500: "Internal Server Error"
    },
    tags=['my_tag']  # Group in Swagger UI
)
@api_view(['POST'])  # or ['GET'], etc.
def my_api_view(request):
    # Your view logic here
    pass
```

### 3. Update the OpenAPI YAML (Optional)

If you want to maintain a static OpenAPI specification, update the `openapi.yaml` file with your new endpoint:

```yaml
paths:
  /my-app/my-endpoint/:
    post:
      tags:
        - my_tag
      summary: Short summary
      description: Longer description
      operationId: myApiView
      requestBody:
        description: Request parameters
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MyRequest'
      responses:
        '200':
          description: Successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MyResponse'
```

## Automatic Documentation Updates

The Swagger documentation is automatically generated from your code. When you add new API endpoints with proper decorators, they will automatically appear in the Swagger UI.

The key components that enable automatic updates are:

1. **swagger.py**: Contains the configuration for the Swagger schema view
2. **@swagger_auto_schema decorator**: Documents individual API endpoints
3. **Serializers**: Define the structure of request and response data

## Best Practices

1. Always use serializers to define request and response structures
2. Use descriptive operation_description in @swagger_auto_schema
3. Group related endpoints with the same tag
4. Include all possible response codes
5. Add help_text to serializer fields for better documentation
6. Test your API through the Swagger UI to ensure it works as expected

## Troubleshooting

If your API endpoint is not showing up in the Swagger UI:

1. Make sure you've added the @swagger_auto_schema decorator
2. Ensure you've added the @api_view decorator with the correct HTTP methods
3. Check that your URL is properly registered in your app's urls.py
4. Restart the Django server to refresh the schema

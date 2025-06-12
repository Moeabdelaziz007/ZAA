import json
import os
from pathlib import Path
from fastapi.openapi.utils import get_openapi
from app.main import app

def generate_openapi_docs():
    """توليد توثيق OpenAPI وحفظه في ملف JSON"""
    
    # توليد توثيق OpenAPI
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # إنشاء مجلد docs إذا لم يكن موجوداً
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # حفظ التوثيق في ملف JSON
    with open(docs_dir / "openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, ensure_ascii=False, indent=2)
    
    # توليد ملف HTML باستخدام Swagger UI
    html_template = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>توثيق API - Zentix AI</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.1.3/swagger-ui.css">
        <style>
            body {
                margin: 0;
                background-color: #fafafa;
            }
            .swagger-ui {
                font-family: 'Cairo', sans-serif;
            }
            .swagger-ui .opblock {
                border-radius: 8px;
                margin-bottom: 16px;
            }
            .swagger-ui .opblock .opblock-summary {
                padding: 8px;
            }
            .swagger-ui .opblock .opblock-summary-method {
                border-radius: 4px;
            }
            .swagger-ui .opblock .opblock-summary-path {
                font-weight: 600;
            }
            .swagger-ui .opblock .opblock-summary-description {
                color: #666;
            }
            .swagger-ui .opblock .opblock-body {
                padding: 16px;
            }
            .swagger-ui .opblock .opblock-body pre {
                border-radius: 4px;
            }
            .swagger-ui .opblock .opblock-body .opblock-section {
                margin-bottom: 16px;
            }
            .swagger-ui .opblock .opblock-body .opblock-section-header {
                background-color: #f5f5f5;
                padding: 8px;
                border-radius: 4px;
            }
            .swagger-ui .opblock .opblock-body .opblock-section-header h4 {
                margin: 0;
                font-weight: 600;
            }
            .swagger-ui .opblock .opblock-body .opblock-section-header .opblock-section-header {
                margin-bottom: 8px;
            }
            .swagger-ui .opblock .opblock-body .opblock-section-header .opblock-section-header h4 {
                font-size: 14px;
            }
            .swagger-ui .opblock .opblock-body .opblock-section-header .opblock-section-header .opblock-section-header {
                margin-bottom: 4px;
            }
            .swagger-ui .opblock .opblock-body .opblock-section-header .opblock-section-header .opblock-section-header h4 {
                font-size: 12px;
            }
            .swagger-ui .opblock .opblock-body .opblock-section-header .opblock-section-header .opblock-section-header .opblock-section-header {
                margin-bottom: 2px;
            }
            .swagger-ui .opblock .opblock-body .opblock-section-header .opblock-section-header .opblock-section-header .opblock-section-header h4 {
                font-size: 10px;
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@4.1.3/swagger-ui-bundle.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "./openapi.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "BaseLayout",
                    docExpansion: "list",
                    defaultModelsExpandDepth: 3,
                    defaultModelExpandDepth: 3,
                    displayRequestDuration: true,
                    filter: true,
                    showExtensions: true,
                    showCommonExtensions: true,
                    supportedSubmitMethods: [
                        "get",
                        "post",
                        "put",
                        "delete",
                        "patch"
                    ]
                });
                window.ui = ui;
            };
        </script>
    </body>
    </html>
    """
    
    with open(docs_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print("✅ تم توليد توثيق OpenAPI بنجاح!")

if __name__ == "__main__":
    generate_openapi_docs() 
from backend.routes import app
import os

with app.app_context():
    app.jinja_env.cache = {}  # Clear Jinja cache
    app.jinja_env.loader = app.create_global_jinja_loader()  # Force load templates
    
    print("🔍 Flask is looking in:", app.template_folder)
    print("📂 Folder exists:", os.path.exists(app.template_folder))
    print("📄 Found templates:", os.listdir(app.template_folder))
    print("📃 Jinja detected templates:", app.jinja_env.list_templates())

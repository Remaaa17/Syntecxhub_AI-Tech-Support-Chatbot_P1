"""
Create a clean ZIP file for distribution without sensitive data
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_clean_zip():
    """Create a ZIP file with important files, excluding sensitive data"""
    
    # Output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f'AI_Tech_Support_Chatbot_Clean_{timestamp}.zip'
    output_path = os.path.join('..', zip_filename)
    
    print("=" * 60)
    print("Creating Clean Distribution ZIP")
    print("=" * 60)
    
    # Files and folders to include
    include_patterns = [
        # Python files
        'app.py',
        'console_bot.py',
        'requirements.txt',
        'run.bat',
        
        # Source code
        'src/*.py',
        
        # Data
        'data/knowledge_base.json',
        
        # Documentation
        'README.md',
        'docs/*.md',
        'TEST_GUIDE.md',
        'QUICK_TEST.md',
        'FIXES_SUMMARY.md',
        'AI_PLAIN_TEXT_UPDATE.md',
        
        # Web files
        'templates/*.html',
        'static/css/*.css',
        'static/js/*.js',
        
        # Config examples
        '.env.example',
        '.gitignore',
    ]
    
    # Files to explicitly exclude
    exclude_files = [
        '.env',  # Contains API keys
        '__pycache__',
        '.git',
        '.gitignore',
        '*.pyc',
        '*.pyo',
        'test_*.py',
        'create_zip.py',
        'exports/',
        'logs/',
        'models/',
        '.DS_Store',
        'Thumbs.db'
    ]
    
    files_added = []
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Add root files
        for filename in ['app.py', 'console_bot.py', 'requirements.txt', 
                        'run.bat', 'README.md', '.env.example', '.gitignore',
                        'TEST_GUIDE.md', 'QUICK_TEST.md', 'FIXES_SUMMARY.md',
                        'AI_PLAIN_TEXT_UPDATE.md', 'DISTRIBUTION_README.md']:
            if os.path.exists(filename):
                zipf.write(filename, os.path.join('AI_Tech_Support_Chatbot', filename))
                files_added.append(filename)
                print(f"✓ Added: {filename}")
        
        # Add src folder
        if os.path.exists('src'):
            for filename in os.listdir('src'):
                if filename.endswith('.py') and not filename.startswith('test_'):
                    filepath = os.path.join('src', filename)
                    zipf.write(filepath, os.path.join('AI_Tech_Support_Chatbot', filepath))
                    files_added.append(filepath)
                    print(f"✓ Added: {filepath}")
        
        # Add data folder
        if os.path.exists('data'):
            for filename in os.listdir('data'):
                if filename.endswith('.json'):
                    filepath = os.path.join('data', filename)
                    zipf.write(filepath, os.path.join('AI_Tech_Support_Chatbot', filepath))
                    files_added.append(filepath)
                    print(f"✓ Added: {filepath}")
        
        # Add docs folder
        if os.path.exists('docs'):
            for filename in os.listdir('docs'):
                if filename.endswith('.md'):
                    filepath = os.path.join('docs', filename)
                    zipf.write(filepath, os.path.join('AI_Tech_Support_Chatbot', filepath))
                    files_added.append(filepath)
                    print(f"✓ Added: {filepath}")
        
        # Add templates
        if os.path.exists('templates'):
            for filename in os.listdir('templates'):
                if filename.endswith('.html'):
                    filepath = os.path.join('templates', filename)
                    zipf.write(filepath, os.path.join('AI_Tech_Support_Chatbot', filepath))
                    files_added.append(filepath)
                    print(f"✓ Added: {filepath}")
        
        # Add static/css
        css_path = os.path.join('static', 'css')
        if os.path.exists(css_path):
            for filename in os.listdir(css_path):
                if filename.endswith('.css'):
                    filepath = os.path.join(css_path, filename)
                    zipf.write(filepath, os.path.join('AI_Tech_Support_Chatbot', filepath))
                    files_added.append(filepath)
                    print(f"✓ Added: {filepath}")
        
        # Add static/js
        js_path = os.path.join('static', 'js')
        if os.path.exists(js_path):
            for filename in os.listdir(js_path):
                if filename.endswith('.js'):
                    filepath = os.path.join(js_path, filename)
                    zipf.write(filepath, os.path.join('AI_Tech_Support_Chatbot', filepath))
                    files_added.append(filepath)
                    print(f"✓ Added: {filepath}")
        
        # Create empty folders
        for folder in ['logs', 'models', 'exports']:
            zipf.writestr(os.path.join('AI_Tech_Support_Chatbot', folder, '.gitkeep'), '')
            print(f"✓ Created: {folder}/ (empty)")
    
    print("=" * 60)
    print(f"✅ ZIP file created: {output_path}")
    print(f"📊 Total files: {len(files_added)}")
    print(f"📦 File size: {os.path.getsize(output_path) / 1024:.2f} KB")
    print("=" * 60)
    print("\n✅ Safe to share - no API keys included!")
    print("📋 Users need to create their own .env file with GROQ_API_KEY")
    
    return output_path

if __name__ == '__main__':
    try:
        zip_path = create_clean_zip()
        print(f"\n✅ Done! ZIP saved to: {os.path.abspath(zip_path)}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

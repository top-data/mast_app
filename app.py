from flask import Flask, render_template, request, send_file
import os
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']
        
        if uploaded_file.filename != '':
            # Save the uploaded file to a temporary location
            uploaded_file.save(uploaded_file.filename)
            
            # Run the main.py script
            subprocess.run(['python', 'main.py', uploaded_file.filename])
            
            # Generate the path for the result file
            result_filename = "ai_output.csv"  
            
            # Return the result file for download
            return send_file(result_filename, as_attachment=True)
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

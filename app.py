from flask import Flask, render_template, request, send_file
import os
import subprocess
from ai_functions import return_ai_output

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']
        
        if uploaded_file.filename != '':
            # Save the uploaded file to a temporary location
            uploaded_file.save(uploaded_file.filename)
            
            # return output file
            ai_output = return_ai_output(uploaded_file.filename)
            
            # Generate the path for the result file
            result_filename = f"{uploaded_file.filename.rstrip('.csv')}_output.csv"  
            ai_output.to_csv(result_filename, index=False)
            
            # Return the result file for download
            return send_file(result_filename, as_attachment=True)
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

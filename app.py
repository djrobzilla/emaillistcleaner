import re
import csv
import os
from flask import Flask, request, render_template, redirect, url_for, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def clean_email_list(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        header = next(reader)
        writer.writerow(header)

        for row in reader:
            cleaned_row = [re.sub(r'\s+', '', email)
                           for email in row if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)]
            if cleaned_row:
                writer.writerow(cleaned_row)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            output_path = os.path.join(
                app.config['UPLOAD_FOLDER'], 'cleaned_' + filename)
            clean_email_list(input_path, output_path)
            response = send_file(output_path, as_attachment=True)

            # Delete the files after sending the response
            os.remove(input_path)
            os.remove(output_path)

            return response
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)

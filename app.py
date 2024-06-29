import re
import csv
import os
from flask import Flask, request, render_template, redirect, url_for, send_file, session, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
app.secret_key = 'supersecretkey'  # Needed for session management

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def clean_email_list(input_file, output_file):
    removed_emails = []
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header
        header = next(reader)
        writer.writerow(header)

        for row_num, row in enumerate(reader, start=2):
            cleaned_row = [re.sub(r'\s+', '', email)
                           for email in row if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)]
            removed = [email for email in row if email not in cleaned_row]
            if removed:
                removed_emails.append((row_num, removed))
            if cleaned_row:
                writer.writerow(cleaned_row)
    return removed_emails


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/emaillistcleaner', methods=['GET', 'POST'])
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
            removed_emails = clean_email_list(input_path, output_path)
            response = send_file(output_path, as_attachment=True)

            # Save the removed emails in session
            session['removed_emails'] = removed_emails

            # Send the cleaned file
            response = send_file(output_path, as_attachment=True)

            # Delete the files after sending the response
            os.remove(input_path)
            os.remove(output_path)

            return response
    return render_template('emaillistcleaner.html')


@app.route('/report')
def report():
    removed_emails = session.get('removed_emails', [])
    return render_template('report.html', removed_emails=removed_emails)


if __name__ == "__main__":
    app.run(debug=True)

import os.path
import tempfile

from flask import Flask, request, render_template, send_file
from werkzeug import secure_filename

from forms import PDFForm
from utils import convert_pdf, arg_by_form


DEBUG = True
#ALLOWED_EXTENSIONS = ["pdf",]
UPLOAD_FOLDER = "/tmp"


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024
app.config['DEBUG'] = DEBUG
app.secret_key = 'A0Zr98j/3yX R~XHH!jmGGGRT'


@app.route("/", methods=("GET", "POST"))
def main():
    form = PDFForm()
    if form.validate_on_submit():
        filename = secure_filename(form.pdf.file.filename)
        #filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        _, filepath = tempfile.mkstemp(suffix=".pdf",
                                       prefix="k2pdf",
                                       dir=app.config['UPLOAD_FOLDER'])
        pdffile = request.files['pdf']
        pdffile.save(filepath)
        arg = arg_by_form(form)
        new_filename, newpdfpath = convert_pdf(filepath, filename, arg=arg)
        #
        return send_file(newpdfpath, mimetype="application/pdf", as_attachment=True,
                         attachment_filename=new_filename, add_etags=True,
                         cache_timeout=43200, conditional=False)
    else:
        filename = None

    return render_template("main.html", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    

from flask import Flask, render_template, request
import pdfplumber

app = Flask(__name__, template_folder="templates")
@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    keyword = ""

    if request.method == "POST":
        pdf_file = request.files["pdf"]
        keyword = request.form["keyword"].strip()

        with pdfplumber.open(pdf_file) as pdf:
            for page_no, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    for line in text.split("\n"):
                        if keyword.lower() in line.lower():
                            results.append({
                                "page": page_no,
                                "text": line
                            })

    return render_template("index.html", results=results, keyword=keyword)

if __name__ == "__main__":
    app.run()

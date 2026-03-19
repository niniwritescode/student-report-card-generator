from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        class_name = request.form["class"]
        maths = float(request.form["maths"])
        science = float(request.form["science"])
        english = float(request.form["english"])

        total = maths + science + english
        percentage = (total / 300) * 100

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "F"

        status = "Pass" if percentage >= 50 else "Fail"

        result = {
            "name": name,
            "roll": roll,
            "class": class_name,
            "maths": maths,
            "science": science,
            "english": english,
            "total": total,
            "percentage": round(percentage, 2),
            "grade": grade,
            "status": status
        }

    return render_template("index.html", result=result)


@app.route("/download", methods=["POST"])
def download():

    name = request.form["name"]
    roll = request.form["roll"]
    class_name = request.form["class"]
    maths = float(request.form["maths"])
    science = float(request.form["science"])
    english = float(request.form["english"])

    total = maths + science + english
    percentage = (total / 300) * 100

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    status = "Pass" if percentage >= 50 else "Fail"

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    # Logo
    pdf.drawImage("logo.png", 250, 760, width=80, height=80)

    # School title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(180, 730, "Springfield Public School")

    # Subtitle
    pdf.setFont("Helvetica", 14)
    pdf.drawString(230, 700, "Student Report Card")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 650, f"Name: {name}")
    pdf.drawString(100, 630, f"Class: {class_name}")
    pdf.drawString(100, 610, f"Roll No: {roll}")

    pdf.drawString(100, 570, f"Maths: {maths}")
    pdf.drawString(100, 550, f"Science: {science}")
    pdf.drawString(100, 530, f"English: {english}")

    pdf.drawString(100, 490, f"Total: {total}")
    pdf.drawString(100, 470, f"Percentage: {round(percentage,2)}%")
    pdf.drawString(100, 450, f"Grade: {grade}")
    pdf.drawString(100, 430, f"Status: {status}")

    pdf.save()

    buffer.seek(0)

    return send_file(buffer,
                     as_attachment=True,
                     download_name="report_card.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)
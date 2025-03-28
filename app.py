from flask import Flask, request, send_file
from flask_cors import CORS  # استيراد CORS
import qrcode
from io import BytesIO

app = Flask(__name__)
CORS(app)  # تفعيل CORS للسماح بالطلبات من index.html

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    try:
        data = request.json.get('data', '')
        color = request.json.get('color', 'black')
        bg_color = request.json.get('bg_color', 'white')

        if not data:
            return {"error": "البيانات فارغة!"}, 400

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=color, back_color=bg_color)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)


import os
import subprocess
import uuid
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "input")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sakura.png')
def serve_sakura():
    return send_from_directory(SCRIPT_DIR, 'sakura.png')


@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diupload'}), 400
    
    file = request.files['file']
    mode = request.form.get('mode', 'enhance')
    scale = request.form.get('scale', '4')
    
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Format file tidak didukung'}), 400
    
    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())[:8]
    name, ext = os.path.splitext(filename)
    
    input_filename = f"{name}_{unique_id}_input{ext}"
    output_filename = f"{name}_{unique_id}_output{ext}"
    
    input_path = os.path.join(INPUT_DIR, input_filename)
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    file.save(input_path)
    
    script_path = os.path.join(SCRIPT_DIR, "image_enhancer.py")
    
    cmd = [
        "python",
        script_path,
        input_path,
        output_path,
        "--mode",
        mode,
        "--scale",
        scale
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR,
            timeout=300
        )
        
        # Log untuk debugging
        log_path = os.path.join(SCRIPT_DIR, "debug.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Return code: {result.returncode}\n")
            f.write(f"STDOUT:\n{result.stdout}\n")
            f.write(f"STDERR:\n{result.stderr}\n")
        
        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else result.stdout
            return jsonify({'error': f'Proses gagal: {error_msg}'}), 500
        
        if not os.path.exists(output_path):
            error_msg = result.stdout if result.stdout else "File output tidak ditemukan"
            return jsonify({'error': f'Gagal: {error_msg}'}), 500
        
        return jsonify({
            'success': True,
            'output_file': output_filename,
            'message': 'Gambar berhasil diproses!'
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Proses timeout (terlalu lama)'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(OUTPUT_DIR, filename),
        as_attachment=True,
        download_name=f"anjayhd_{filename}"
    )


@app.route('/preview/<filename>')
def preview_file(filename):
    return send_file(
        os.path.join(OUTPUT_DIR, filename)
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

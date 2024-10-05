from flask import Flask, request, jsonify, send_file
import instaloader
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download_profile_picture', methods=['GET'])
def download_profile_picture():
    username = request.args.get('username')
    L = instaloader.Instaloader()

    try:
        # Obtener el perfil
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Verificar el tipo de dato de la URL de la foto de perfil
        profile_pic_url = profile.profile_pic_url
        print(f"Tipo de profile_pic_url: {type(profile_pic_url)}")  # Verificar el tipo de dato
        print(f"URL de la foto de perfil: {profile_pic_url}")  # Verificar el valor de la URL

        # Descargar la foto de perfil
        response = requests.get(profile_pic_url)
        print(f"HTTP Status: {response.status_code}")  # Para depuración

        if response.status_code == 200:
            with open(f"{username}.jpg", "wb") as file:
                file.write(response.content)
            return jsonify({"success": True, "message": f"{username}.jpg"}), 200
        else:
            return jsonify({"success": False, "message": "Error al descargar la foto."}), 400

    except instaloader.exceptions.ProfileNotExistsException:
        return jsonify({"success": False, "message": "El perfil no existe."}), 404
    except Exception as e:
        print(f"Error: {e}")  # Para depuración
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

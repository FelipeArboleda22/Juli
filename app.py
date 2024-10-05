import streamlit as st
import instaloader
import requests

st.title("Descargar Foto de Perfil de Instagram")

# Pedir nombre de usuario de Instagram
username = st.text_input("Introduce el nombre de usuario de Instagram")

# Agrega tus credenciales de Instagram
insta_username = "arboleda.22"
insta_password = "729543816Wp"

if st.button("Descargar"):
    if username:
        # Crear una instancia de Instaloader
        L = instaloader.Instaloader()

        # Iniciar sesión en Instagram
        try:
            L.login(insta_username, insta_password)

            # Obtener el perfil
            profile = instaloader.Profile.from_username(L.context, username)
            profile_pic_url = profile.profile_pic_url

            # Descargar la foto de perfil
            response = requests.get(profile_pic_url)

            if response.status_code == 200:
                with open(f"{username}.jpg", "wb") as file:
                    file.write(response.content)

                st.success(f"Foto de perfil de {username} descargada con éxito.")
                st.image(f"{username}.jpg", caption=f"Foto de perfil de {username}")
            else:
                st.error("Error al descargar la foto de perfil.")
        except instaloader.exceptions.BadCredentialsException:
            st.error("Credenciales de Instagram incorrectas.")
        except instaloader.exceptions.ConnectionException:
            st.error("Error al conectarse a Instagram.")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

import streamlit as st
import instaloader
import requests

st.title("Descargar Foto de Perfil de Instagram")

# Input para el nombre de usuario de Instagram
username = st.text_input("Introduce el nombre de usuario de Instagram")

# Botón para iniciar la descarga
if st.button("Descargar"):
    if username:
        # Crear una instancia de Instaloader
        L = instaloader.Instaloader()
        try:
            # Obtener el perfil y la URL de la foto de perfil
            profile = instaloader.Profile.from_username(L.context, username)
            profile_pic_url = profile.profile_pic_url

            # Realizar la solicitud para descargar la imagen
            response = requests.get(profile_pic_url)

            if response.status_code == 200:
                # Guardar la imagen en un archivo local
                with open(f"{username}.jpg", "wb") as file:
                    file.write(response.content)

                # Mostrar la imagen en Streamlit
                st.success(f"Foto de perfil de {username} descargada con éxito.")
                st.image(f"{username}.jpg", caption=f"Foto de perfil de {username}")
            else:
                st.error("Error al descargar la foto de perfil.")
        except instaloader.exceptions.ProfileNotExistsException:
            st.error(f"El perfil {username} no existe.")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

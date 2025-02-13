import logging
import requests

#Requisição a API
def get_movie_data(movie_title, api_key):
    logging.info(f"Buscando dados para o filme: {movie_title}")
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            logging.info(f"Dados extraídos com sucesso para o filme: {movie_title}")
            return data
        else:
            logging.warning(f"Erro na resposta da API: {data.get('Error')}")
            return None
    except requests.RequestException as e:
        logging.error(f"Erro ao conectar à API: {str(e)}")
        return None

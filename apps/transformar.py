import logging
from datetime import datetime

#Conversão da data para iso8601
def convert_to_iso8601(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date().isoformat()
    except ValueError:
        return "N/A"

#Normalização do nome do filme
def normalize_name(name):
    return ", ".join([word.title() for word in name.split(", ")]) if name != "N/A" else "N/A"

#Calculo de data do lançamento até hoje
def calculate_time_since_release(release_date, unit):
    if release_date == "N/A":
        return "N/A"
    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
    delta = datetime.today().date() - release_date
    if unit == "days":
        return delta.days
    elif unit == "months":
        return delta.days // 30
    elif unit == "years":
        return delta.days // 365
    return "N/A"

#Transformando dados do filme
def transform_movie_data(movie_data):
    logging.info(f"Transformando dados para o filme: {movie_data.get('Title', 'Desconhecido')}")
    release_date = movie_data.get("Released", "N/A")
    release_date_iso = convert_to_iso8601(release_date) if release_date != "N/A" else "N/A"
    genres = [genre.strip() for genre in movie_data.get("Genre", "N/A").split(",")] if movie_data.get("Genre") else []
    
    transformed_data = {
        "Title": normalize_name(movie_data.get("Title", "N/A")),
        "Year": int(movie_data.get("Year", "0")) if movie_data.get("Year", "0").isdigit() else 0,
        "Genres": genres,
        "Director": normalize_name(movie_data.get("Director", "N/A")),
        "Actors": normalize_name(movie_data.get("Actors", "N/A")),
        "IMDB Rating": movie_data.get("imdbRating", "N/A"),
        "Release Date": release_date_iso,
        "Days Since Release": calculate_time_since_release(release_date_iso, "days"),
        "Months Since Release": calculate_time_since_release(release_date_iso, "months"),
        "Years Since Release": calculate_time_since_release(release_date_iso, "years"),
        "Plot": movie_data.get("Plot", "N/A")
    }
    logging.info("Transformação concluída.")
    return transformed_data

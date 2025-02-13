import logging
from apps.extrair import get_movie_data
from apps.transformar import transform_movie_data
from apps.carregar import create_database, save_to_database

#Log de conexão a API
def setup_logging():
    logging.basicConfig(
        filename=r"C:\Users\Erick\Documents\Code\bases\etl_log.log", 
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Lista de filmes a serem inseridos
movie_titles = [
    "The Shawshank Redemption",
    "The Dark Knight",
    "Inception",
    "Fight Club",
    "Pulp Fiction",
    "The Godfather",
    "Inception",
    "Fight Club",
    "Pulp Fiction",
    "The Godfather",
    "Forrest Gump",
    "The Matrix",
    "The Empire Strikes Back",
    "The Lord of the Rings: The Return of the King",
    "Interstellar",
    "Gladiator",
    "The Prestige",
    "The Godfather: Part II",
    "Schindler's List",
    "The Departed",
    "Back to the Future",
    "The Lion King",
    "Spider-Man: No Way Home",
    "The Avengers",
    "Titanic",
    "Star Wars: A New Hope",
    "Jurassic Park",
    "The Dark Knight Rises",
    "The Silence of the Lambs",
    "Saving Private Ryan",
    "Se7en",
    "Goodfellas",
    "The Usual Suspects",
    "Braveheart",
    "The Shining",
    "The Green Mile",
    "The Social Network",
    "The Wolf of Wall Street",
    "The Hunger Games",
    "Avatar",
    "Jaws",
    "Blade Runner",
    "12 Angry Men",
    "The Matrix Reloaded",
    "The Truman Show",
    "The Godfather: Part III",
    "The Big Lebowski",
    "A Clockwork Orange",
    "Gone with the Wind",
    "The Princess Bride",
    "The Breakfast Club",
    "The Grand Budapest Hotel",
    "Mad Max: Fury Road",
    "The Terminator",
    "Abacate"
]



# Main
def main():
    setup_logging()
    logging.info("Iniciando o pipeline ETL de filmes.")
    
    API_KEY = "f6e3f769"
    usuario = "Erick"
    
    create_database()
    # Execução do codigo
    for movie_name in movie_titles:
        try:
            movie_data = get_movie_data(movie_name, API_KEY)
            if movie_data:
                transformed_data = transform_movie_data(movie_data)
                save_to_database(transformed_data, usuario)
                logging.info(f"Filme '{movie_name}' processado e salvo com sucesso.")
            else:
                logging.warning(f"Nenhum dado válido retornado para o filme '{movie_name}'.")
        except Exception as e:
            logging.error(f"Erro no pipeline ETL: {str(e)}")
        
        logging.info("Pipeline ETL finalizado.")
    
if __name__ == "__main__":
    main()

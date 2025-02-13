import logging
import sqlite3
from datetime import datetime

#Criação do banco de dados
def create_database():
    conn = sqlite3.connect(r"C:\Users\Erick\Documents\Code\bases\movies.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Filmes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT,
                        ano INTEGER,
                        dias_lancamento INTEGER,
                        meses_lancamento INTEGER,
                        anos_lancamento INTEGER,
                        diretor TEXT,
                        sinopse TEXT
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Generos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT UNIQUE
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Filme_Genero (
                        filme_id INTEGER,
                        genero_id INTEGER,
                        FOREIGN KEY (filme_id) REFERENCES Filmes(id),
                        FOREIGN KEY (genero_id) REFERENCES Generos(id)
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Log_Insercao (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filme_id INTEGER,
                        usuario TEXT,
                        data_insercao TEXT,
                        FOREIGN KEY (filme_id) REFERENCES Filmes(id)
                    )''')
    
    conn.commit()
    conn.close()

#Verificação se o filme já existe pelo nome
def movie_exists(title):
    conn = sqlite3.connect(r"C:\Users\Erick\Documents\Code\bases\movies.db")
    cursor = conn.cursor()
    
    cursor.execute('''SELECT id FROM Filmes WHERE titulo = ?''', (title,))
    movie = cursor.fetchone()
    
    conn.close()
    
    return movie is not None

#Salvamento de dados
def save_to_database(movie_data, usuario):
    if movie_exists(movie_data["Title"]):
        print("Filme já existe no banco de dados.")
        return
    
    conn = sqlite3.connect(r"C:\Users\Erick\Documents\Code\bases\movies.db")
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO Filmes (titulo, ano, dias_lancamento, meses_lancamento, anos_lancamento, diretor, sinopse)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                          movie_data["Title"],
                          movie_data["Year"],
                          movie_data["Days Since Release"],
                          movie_data["Months Since Release"],
                          movie_data["Years Since Release"],
                          movie_data["Director"],
                          movie_data["Plot"]
                      ))
    
    filme_id = cursor.lastrowid
    
    for genre in movie_data["Genres"]:
        cursor.execute("INSERT OR IGNORE INTO Generos (nome) VALUES (?)", (genre,))
        cursor.execute("SELECT id FROM Generos WHERE nome = ?", (genre,))
        genero_id = cursor.fetchone()[0]
        
        cursor.execute("INSERT INTO Filme_Genero (filme_id, genero_id) VALUES (?, ?)", (filme_id, genero_id))
    
    data_insercao_iso = datetime.now().isoformat()
    cursor.execute('''INSERT INTO Log_Insercao (filme_id, usuario, data_insercao)
                      VALUES (?, ?, ?)''', (filme_id, usuario, data_insercao_iso))
    
    conn.commit()
    conn.close()
    logging.info(f"Filme '{movie_data['Title']}' salvo no banco de dados com sucesso.")

# create_schema.py
import sqlite3

# conectando...
conn = sqlite3.connect('base.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE consultas (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        texto  VARCHAR(200) NOT NULL,
        tipo  VARCHAR(50) NOT NULL,
        criado_em DATE NOT NULL
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()
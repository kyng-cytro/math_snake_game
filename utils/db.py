import sqlite3

conn = sqlite3.connect('highscores.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER,
        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()


def get_top_3_scores():
    conn = sqlite3.connect('highscores.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players ORDER BY score DESC LIMIT 3')
    top_3_scores = cursor.fetchall()
    conn.close()
    return top_3_scores


def add_new_high_score(score):
    conn = sqlite3.connect('highscores.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO players (score) VALUES (?)', (score,))
    conn.commit()
    conn.close()


def is_high_score(score):
    if score == 0:
        return False
    top_3_scores = get_top_3_scores()
    if not top_3_scores:
        return True
    return score > top_3_scores[0][1]

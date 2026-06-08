import sqlite3

# ==================== ЗАДАНИЕ 1-2: ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ ====================
print("=" * 50)
print("ЗАДАНИЕ 1-2: Подключение к базе данных")
print("=" * 50)

# Подключаемся к базе данных (файл mybase.db)
conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()

print("База данных создана и подключена!")


# ==================== ЗАДАНИЕ 3: СОЗДАНИЕ ТАБЛИЦЫ ====================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 3: Создание таблицы users")
print("=" * 50)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')
conn.commit()
print("Таблица users создана!")


# ==================== ЗАДАНИЕ 4: ДОБАВЛЕНИЕ ДАННЫХ (INSERT) ====================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 4: Добавление данных (INSERT)")
print("=" * 50)

# Добавляем одного пользователя
cursor.execute('''
    INSERT INTO users (name, age) VALUES (?, ?)
''', ('Анна', 25))

# Добавляем нескольких пользователей
users = [
    ('Иван', 30),
    ('Мария', 22),
    ('Петр', 35)
]
cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users)

conn.commit()
print("Пользователи добавлены!")


# ==================== ЗАДАНИЕ 5: ЧТЕНИЕ ДАННЫХ (SELECT) ====================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 5: Чтение данных (SELECT)")
print("=" * 50)

cursor.execute('SELECT * FROM users')
all_users = cursor.fetchall()

print("--- Все пользователи ---")
for user in all_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")


# ==================== ЗАДАНИЕ 6: ЧТЕНИЕ С УСЛОВИЕМ (WHERE) ====================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 6: Чтение с условием (WHERE)")
print("=" * 50)

cursor.execute('SELECT * FROM users WHERE age > 25')
older_users = cursor.fetchall()

print("--- Пользователи старше 25 ---")
for user in older_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")


# ==================== ЗАДАНИЕ 7: ИЗМЕНЕНИЕ ДАННЫХ (UPDATE) ====================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 7: Изменение данных (UPDATE)")
print("=" * 50)

cursor.execute('UPDATE users SET age = age + 1')
conn.commit()

cursor.execute('SELECT * FROM users')
updated_users = cursor.fetchall()

print("--- После увеличения возраста на 1 год ---")
for user in updated_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")


# ==================== ЗАДАНИЕ 8: УДАЛЕНИЕ ДАННЫХ (DELETE) ====================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 8: Удаление данных (DELETE)")
print("=" * 50)

cursor.execute('DELETE FROM users WHERE id = ?', (2,))
conn.commit()

cursor.execute('SELECT * FROM users')
remaining_users = cursor.fetchall()

print("--- После удаления id=2 ---")
for user in remaining_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")


# ==================== ЗАДАНИЕ 9: ЗАКРЫТИЕ СОЕДИНЕНИЯ ====================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 9: Закрытие соединения")
print("=" * 50)

conn.close()
print("Соединение закрыто.")


# ==================== ЗАДАНИЕ 10-17: ВТОРОЕ СОЕДИНЕНИЕ ДЛЯ ТАБЛИЦЫ products ====================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 10-17: Работа с таблицей products")
print("=" * 50)

# Открываем новое соединение
conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()

# ЗАДАНИЕ 10: Создание таблицы products
print("\n--- Задание 10: Создание таблицы products ---")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER DEFAULT 0
    )
''')
conn.commit()
print("Таблица products создана!")

# ЗАДАНИЕ 11: Добавление товаров
print("\n--- Задание 11: Добавление товаров ---")
products = [
    ('Яблоки', 50, 100),
    ('Бананы', 80, 50),
    ('Молоко', 70, 30),
    ('Хлеб', 40, 0),
    ('Сыр', 150, 20)
]
cursor.executemany('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', products)
conn.commit()
print("Товары добавлены!")

# ЗАДАНИЕ 12: Вывод всех товаров
print("\n--- Задание 12: Все товары ---")
cursor.execute('SELECT * FROM products')
all_products = cursor.fetchall()
for product in all_products:
    print(f"{product[0]}. {product[1]} - {product[2]} руб, в наличии: {product[3]}")

# ЗАДАНИЕ 13: Товары с ценой меньше 100 рублей
print("\n--- Задание 13: Товары с ценой меньше 100 рублей ---")
cursor.execute('SELECT * FROM products WHERE price < 100')
cheap_products = cursor.fetchall()
for product in cheap_products:
    print(f"{product[1]} - {product[2]} руб")

# ЗАДАНИЕ 14: Товары, которых нет в наличии (quantity = 0)
print("\n--- Задание 14: Товары, которых нет в наличии ---")
cursor.execute('SELECT * FROM products WHERE quantity = 0')
out_of_stock = cursor.fetchall()
for product in out_of_stock:
    print(f"{product[1]}")

# ЗАДАНИЕ 15: Увеличение цены на 10 рублей
print("\n--- Задание 15: Увеличение цены всех товаров на 10 рублей ---")
cursor.execute('UPDATE products SET price = price + 10')
conn.commit()

cursor.execute('SELECT * FROM products')
updated_products = cursor.fetchall()
print("Товары с новыми ценами:")
for product in updated_products:
    print(f"{product[1]} - {product[2]} руб")

# ЗАДАНИЕ 16: Удаление товаров с ценой выше 100 рублей
print("\n--- Задание 16: Удаление товаров с ценой выше 100 рублей ---")
cursor.execute('DELETE FROM products WHERE price > 100')
conn.commit()

cursor.execute('SELECT * FROM products')
remaining_products = cursor.fetchall()
print("Оставшиеся товары:")
for product in remaining_products:
    print(f"{product[1]} - {product[2]} руб")

# ЗАДАНИЕ 17: Добавление поля category
print("\n--- Задание 17: Добавление поля category ---")
try:
    cursor.execute('ALTER TABLE products ADD COLUMN category TEXT DEFAULT "другое"')
    conn.commit()
    print("Поле category добавлено!")
except sqlite3.OperationalError:
    print("Поле category уже существует")

# Обновляем категории
categories = [
    ('фрукты', 'Яблоки'),
    ('фрукты', 'Бананы'),
    ('молочные', 'Молоко'),
    ('выпечка', 'Хлеб')
]
for category, name in categories:
    cursor.execute('UPDATE products SET category = ? WHERE name = ?', (category, name))
conn.commit()

# Проверяем результат
print("\n--- Товары с категориями ---")
cursor.execute('SELECT name, price, category FROM products')
final_products = cursor.fetchall()
for product in final_products:
    print(f"{product[0]} - {product[1]} руб, категория: {product[2]}")

# Закрываем соединение
conn.close()
print("\nСоединение закрыто.")


# ==================== ВОПРОСЫ ДЛЯ ПРОВЕРКИ ====================
print("\n" + "=" * 50)
print("ВОПРОСЫ ДЛЯ ПРОВЕРКИ ЗНАНИЙ")
print("=" * 50)

questions = [
    "1. Как подключиться к базе данных SQLite в Python?",
    "2. Что делает cursor.execute()?",
    "3. Зачем нужен conn.commit()?",
    "4. Что означает ? в запросе INSERT INTO users (name, age) VALUES (?, ?)?",
    "5. Как получить все строки из таблицы?",
    "6. Чем отличается fetchone() от fetchall()?",
    "7. Как обновить данные в таблице?",
    "8. Как удалить данные из таблицы?"
]

answers = [
    "→ sqlite3.connect('имя_файла.db')",
    "→ Выполняет SQL-запрос к базе данных",
    "→ Сохраняет (фиксирует) изменения в базе данных",
    "→ Это заполнитель (placeholder) для безопасной подстановки значений, защищает от SQL-инъекций",
    "→ cursor.fetchall()",
    "→ fetchone() возвращает одну строку, fetchall() возвращает все строки",
    "→ UPDATE название_таблицы SET поле = новое_значение WHERE условие",
    "→ DELETE FROM название_таблицы WHERE условие"
]

for i, (q, a) in enumerate(zip(questions, answers)):
    print(f"\n{q}")
    print(f"{a}")
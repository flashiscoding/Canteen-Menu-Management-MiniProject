from flask import Flask, render_template_string, request, redirect
import mysql.connector

app = Flask(__name__)

from config import DB_CONFIG  # your local DB login (not uploaded to GitHub)


def run(query, params=(), fetch=False):
    """Open connection, run one query, close. Simple and good enough for a mini project."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    result = cur.fetchall() if fetch else None
    conn.commit()
    cur.close()
    conn.close()
    return result


PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Canteen Menu</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; background: #f4ead8; color: #3b2a1a; font-family: Georgia, "Times New Roman", serif; }
    .wrap { max-width: 760px; margin: 0 auto; padding: 24px 16px 60px; }
    header { text-align: center; padding: 28px 0 18px; border-bottom: 3px double #8a5a2b; margin-bottom: 26px; }
    header small { letter-spacing: 4px; text-transform: uppercase; color: #8a5a2b; font-size: 13px; }
    header h1 { font-size: 46px; margin: 6px 0 2px; font-weight: normal; letter-spacing: 2px; }
    header p { margin: 0; font-style: italic; color: #7a6048; }
    .manage-btn { margin-top: 14px; background: none; border: 1px solid #8a5a2b; color: #8a5a2b;
                  padding: 6px 16px; border-radius: 20px; cursor: pointer; font-family: inherit; font-size: 14px; }
    .manage-btn:hover { background: #8a5a2b; color: #fff; }

    .card { background: #fffaf0; border: 1px solid #e2d2b4; border-radius: 10px; padding: 18px 22px; margin-bottom: 22px;
            box-shadow: 0 2px 6px rgba(80,50,20,.08); }
    .card h2 { margin: 0 0 12px; font-size: 24px; font-weight: normal; color: #8a5a2b; text-align: center;
               letter-spacing: 3px; text-transform: uppercase; }
    .card h2::after { content: ""; display: block; width: 60px; height: 2px; background: #c9a36a; margin: 8px auto 0; }

    .item { display: flex; align-items: baseline; gap: 8px; padding: 9px 0; }
    .item .name { font-size: 18px; }
    .item .dots { flex: 1; border-bottom: 2px dotted #c9b48e; transform: translateY(-4px); }
    .item .price { font-size: 18px; font-weight: bold; }
    .item.soldout .name, .item.soldout .price { text-decoration: line-through; color: #a89880; }
    .badge { font-size: 11px; background: #b42318; color: #fff; padding: 2px 8px; border-radius: 10px;
             letter-spacing: 1px; text-transform: uppercase; font-family: Arial, sans-serif; }

    .actions { display: none; font-family: Arial, sans-serif; font-size: 12px; gap: 8px; }
    body.manage .actions { display: flex; }
    form { margin: 0; }
    .actions button { border: none; background: #efe2c6; color: #3b2a1a; padding: 4px 9px; border-radius: 6px; cursor: pointer; }
    .actions button.del { background: #f6d5d1; color: #b42318; }

    .add { display: none; }
    body.manage .add { display: block; }
    .add form { display: flex; gap: 8px; flex-wrap: wrap; }
    .add input, .add select { flex: 1; min-width: 120px; padding: 10px; border: 1px solid #d6c3a0; border-radius: 6px;
                              font-family: inherit; font-size: 15px; background: #fff; }
    .add button { padding: 10px 20px; background: #8a5a2b; color: #fff; border: none; border-radius: 6px;
                  font-family: inherit; font-size: 15px; cursor: pointer; }
    .empty { text-align: center; color: #7a6048; font-style: italic; }
    footer { text-align: center; color: #7a6048; font-size: 13px; margin-top: 30px; font-style: italic; }
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <small>Fresh &bull; Hot &bull; Affordable</small>
      <h1>The Canteen</h1>
      <p>Today's Menu</p>
      <button class="manage-btn" onclick="document.body.classList.toggle('manage')">Manage menu</button>
    </header>

    <div class="card add">
      <h2>Add an item</h2>
      <form method="post" action="/add">
        <input name="name" placeholder="Item name" required>
        <input name="price" type="number" step="0.01" min="0.01" placeholder="Price (&#8377;)" required>
        <select name="category_id" required>
          {% for c in categories %}<option value="{{ c.category_id }}">{{ c.name }}</option>{% endfor %}
        </select>
        <button type="submit">Add</button>
      </form>
    </div>

    {% for cat, items in menu.items() %}
    <div class="card">
      <h2>{{ cat }}</h2>
      {% for i in items %}
      <div class="item {{ '' if i.available else 'soldout' }}">
        <span class="name">{{ i.name }}</span>
        {% if not i.available %}<span class="badge">Sold out</span>{% endif %}
        <span class="dots"></span>
        <span class="price">&#8377;{{ '%g' % i.price }}</span>
        <div class="actions">
          <form method="post" action="/toggle/{{ i.item_id }}">
            <button>{{ 'Sold out' if i.available else 'Restock' }}</button>
          </form>
          <form method="post" action="/delete/{{ i.item_id }}" onsubmit="return confirm('Delete this item?')">
            <button class="del">Delete</button>
          </form>
        </div>
      </div>
      {% endfor %}
    </div>
    {% else %}
    <p class="empty">The menu is empty. Click "Manage menu" to add items.</p>
    {% endfor %}

    <footer>Canteen Menu Management System &mdash; DBMS Mini Project</footer>
  </div>
</body>
</html>
"""


@app.route("/")
def index():
    items = run(
        """SELECT m.item_id, m.name, m.price, c.name AS category, m.available
           FROM menu_items m JOIN categories c ON m.category_id = c.category_id
           ORDER BY c.name, m.name""",
        fetch=True,
    )
    categories = run("SELECT * FROM categories ORDER BY name", fetch=True)
    menu = {}
    for i in items:
        menu.setdefault(i["category"], []).append(i)
    return render_template_string(PAGE, menu=menu, categories=categories)


@app.route("/add", methods=["POST"])
def add():
    run(
        "INSERT INTO menu_items (name, price, category_id) VALUES (%s, %s, %s)",
        (request.form["name"], request.form["price"], request.form["category_id"]),
    )
    return redirect("/")


@app.route("/toggle/<int:item_id>", methods=["POST"])
def toggle(item_id):
    run("UPDATE menu_items SET available = NOT available WHERE item_id = %s", (item_id,))
    return redirect("/")


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete(item_id):
    run("DELETE FROM menu_items WHERE item_id = %s", (item_id,))
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5001)

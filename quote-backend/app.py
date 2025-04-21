from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)

CORS(app, origins="*")

quotes = {
    "philosophy": [
        {"quote": "The unexamined life is not worth living.", "author": "Socrates"},
        {"quote": "I think, therefore I am.", "author": "René Descartes"},
        {"quote": "He who thinks great thoughts, often makes great errors.", "author": "Martin Heidegger"},
        {"quote": "One cannot step twice in the same river.", "author": "Heraclitus"},
        {"quote": "Happiness is the highest good.", "author": "Aristotle"},
        {"quote": "Man is condemned to be free.", "author": "Jean-Paul Sartre"},
        {"quote": "To be is to be perceived.", "author": "George Berkeley"},
        {"quote": "Liberty consists in doing what one desires.", "author": "John Stuart Mill"},
        {"quote": "God is dead. God remains dead. And we have killed him.", "author": "Friedrich Nietzsche"},
        {"quote": "The only thing I know is that I know nothing.", "author": "Socrates"},
        {"quote": "Life must be understood backward. But it must be lived forward.", "author": "Søren Kierkegaard"},
        {"quote": "Freedom is the recognition of necessity.", "author": "Georg Wilhelm Friedrich Hegel"},
        {"quote": "Even while they teach, men learn.", "author": "Seneca"},
        {"quote": "The greatest happiness of the greatest number is the foundation of morals and legislation.", "author": "Jeremy Bentham"},
        {"quote": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "author": "Aristotle"},
        {"quote": "That which does not kill us makes us stronger.", "author": "Friedrich Nietzsche"},
        {"quote": "Hell is other people.", "author": "Jean-Paul Sartre"},
        {"quote": "No man's knowledge here can go beyond his experience.", "author": "John Locke"},
        {"quote": "Happiness lies in virtuous activity, and perfect happiness lies in the best activity, which is contemplative.", "author": "Aristotle"},
        {"quote": "Time is a moving image of eternity.", "author": "Plato"}
    ],
    "humor": [
        {"quote": "I'm not arguing, I'm just explaining why I'm right.", "author": "Unknown"},
        {"quote": "I'm on a whiskey diet. I've lost three days already.", "author": "Tommy Cooper"},
        {"quote": "Why don’t scientists trust atoms? Because they make up everything!", "author": "Unknown"},
        {"quote": "I can resist everything except temptation.", "author": "Oscar Wilde"},
        {"quote": "I used to think I was indecisive, but now I'm not so sure.", "author": "Unknown"},
        {"quote": "A day without laughter is a day wasted.", "author": "Charlie Chaplin"},
        {"quote": "Behind every great man is a woman rolling her eyes.", "author": "Jim Carrey"},
        {"quote": "If you think nobody cares if you're alive, try missing a couple of payments.", "author": "Earl Wilson"},
        {"quote": "I'm not superstitious, but I am a little stitious.", "author": "Michael Scott"},
        {"quote": "You can't have everything. Where would you put it?", "author": "Steven Wright"},
        {"quote": "If at first you don't succeed, then skydiving definitely isn't for you.", "author": "Steven Wright"},
        {"quote": "I intend to live forever. So far, so good.", "author": "Steven Wright"},
        {"quote": "The road to success is always under construction.", "author": "Lily Tomlin"},
        {"quote": "Age is of no importance unless you're a cheese.", "author": "Billie Burke"},
        {"quote": "People say nothing is impossible, but I do nothing every day.", "author": "A.A. Milne (Winnie the Pooh)"},
        {"quote": "Light travels faster than sound. This is why some people appear bright until you hear them speak.", "author": "Alan Dundes"},
        {"quote": "To steal ideas from one person is plagiarism; to steal from many is research.", "author": "Wilson Mizner"},
        {"quote": "I always wanted to be somebody, but now I realize I should have been more specific.", "author": "Lily Tomlin"},
        {"quote": "Insanity is hereditary; you get it from your children.", "author": "Sam Levenson"},
        {"quote": "A clear conscience is usually the sign of a bad memory.", "author": "Steven Wright"}
    ],
    "random": [
        {"quote": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde"},
        {"quote": "You only live once, but if you do it right, once is enough.", "author": "Mae West"},
        {"quote": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
        {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
        {"quote": "Do not go where the path may lead, go instead where there is no path and leave a trail.", "author": "Ralph Waldo Emerson"},
        {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"quote": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
        {"quote": "Not all those who wander are lost.", "author": "J.R.R. Tolkien"},
        {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
        {"quote": "You miss 100% of the shots you don't take.", "author": "Wayne Gretzky"},
        {"quote": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson"},
        {"quote": "Act as if what you do makes a difference. It does.", "author": "William James"},
        {"quote": "Whether you think you can or you think you can’t, you’re right.", "author": "Henry Ford"},
        {"quote": "Everything you can imagine is real.", "author": "Pablo Picasso"},
        {"quote": "It always seems impossible until it’s done.", "author": "Nelson Mandela"},
        {"quote": "Do what you can, with what you have, where you are.", "author": "Theodore Roosevelt"},
        {"quote": "Strive not to be a success, but rather to be of value.", "author": "Albert Einstein"},
        {"quote": "Dream big and dare to fail.", "author": "Norman Vaughan"},
        {"quote": "The best way out is always through.", "author": "Robert Frost"},
        {"quote": "Change your thoughts and you change your world.", "author": "Norman Vincent Peale"}
    ]
}



@app.route('/quote/<category>')
def get_route(category):
    if category == "all":
        all_quotes = [q for quotes_list in quotes.values() for q in quotes_list]
        return jsonify({"quote": random.choice(all_quotes)})
    else:
        category_quotes = quotes.get(category, quotes["random"])
        return jsonify({"quote": random.choice(category_quotes)})


@app.route('/quotes')
def get_all_quotes():
    all_quotes = []
    for category, items in quotes.items():
        for q in items:
            all_quotes.append({**q, "category": category})
    return jsonify(all_quotes)

if __name__ == '__main__':
    app.run(debug=True)
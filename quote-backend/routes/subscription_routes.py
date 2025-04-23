from flask import Blueprint, jsonify, request
# from models import Quote 
# # Import the Quote class from models.py when the database is set up and the subscriber model is created

# from app import db

# Again, db is imported from app.py after db is defined in app.py

from data.quotes_data import quotes

# Blueprint for subscription routes

subscription_routes = Blueprint('subscription_routes', __name__)

subscribers = []


@subscription_routes.route('/api/search', methods=['GET'])
def search_quotes():
    query = request.args.get('q', '').lower()
    results = []

    for category, quote_list in quotes.items():
        for quote in quote_list:
            if query in quote["quote"].lower() or query in quote["author"].lower():
                results.append({
                    "quote": quote["quote"],
                    "author": quote["author"],
                    "category": category
                })

    return jsonify({
        "success": True,
        "count": len(results),
        "quotes": results
    })

@subscription_routes.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    if email not in subscribers:
        subscribers.append(email)
        return jsonify({"message": "You have successfully subscribed to our newsletter!"})
    else:
        return jsonify({"message": "You are already subscribed to our newsletter."})
    
# Route for unsubscribing from a quote via form

@subscription_routes.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.form['email']
    if email in subscribers:
        subscribers.remove(email)
        return jsonify({"message": "Unsubscribed successfully."})
    else:
        return jsonify({"message": "You were not suscribed to our newsletter."})
    
# Search function for server-side search

# @subscription_routes.route('/search', methods=['GET'])
# def search_quotes():
#     query = request.args.get('q', '')
#     search_type = request.args.get('type', 'all')

#     if not query:
#         return jsonify({'quotes': []}), 200
    
#     try:
#         if search_type == 'quote':
#             quotes = Quote.query.ilike(f'%{query}%').all()
#         elif search_type == 'author':
#             quotes = Quote.query.ilike(f'%{query}%').all()
#         elif search_type == 'category':
#             quotes = Quote.query.ilike(f'%{query}%').all()
#         else:
#             quotes = Quote.query.filter(Quote.quote.ilike(f'%{query}%') | Quote.author.ilike(f'%{query}%') | Quote.category.ilike(f'%{query}%')).all()

#         result = [quote.to_dict() for quote in quotes]

#         return jsonify({
#             'success': True,
#             'quotes': result,
#             'count': len(result)
#         }), 200
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
    
# Route to get categories of quotes
# @subscription_routes.route('/api/quotes/categories', methods=['GET'])
# def get_categories():
#     try:
#         categories = db.session.query(Quote.category).distinct().all()
#         category_list = [cat[0] for cat in categories if cat[0]]
        
#         return jsonify({
#             'success': True,
#             'categories': category_list
#         }), 200
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 500
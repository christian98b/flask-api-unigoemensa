def bot_meals_reply(meals:dict):
    reply = f"Am {meals['date']} gibt es in der {meals['location']}:\n\n"
    for meal in meals['meals']:
        reply += f"_{meal['type']}:_\n *{meal['name']}*\n"
        reply += f"Zutaten: {meal['meal_ingredients']}\n"
        if meal['content'] != '':
            reply += f"Angebot: {meal['content']}\n\n"
        else:
            reply += "\n"
    return reply
def bot_meals_reply(meals:dict):
    reply = f"Am {meals['date']} gibt es in der {meals['location']}:\n\n"
    for meal in meals['meals']:
        if meal['name'] != '':
            reply += f"_{meal['type']}:_\n *{meal['name']}*\n\n"
        if meal['meal_ingredients'] != '':
            reply += f"Zutaten: {meal['meal_ingredients']}\n"
        if meal['content'] != 'Mittagsangebot' or meal['content'] != '':
            reply += f"Angebot: {meal['content']}\n\n"
        reply += "--------------------"
    return reply
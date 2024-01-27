from flask import Flask, render_template
from clash_royale_library import ClashRoyaleCard, get_card_info

app = Flask(__name__)

# Route to display card information
@app.route('/')
def display_card_info():
    card_info1 = get_card_info(electro_dragon)
    card_info2 = get_card_info(fireball_blaster)
    return render_template('index.html', card_info1=card_info1, card_info2=card_info2)

if __name__ == '__main__':
    app.run(debug=True)
import tkinter as tk
import random

CARD_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
               'J': 10, 'Q': 10, 'K': 10, 'A': 11}
deck = []
player_hand = []
dealer_hand = []
game_over = False

root = None
dealer_label = None
player_label = None
prob_label = None
hit_button = None
stay_button = None


def initialize_deck():
    global deck
    deck = list(CARD_VALUES.keys()) * 8
    random.shuffle(deck)



def calculate_hand_value(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    aces = hand.count('A')

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value


def monte_carlo_simulation(trials=10000):
    results = {'Win': 0, 'Loss': 0, 'Tie': 0}

    for _ in range(trials):
        temp_deck = deck[:]
        temp_player_hand = player_hand[:]
        temp_dealer_hand = dealer_hand[:]

        while calculate_hand_value(temp_player_hand) < 17:
            temp_player_hand.append(random.choice(temp_deck))

        player_score = calculate_hand_value(temp_player_hand)
        if player_score > 21:
            results['Loss'] += 1
            continue

        while calculate_hand_value(temp_dealer_hand) < 17:
            temp_dealer_hand.append(random.choice(temp_deck))

        dealer_score = calculate_hand_value(temp_dealer_hand)

        if dealer_score > 21:
            results['Win'] += 1
        elif player_score > dealer_score:
            results['Win'] += 1
        elif player_score < dealer_score:
            results['Loss'] += 1
        else:
            results['Tie'] += 1

    total_games = sum(results.values())
    percentages = {key: round((results[key] / total_games) * 100, 2) for key in results}

    return percentages


def update_display():
    dealer_text = f"Dealer's Hand: {' '.join(dealer_hand)} (Value: {calculate_hand_value(dealer_hand)})" \
        if game_over else f"Dealer's Hand: {dealer_hand[0]} ??"
    dealer_label.config(text=dealer_text)

    player_label.config(
        text=f"Your Hand: {' '.join(player_hand)} (Value: {calculate_hand_value(player_hand)})")

    if not game_over:
        probabilities = monte_carlo_simulation()
        prob_label.config(
            text=f"Win Probability: {probabilities['Win']}%\n"
                 f"Loss Probability: {probabilities['Loss']}%\n"
                 f"Tie Probability: {probabilities['Tie']}%"
        )


def hit():
    global game_over
    if not game_over:
        player_hand.append(deck.pop())
        if calculate_hand_value(player_hand) > 21:
            game_over = True
            end_game("You bust! Dealer wins!")
        update_display()


def stay():
    global game_over
    if not game_over:
        game_over = True
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())
        update_display()
        check_winner()


def check_winner():
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value > 21 or player_value > dealer_value:
        end_game("You win!")
    elif dealer_value > player_value:
        end_game("Dealer wins!")
    else:
        end_game("It's a tie!")


def end_game(message):
    prob_label.config(text=message)
    hit_button.config(state=tk.DISABLED)
    stay_button.config(state=tk.DISABLED)


def new_game():
    global game_over, player_hand, dealer_hand
    initialize_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    game_over = False
    hit_button.config(state=tk.NORMAL)
    stay_button.config(state=tk.NORMAL)
    update_display()



def setup_gui():
    global root, dealer_label, player_label, prob_label, hit_button, stay_button

    root = tk.Tk()
    root.title("Blackjack")
    root.geometry("800x600")

    main_frame = tk.Frame(root, bg="dark green")
    main_frame.pack(expand=True, fill="both")

    dealer_label = tk.Label(main_frame, text="Dealer's Hand:", bg='dark green', fg="white",
                            font=("Times new roman", 13))
    dealer_label.pack()

    player_label = tk.Label(main_frame, text="Your Hand:", bg='dark green', fg="white",
                            font=("Times new roman", 13))
    player_label.pack()

    prob_label = tk.Label(main_frame, text="", bg='dark green', fg="white", font=("Times new roman", 13))
    prob_label.pack(pady=10)

    button_frame = tk.Frame(main_frame, bg="dark green")
    button_frame.pack(pady=10)

    hit_button = tk.Button(button_frame, text="Hit", command=hit, font=("Times new roman", 13))
    hit_button.pack(side=tk.LEFT, padx=10)

    stay_button = tk.Button(button_frame, text="Stay", command=stay, font=("Times new roman", 13))
    stay_button.pack(side=tk.LEFT, padx=10)

    new_game_button = tk.Button(button_frame, text="New Game", command=new_game, font=("Times new roman", 13))
    new_game_button.pack(side=tk.LEFT, padx=10)

    new_game()


setup_gui()
root.mainloop()

import streamlit as st
import random
import time

def initialize_game_state():
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 3
    if 'numbers' not in st.session_state:
        st.session_state.numbers = []
    if 'game_phase' not in st.session_state:
        st.session_state.game_phase = 'start'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'show_numbers' not in st.session_state:
        st.session_state.show_numbers = False

def generate_numbers(level):
    return [random.randint(1, 99) for _ in range(level)]

def check_answer():
    try:
        player_numbers = [int(num) for num in st.session_state.guess.split()]
        if player_numbers == st.session_state.numbers:
            st.session_state.current_level += 1
            st.session_state.game_phase = 'memorize'
            st.session_state.numbers = generate_numbers(st.session_state.current_level)
        else:
            st.session_state.game_over = True
    except ValueError:
        st.session_state.error = "Please enter valid numbers separated by spaces"

def main():
    st.title("Number Memory Game")
    initialize_game_state()
    
    # Start screen
    if st.session_state.game_phase == 'start':
        st.write("Welcome to the Number Memory Game!")
        if st.button("Start"):
            st.session_state.numbers = generate_numbers(st.session_state.current_level)
            st.session_state.show_numbers = True
            st.session_state.game_phase = 'memorize'
            st.write("Are you sure?")

    # Memorize phase
    elif st.session_state.game_phase == 'memorize':
        st.write(f"Level {st.session_state.current_level - 2}")
        st.write("Memorize these numbers:")
        
        # Display numbers
        st.write(st.session_state.numbers)
        
        # Create placeholder and start countdown immediately
        placeholder = st.empty()
        for secs in range(3, 0, -1):
            placeholder.metric("Time Remaining", f"{secs} seconds")
            time.sleep(1)
        placeholder.empty()
        st.session_state.show_numbers = False
        st.session_state.game_phase = 'guess'
        st.rerun()

    # Guess phase
    elif st.session_state.game_phase == 'guess':
        st.write(f"Level {st.session_state.current_level - 2}")
        st.write("Enter the numbers you saw, separated by spaces:")
        
        # Use a key to maintain the answer between reruns
        st.text_input("Your answer:", key="guess")
        
        if st.button("Submit", on_click=check_answer):
            if st.session_state.game_over:
                st.error(f"Wrong! The correct sequence was: {st.session_state.numbers}")
            elif st.session_state.game_phase == 'memorize':
                st.success("Correct! Moving to next level...")
                st.rerun()
            elif hasattr(st.session_state, 'error'):
                st.error(st.session_state.error)

    if st.session_state.game_over:
        st.write(f"Game Over! You reached Level {st.session_state.current_level - 2}")
        if st.button("Play Again"):
            st.session_state.current_level = 3
            st.session_state.game_phase = 'start'
            st.session_state.game_over = False
            st.rerun()

if __name__ == "__main__":
    main()
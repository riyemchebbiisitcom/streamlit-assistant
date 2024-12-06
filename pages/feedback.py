import streamlit as st
from streamlit_lottie import st_lottie
import json
import csv
import os

# Function to load Lottie JSON file
def load_lottiefile(filepath: str):
    """Load a Lottie animation file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading animation file: {e}")
        return None

# Load animations
def load_animations(base_path="animations"):
    """Load animations from the specified base path."""
    animations = {
        "happy": os.path.join(base_path, "happy_animation.json"),
        "surprised": os.path.join(base_path, "surprised_animation.json"),
        "loading": os.path.join(base_path, "drop.json"),
    }
    return {key: load_lottiefile(path) for key, path in animations.items()}

# Display the feedback form
st.title("Chatbot Feedback Form")
st.write("Please share your experience with our chatbot.")

# Collect user information
name = st.text_input("Your Name")
email = st.text_input("Your Email")

# Collect feedback about the chatbot
rating = st.slider("Rate your overall experience with the chatbot (0 = Poor, 10 = Excellent)", 0, 10)
ease_of_use = st.slider("How easy was it to use the chatbot? (0 = Very Difficult, 10 = Very Easy)", 0, 10)
response_quality = st.slider("How would you rate the chatbot's response quality? (0 = Poor, 10 = Excellent)", 0, 10)
speed = st.slider("How would you rate the chatbot's response speed? (0 = Slow, 10 = Fast)", 0, 10)

features_liked = st.text_area("What features or aspects of the chatbot did you like the most?")
improvements = st.text_area("What specific improvements would you suggest for the chatbot?")
issues_faced = st.text_area("Did you face any issues while using the chatbot? If yes, please describe.")
preferred_features = st.text_area("What additional features would you like to see in the chatbot?")
compared_to_humans = st.radio(
    "How does the chatbot compare to interacting with a human?",
    options=["Better", "Similar", "Worse"],
)
recommendation = st.radio("Would you recommend this chatbot to others?", options=["Yes", "No"])
return_usage = st.radio("Would you use this chatbot again?", options=["Yes", "No"])

# Load animations
animations = load_animations()

# Submit button
if st.button("Submit Feedback"):
    # Show a loading animation while processing
    if animations["loading"]:
        st_lottie(animations["loading"], height=300, key="loading")

    # Show appropriate animation based on rating
    if rating >= 8:
        if animations["happy"]:
            st_lottie(animations["happy"], height=300, key="happy_face")
        st.success(f"Thank you, {name}! We're glad you had a great experience! 😊")
    elif rating <= 4:
        if animations["surprised"]:
            st_lottie(animations["surprised"], height=300, key="surprised_face")
        st.warning(f"Sorry to hear that, {name}. We’ll work on improving the chatbot. 😔")
    else:
        st.info("Thank you for your feedback!")

    # Save feedback to a CSV file
    file_name = "chatbot_feedback.csv"
    file_exists = os.path.isfile(file_name)
    try:
        with open(file_name, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                # Write header if file doesn't exist
                writer.writerow([
                    "Name", "Email", "Rating", "Ease of Use", "Response Quality", "Response Speed",
                    "Features Liked", "Improvements", "Issues Faced", "Preferred Features",
                    "Compared to Humans", "Recommendation", "Return Usage",
                ])
            # Write user feedback
            writer.writerow([
                name, email, rating, ease_of_use, response_quality, speed,
                features_liked, improvements, issues_faced, preferred_features,
                compared_to_humans, recommendation, return_usage,
            ])
        st.success("Your feedback has been successfully saved!")
    except Exception as e:
        st.error(f"An error occurred while saving your feedback: {e}")
        
        
import random
 

# List of water facts
water_facts = [
    "It takes about 1,800 gallons of water to produce a single pair of jeans!",
    "Turning off the tap while brushing your teeth can save up to 8 gallons of water per day.",
    "Less than 1% of the water on Earth is drinkable.",
    "A 10-minute shower uses 25 gallons of water on average.",
    "Fixing a leaky faucet can save up to 3,000 gallons of water per year.",
    "It takes about 1,800 gallons of water to produce a single pair of jeans!",
    "Turning off the tap while brushing your teeth can save up to 8 gallons of water per day.",
    "A 10-minute shower uses 25 gallons of water on average.",
    "Fixing a leaky faucet can save up to 3,000 gallons of water per year.",
    "The human body is made up of approximately 60% water.",
    "A person can survive for about 3 days without water.",
    "The United Nations declared access to clean water a human right in 2010.",
    "An average American household uses 300 gallons of water daily.",
    "Fixing a leaky faucet can save over 3,000 gallons of water annually.",
    "Turning off the tap while brushing your teeth can save up to 5 gallons of water each time.",
    "A running toilet can waste over 200 gallons of water a day.",
    "Low-flow showerheads save up to 15 gallons of water per 10-minute shower.",
    "Replacing a traditional toilet with a water-efficient one can save 13,000 gallons a year.",
    "Washing your car with a bucket instead of a hose saves about 100 gallons of water.",
    "Using a broom instead of a hose to clean driveways saves up to 150 gallons per use.",
    "It takes about 2,400 gallons of water to produce a single hamburger.",
    "Producing one cup of coffee requires about 37 gallons of water.",
    "Growing a pound of rice requires about 450 gallons of water.",
    "A pound of chocolate takes 1,700 gallons of water to produce.",
    "Producing a single egg requires about 53 gallons of water.",
    "Eating plant-based meals can significantly reduce your water footprint.",
    "Water boils at 212°F (100°C) at sea level but at lower temperatures at higher altitudes.",
    "Hot water freezes faster than cold water in some cases—this is called the Mpemba effect.",
    "A jellyfish is approximately 95% water.",
    "The Amazon River discharges about 58 million gallons of water per second into the ocean.",
    "The world's largest underground reservoir is the Ogallala Aquifer in the United States. ",
    "The average shower uses about 17 gallons of water.",
    "A dishwasher uses about 4-6 gallons of water per cycle, less than washing dishes by hand.",
    "Washing clothes in a high-efficiency machine uses about 15 gallons, compared to 40 gallons for older machines.",
    "A single lawn sprinkler uses over 1,000 gallons of water per hour.",
    "Swimming pools lose thousands of gallons of water yearly through evaporation." ,
    "The average raindrop falls at a speed of 7 miles per hour.",
    "A cloud can weigh more than a million pounds.",
    "Glaciers and ice caps store the majority of the Earth's freshwater.",
    "Over 2 billion people worldwide lack access to clean drinking water.",
    "Plastic pollution in the ocean can harm marine life and ecosystems.",
    "One quart of oil can contaminate up to 250,000 gallons of water.",
    "The ancient Romans built aqueducts to transport water, some of which are still in use today.",
    "In some cultures, rain is considered a symbol of renewal and blessing.",
    "Cape Town, South Africa, nearly ran out of water during its Day Zero crisis in 2018.",
    "Desalination plants provide water to countries like Saudi Arabia , despite their high energy costs.",
    "Melting glaciers contribute to rising sea levels and loss of freshwater reservoirs.",
    "Water expands by about 9% when it freezes",    
    "Water is the only substance that can exist as a solid, liquid, and gas at Earths natural temperatures.",
    "The world's first water treatment plant was built in Scotland in 1804.²"

]

# Hidden button/icon
st.markdown('<div style="text-align: center; cursor: pointer;">💧</div>', unsafe_allow_html=True)
if st.button("Discover a Water Fact"):
    fact = random.choice(water_facts)
    st.info(f"💧 {fact}")





import time  # Import time module to introduce delays

st.title("Water Trivia Challenge")

# Questions and Answers
questions = [
    {
        "question": "How much water does the average person use per day?",
        "options": ["10 gallons", "50 gallons", "100 gallons", "200 gallons"],
        "answer": "100 gallons",
        "badge": "Water Saver Pro"
    },
    {
        "question": "Which activity uses the most water?",
        "options": ["Showering", "Washing dishes", "Flushing the toilet", "Laundry"],
        "answer": "Laundry",
        "badge": "Eco-Warrior"
    },
    {
        "question": "How much water can a leaky faucet waste in a year?",
        "options": ["1,000 gallons", "3,000 gallons", "5,000 gallons", "10,000 gallons"],
        "answer": "3,000 gallons",
        "badge": "Leak Detective"
    },
    {
        "question": "How much of Earth's water is freshwater?",
        "options": ["1%", "2.5%", "10%", "25%"],
        "answer": "2.5%",
        "badge": "Freshwater Explorer"
    },
    {
        "question": "How long can a person survive without water?",
        "options": ["3 days", "7 days", "2 weeks", "1 month"],
        "answer": "3 days",
        "badge": "Survivalist"
    },
    {
        "question": "How much water can you save by turning off the tap while brushing your teeth?",
        "options": ["1 gallon", "5 gallons", "8 gallons", "10 gallons"],
        "answer": "5 gallons",
        "badge": "Tap Saver"
    },
    {
        "question": "How much water does it take to produce one hamburger?",
        "options": ["100 gallons", "500 gallons", "1,200 gallons", "2,400 gallons"],
        "answer": "2,400 gallons",
        "badge": "Water Wise Eater"
    },
    {
        "question": "Which food item requires the least water to produce?",
        "options": ["Chicken", "Rice", "Beans", "Lettuce"],
        "answer": "Lettuce",
        "badge": "Eco-Foodie"
    },
    {
        "question": "What percentage of global freshwater is used for agriculture?",
        "options": ["20%", "40%", "70%", "90%"],
        "answer": "70%",
        "badge": "Agri-Water Expert"
    },
    {
        "question": "How much water is used by toilets in the home?",
        "options": ["10%", "20%", "30%", "40%"],
        "answer": "30%",
        "badge": "Home Saver"
    }
]

# Session State for Progress
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.correct_answers = 0

# Display Question
current_question = st.session_state.current_question
if current_question < len(questions):
    question = questions[current_question]
    st.write(question["question"])
    selected = st.radio("Choose an answer:", question["options"])

    if st.button("Submit"):
        if selected == question["answer"]:
            st.success(f"Correct! Badge Earned: 🏅 {question['badge']}")
            st.session_state.correct_answers += 1
        else:
            st.error(f"Incorrect! The correct answer is: **{question['answer']}**")
            st.write(f"Better luck next time! The badge for this question is: 🏅 {question['badge']}")
        
        # Wait for 3 seconds to give time to see the result
        time.sleep(3)
        
        st.session_state.current_question += 1
        st.rerun()  # Refresh the page to show the next question
else:
    st.write(f"You completed the quiz! 🎉 Correct Answers: {st.session_state.correct_answers}/{len(questions)}")
    if st.button("Restart"):
        st.session_state.current_question = 0
        st.session_state.correct_answers = 0
        st.rerun()  # Refresh the page to restart the quiz
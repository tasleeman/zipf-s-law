import os
import streamlit as st
import string
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Streamlit UI
st.title("Word Frequency Distribution (Zipf's Law)")

st.sidebar.header("Upload Text Files")
uploaded_files = st.sidebar.file_uploader("Upload .txt files", accept_multiple_files=True, type=["txt"])

# Define parameters
depth = 10  # Number of top-ranked words to display
unwanted_characters = list(string.punctuation)

# Data storage
texts = {}
textlengths = {}
textwordamounts = {}

if uploaded_files:
    for file in uploaded_files:
        file_name = file.name.split('.')[0]
        texts[file_name] = file.read().decode("utf-8")

    # Processing text
    for text in texts:
        # Remove punctuation and convert to lowercase
        for character in unwanted_characters:
            texts[text] = texts[text].replace(character, '').lower()

        words = texts[text].split()
        textlengths[text] = len(words)

        # Word frequency count
        textwordamounts[text] = {}
        for word in words:
            textwordamounts[text][word] = textwordamounts[text].get(word, 0) + 1

        # Sort by frequency and keep top depth words
        textwordamounts[text] = dict(sorted(textwordamounts[text].items(), key=lambda x: x[1], reverse=True)[:depth])

    # Function to normalize values to percentage
    def percentify(value, max_value):
        return round(value / max_value * 100)

    # Function to smooth curves
    def smoothify(y_values):
        x = np.array(range(len(y_values)))
        y = np.array(y_values)
        x_smooth = np.linspace(x.min(), x.max(), 600)
        spl = make_interp_spline(x, y, k=3)
        y_smooth = spl(x_smooth)
        return x_smooth, y_smooth

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 5))

    # Generate the Zipfian Curve
    zipfian_curve = [100 / i for i in range(1, depth + 1)]
    x, y = smoothify(zipfian_curve)
    ax.plot(x, y, label="Zipfian Curve", linestyle=":", color="gray")

    # Plot text file data
    for text in textwordamounts:
        max_value = list(textwordamounts[text].values())[0]
        y_values = [percentify(value, max_value) for value in textwordamounts[text].values()]
        x, y = smoothify(y_values)
        ax.plot(x, y, label=f"{text} [{textlengths[text]} words]", linewidth=1, alpha=0.7)

    ax.set_xticks(range(depth))
    ax.set_xticklabels(range(1, depth + 1))
    ax.set_xlabel("Word Rank")
    ax.set_ylabel("Frequency (%)")
    ax.legend()
    st.pyplot(fig)
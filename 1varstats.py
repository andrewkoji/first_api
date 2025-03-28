import pandas as pd
import numpy as np
import requests 
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    st.markdown(
        """
        <style>
        /* Set the main background with a light mode and optional picture */
        .stApp {
            background: #ffffff; /* Light mode background color */
            background-image: url("/cimages/multimages/16/system2401008797131253426.png"); /* Optional background picture */
            background-size: cover;
            color: #000000; /* Black text for light mode */
        }

        /* Set the sidebar background with a light mode and optional picture */
        section[data-testid="stSidebar"] {
            background: #ffffff; /* Light gray background for sidebar */
            background-image: url("Graph3.gif"); /* Optional sidebar picture */
            background-size: cover;
            color: #000000; /* Black text for light mode */
        }

        /* Ensure text is readable on light backgrounds */
        .stMarkdown, .stTextInput, .stButton {
            color: #000000; /* Black text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title('MP3 Test Grades')

    period1 = pd.read_excel('period5grades.xlsx').sort_values(by='MP3 Test (1x)')
    st.markdown("<h3 style='text-align: center;'>MP3 Test Grades</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{', '.join(map(str, period1['MP3 Test (1x)'].tolist()))}</h3>", unsafe_allow_html=True)
    # st.write("", ", ".join(map(str, period1['MP3 Test (1x)'].tolist())))
    STATS = period1['MP3 Test (1x)'].describe().reset_index()
    STATS.columns = ['Stats', 'Value']
    STATS['Value'] = STATS['Value'].round(2)
    STATS['Stats'] = STATS['Stats'].replace({
        'count': 'Count',
        'mean': 'Mean(x̄)',
        'std': 'Standard Deviation(Sx)',
        'min': 'Minimum',
        '25%': 'Q1',
        '50%': 'Median',
        '75%': 'Q3',
        'max': 'Maximum'
    })
    st.dataframe(STATS,width=400, height=350)

    # Plot a bell curve
    st.write("Test Grade Bell Curve")
    mean = period1['MP3 Test (1x)'].mean()
    median = period1['MP3 Test (1x)'].median()
    std = period1['MP3 Test (1x)'].std()
    q1 = period1['MP3 Test (1x)'].quantile(0.25)
    q3 = period1['MP3 Test (1x)'].quantile(0.75)

    # Generate data for the bell curve
    x = np.linspace(period1['MP3 Test (1x)'].min(), period1['MP3 Test (1x)'].max(), 100)
    sns_kde = sns.kdeplot(period1['MP3 Test (1x)'], bw_adjust=1, fill=False).get_lines()[0].get_data()
    x, y = sns_kde

    # Add checkboxes for toggling vertical lines
    show_mean = st.checkbox("Show Mean", value=True)
    show_median = st.checkbox("Show Median", value=True)
    show_q1 = st.checkbox("Show Q1", value=True)
    show_q3 = st.checkbox("Show Q3", value=True)
    show_std_dev = st.checkbox("Show Standard Deviations", value=False)

    # Plot using matplotlib
    fig, ax = plt.subplots()
    sns.histplot(period1['MP3 Test (1x)'], kde=False, stat="density", bins=10, color="skyblue", label="Data Histogram")

    # Add vertical lines based on checkbox selections
    if show_mean:
        ax.axvline(mean, color="green", linestyle="--", label="Mean")
    if show_median:
        ax.axvline(median, color="purple", linestyle="--", label="Median")
    if show_q1:
        ax.axvline(q1, color="blue", linestyle="--", label="Q1")
    if show_q3:
        ax.axvline(q3, color="blue", linestyle="--", label="Q3")
    if show_std_dev:
        ax.axvline(mean + std, color="orange", linestyle="--", label="Mean + 1 Std Dev")
        ax.axvline(mean - std, color="orange", linestyle="--", label="Mean - 1 Std Dev")
        ax.axvline(mean + 2*std, color="purple", linestyle="--", label="Mean + 2 Std Dev")
        ax.axvline(mean - 2*std, color="purple", linestyle="--", label="Mean - 2 Std Dev")
        ax.axvline(mean + 3*std, color="brown", linestyle="--", label="Mean + 3 Std Dev")
        ax.axvline(mean - 3*std, color="brown", linestyle="--", label="Mean - 3 Std Dev")

    # Set plot title and labels
    ax.set_title("Histogram of Test Scores")
    ax.set_xlabel("Test Score")
    ax.set_ylabel("Density")
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)




    # Add a boxplot below the histogram
    st.markdown(f"<h3 style='text-align: center;'>BoxPlot</h3>", unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(8, 2))
    sns.boxplot(x=period1['MP3 Test (1x)'], ax=ax2, color="skyblue")
    ax2.set_title("Boxplot of Test Scores")
    ax2.set_xlabel("Test Score")
    # Add vertical lines based on checkbox selections

    # Add checkboxes for toggling vertical lines on the boxplot
    show_mean2 = st.checkbox("Show Mean (Boxplot)", value=True)
    show_median2 = st.checkbox("Show Median (Boxplot)", value=True)
    show_q1_2 = st.checkbox("Show Q1 (Boxplot)", value=True)
    show_q3_2 = st.checkbox("Show Q3 (Boxplot)", value=True)
    show_std_dev_2 = st.checkbox("Show Standard Deviations (Boxplot)", value=False)
    show_q1_2 = st.checkbox("Show Legend", value=True)

    # Add vertical lines to the boxplot based on checkbox selections
    if show_mean2:
        ax2.axvline(mean, color="green", linestyle="--", label="Mean")
    if show_median2:
        ax2.axvline(median, color="purple", linestyle="--", label="Median")
    if show_q1_2:
        ax2.axvline(q1, color="blue", linestyle="--", label="Q1")
    if show_q3_2:
        ax2.axvline(q3, color="blue", linestyle="--", label="Q3")
    if show_std_dev_2:
        ax2.axvline(mean + std, color="orange", linestyle="--", label="Mean + 1 Std Dev")
        ax2.axvline(mean - std, color="orange", linestyle="--", label="Mean - 1 Std Dev")
        ax2.axvline(mean + 2*std, color="purple", linestyle="--", label="Mean + 2 Std Dev")
        ax2.axvline(mean - 2*std, color="purple", linestyle="--", label="Mean - 2 Std Dev")
        ax2.axvline(mean + 3*std, color="brown", linestyle="--", label="Mean + 3 Std Dev")
        ax2.axvline(mean - 3*std, color="brown", linestyle="--", label="Mean - 3 Std Dev")
    # Display the boxplot in Streamlit
    # Set plot title and labels
    ax2.set_title("Histogram of Test Scores")
    ax2.set_xlabel("Test Score")
    ax2.set_ylabel("Density")
    ax2.legend()
    st.pyplot(fig2)

    IQR = q3 - q1
    st.markdown(f"<h3 style='text-align: center;color: red'>Interquartile Range (IQR): Q3 - Q1</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{q3} - {q1}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>IQR = {IQR}</h3>", unsafe_allow_html=True)


    range = round(period1['MP3 Test (1x)'].max() - period1['MP3 Test (1x)'].min(), 2)
    max = period1['MP3 Test (1x)'].max()
    min = period1['MP3 Test (1x)'].min()
    st.markdown(f"<h3 style='text-align: center;color: red'>Range: MAX - MIN</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{max} - {min}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Range = {range}</h3>", unsafe_allow_html=True)



if __name__ == '__main__':
    main()
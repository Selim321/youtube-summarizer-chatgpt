import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import unicodedata
import creds 

def summarize_video(url):
  
  if "watch" in url:
    pass
  else:
    url = url.replace("youtu.be/", "www.youtube.com/watch?v=")

  parsed_url = urlparse(url)
  video_id = parse_qs(parsed_url.query)['v'][0]

  # Get the transcript 
  transcript = YouTubeTranscriptApi.get_transcript(video_id)

  # Combining all the lists into on unique list
  text = []
  for i in range(0, len(transcript)):
      text.append(transcript[i]["text"])

  # Join list items into one paragraph
  video_transcript = " ".join(text)
  print("Text transcript created")

  print(video_transcript)

  # Text normalization 
  my_string = unicodedata.normalize('NFKD', video_transcript)
  print("Text normalized")

  #text summarization with openai turbo 3.5
  import openai

  my_api_key = creds.openai_key

  completion = openai.ChatCompletion.create(
     model="gpt-3.5-turbo",
     messages = {"role":"user", "content": "can you summarize me this text? : {my_string} "}
  )
  
  summary = completion.choices[0].message

  return summary


  


# Define the Streamlit app
st.title("YouTube Summarizer")

# Define the input form
form = st.form(key="input_form")

# Get the video ID from the URL
video_url = form.text_input("Enter a YouTube video URL")

# Submit button
submit_button = form.form_submit_button("Summarize Video")

# Handle form submissions
if submit_button:
    # Call the summarize_video function to get the summary
    summary = summarize_video(video_url)

    # Display the summary to the user
    st.subheader("Summary")
    st.write(summary)

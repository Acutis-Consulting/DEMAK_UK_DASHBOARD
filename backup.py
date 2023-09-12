import streamlit as st
import json
import base64

def get_download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.
    """
    # some strings <-> bytes conversions necessary here
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def save_inputs(arbeitnehmer_anzahl):
    inputs = {
        'arbeitnehmer_anzahl': arbeitnehmer_anzahl,
        #... Add all the inputs you want to save
    }
    return json.dumps(inputs)

def load_inputs(uploaded_file):
    uploaded_data = json.loads(uploaded_file.getvalue())
    return uploaded_data

# main part of your streamlit code
uploaded_file = st.file_uploader("Choose a file to upload", type="json")
data = None
if uploaded_file:
    data = load_inputs(uploaded_file)

default_arbeitnehmer_anzahl = data['arbeitnehmer_anzahl'] if data else 0
arbeitnehmer_anzahl = st.sidebar.number_input('Arbeitnehmeranzahl (AN)', value=default_arbeitnehmer_anzahl)

# add a button to download user's current inputs
if st.button('Download Input Values'):
    inputs_str = save_inputs(arbeitnehmer_anzahl)
    st.markdown(get_download_link(inputs_str, 'user_inputs.json', 'Download Your Inputs'), unsafe_allow_html=True)

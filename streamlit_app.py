import streamlit as st
import pandas as pd
from PIL import Image
import json
import hmac
import base64
import uuid

# Password Protection
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Passwort", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("Passwort falsch")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Custom metric HTML templates
custom_metric_html = """
    <div style="display: flex;
                background-color: #F0F8FF;
                border: 1px solid #CCCCCC;
                padding: 0;
                border-radius: 15px;
                margin-bottom: 10px;
                width: 100%;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                overflow-wrap: break-word;">
        <div style="width: 10px;
                    background-color: #fdff00; 
                    border-top-left-radius: 15px;
                    border-bottom-left-radius: 15px;">
        </div>
        <div style="padding: 20px 20px 20px 10px; flex-grow: 1;">
            <div style="font-weight: bold; color: #41528b; font-size: 16px;">
                {label}
            </div>
            <div style="font-size: 36px; font-weight: bold; color: #41528b;">
                {value}
            </div>
        </div>
    </div>
"""

custom_metric_html_with_change = """
    <div style="display: flex;
                background-color: #F0F8FF;
                border: 1px solid #CCCCCC;
                padding: 0;
                border-radius: 15px;
                margin-bottom: 10px;
                width: 100%;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                overflow-wrap: break-word;">
        <div style="width: 10px;
                    background-color: #fdff00;
                    border-top-left-radius: 15px;
                    border-bottom-left-radius: 15px;">
        </div>
        <div style="padding: 20px 20px 20px 10px; flex-grow: 1;">
            <div style="font-weight: bold; color: #41528b; font-size: 16px;">
                {label}
            </div>
            <div style="font-size: 36px; font-weight: bold; color: #41528b;">
                {value}
            </div>
            <div style="font-size: 25px; color: {change_color};">
                {change}
            </div>
        </div>
    </div>
"""

# Utility Functions
def to_percentage(value):
    # Function to format numbers as percentages in German locale
    v1 = f'{value*100:,.2f} %'
    v2 = v1.replace(',','#')
    v3 = v2.replace('.','&')
    v4 = v3.replace('#','.')
    v5 = v4.replace('&',',')
    return v5

def format_german(value):
    # Function to format numbers as currency in German locale
    v1 = f'{value:,.2f} €'
    v2 = v1.replace(',','#')
    v3 = v2.replace('.','%')
    v4 = v3.replace('#','.')
    v5 = v4.replace('%',',')
    return v5

def safe_division(numerator, denominator):
    # Function to avoid division by zero
    if denominator == 0:
        return 0
    else:
        return numerator / denominator

def get_change_color(change_value):
    # Function to determine color based on value
    return "green" if change_value > 0 else "red"

# Sidebar: Simulation Parameters
st.sidebar.header('DEMAK Dashboard `Version 2`')
st.sidebar.title('Simulationsparameter')

# Initialize groups in session state if not present
if 'groups' not in st.session_state:
    st.session_state['groups'] = []

# File Uploader to Load Parameters
uploaded_file = st.sidebar.file_uploader("Parameter Hochladen", type=["json"])

if uploaded_file and 'uploaded_data_loaded' not in st.session_state:
    # Reading the uploaded JSON file
    uploaded_data = json.load(uploaded_file)
    # Load groups data from the uploaded file
    if 'groups' in uploaded_data:
        st.session_state['groups'] = uploaded_data['groups']
    else:
        st.warning("Die hochgeladene Datei enthält keine Gruppendaten.")

    # Load other parameters
    st.session_state['darlehenszins'] = uploaded_data.get('darlehenszins', 0.075)
    st.session_state['psv_beitragssatz'] = uploaded_data.get('psv_beitragssatz', 0.0025)
    st.session_state['uk_verwaltung_jaehrlich_pro_an'] = uploaded_data.get('uk_verwaltung_jaehrlich_pro_an', 89)
    st.session_state['uk_verwaltung_einmalig_im_ersten_jahr'] = uploaded_data.get('uk_verwaltung_einmalig_im_ersten_jahr', 0.02)
    st.session_state['p1_anlage_liq'] = uploaded_data.get('p1_anlage_liq', 0.0)
    st.session_state['beitragsbemessungsgrenze'] = uploaded_data.get('beitragsbemessungsgrenze', 7300)
    # Load balance sheet parameters
    st.session_state['Anlagevermögen'] = uploaded_data.get('Anlagevermögen', 0)
    st.session_state['Vorräte'] = uploaded_data.get('Vorräte', 0)
    st.session_state['Kurzfristige Forderungen'] = uploaded_data.get('Kurzfristige Forderungen', 0)
    st.session_state['Zahlungsmittel'] = uploaded_data.get('Zahlungsmittel', 0)
    st.session_state['kurzfristig (FK kurzfr.)'] = uploaded_data.get('kurzfristig (FK kurzfr.)', 0)
    st.session_state['langfristig (FK langfr.)'] = uploaded_data.get('langfristig (FK langfr.)', 0)

    # Set a flag to indicate that we've loaded the uploaded data
    st.session_state['uploaded_data_loaded'] = True

else:
    # Default values if no file is uploaded or data has already been loaded
    if 'darlehenszins' not in st.session_state:
        st.session_state['darlehenszins'] = 0.075
    if 'psv_beitragssatz' not in st.session_state:
        st.session_state['psv_beitragssatz'] = 0.0025
    if 'uk_verwaltung_jaehrlich_pro_an' not in st.session_state:
        st.session_state['uk_verwaltung_jaehrlich_pro_an'] = 89
    if 'uk_verwaltung_einmalig_im_ersten_jahr' not in st.session_state:
        st.session_state['uk_verwaltung_einmalig_im_ersten_jahr'] = 0.02
    if 'p1_anlage_liq' not in st.session_state:
        st.session_state['p1_anlage_liq'] = 0.0
    if 'beitragsbemessungsgrenze' not in st.session_state:
        st.session_state['beitragsbemessungsgrenze'] = 7300
    # Default balance sheet parameters
    if 'Anlagevermögen' not in st.session_state:
        st.session_state['Anlagevermögen'] = 0
    if 'Vorräte' not in st.session_state:
        st.session_state['Vorräte'] = 0
    if 'Kurzfristige Forderungen' not in st.session_state:
        st.session_state['Kurzfristige Forderungen'] = 0
    if 'Zahlungsmittel' not in st.session_state:
        st.session_state['Zahlungsmittel'] = 0
    if 'kurzfristig (FK kurzfr.)' not in st.session_state:
        st.session_state['kurzfristig (FK kurzfr.)'] = 0
    if 'langfristig (FK langfr.)' not in st.session_state:
        st.session_state['langfristig (FK langfr.)'] = 0

# Button to Add a New Group
if st.sidebar.button('Gruppe hinzufügen'):
    new_group = {
        'id': str(uuid.uuid4()),
        'arbeitnehmer_anzahl': 0,
        'zins_zusage': 0.0,
        'an_fin_jaehrlich_pro_an': 0.0,
        'ag_fin_jaehrlich_pro_an': 0.0,
        'laufzeit': 0
    }
    st.session_state['groups'].append(new_group)

# Loop over Groups and Create Input Fields
for idx, group in enumerate(st.session_state['groups']):
    st.sidebar.title(f'Gruppe {idx+1}')
    group_id = group['id']
    arbeitnehmer_anzahl = st.sidebar.number_input(
        'Arbeitnehmeranzahl (AN)',
        min_value=0,
        value=group.get('arbeitnehmer_anzahl', 0),
        key=f'arbeitnehmer_anzahl_{group_id}'
    )
    zins_zusage = st.sidebar.number_input(
        'Zins Zusage (%)',
        min_value=0.0,
        value=group.get('zins_zusage', 0.0)*100,
        key=f'zins_zusage_{group_id}'
    ) / 100
    an_fin_jaehrlich_pro_an = st.sidebar.number_input(
        'AN finanziert jährlich pro AN (€)',
        min_value=0.0,
        value=group.get('an_fin_jaehrlich_pro_an', 0.0),
        key=f'an_fin_jaehrlich_pro_an_{group_id}'
    )
    ag_fin_jaehrlich_pro_an = st.sidebar.number_input(
        'AG finanziert jährlich pro AN (€)',
        min_value=0.0,
        value=group.get('ag_fin_jaehrlich_pro_an', 0.0),
        key=f'ag_fin_jaehrlich_pro_an_{group_id}'
    )
    laufzeit = st.sidebar.number_input(
        'Laufzeit Zusage (Jahre)',
        min_value=0,
        value=group.get('laufzeit', 0),
        key=f'laufzeit_{group_id}'
    )
    # Update the group in session state
    group.update({
        'arbeitnehmer_anzahl': arbeitnehmer_anzahl,
        'zins_zusage': zins_zusage,
        'an_fin_jaehrlich_pro_an': an_fin_jaehrlich_pro_an,
        'ag_fin_jaehrlich_pro_an': ag_fin_jaehrlich_pro_an,
        'laufzeit': laufzeit
    })
    # Delete group button
    if st.sidebar.button(f'Gruppe {idx+1} löschen', key=f'delete_group_{group_id}'):
        st.session_state['groups'] = [g for g in st.session_state['groups'] if g['id'] != group_id]
        st.experimental_rerun()

# Allgemeine Parameter (General Parameters)
st.sidebar.title('Allgemeine Parameter')
st.session_state['darlehenszins'] = st.sidebar.number_input('Darlehenszins (%)', min_value=0.0, value=st.session_state['darlehenszins']*100)/100
st.session_state['psv_beitragssatz'] = st.sidebar.number_input('PSV-Beitragssatz (%)', min_value=0.0, value=st.session_state['psv_beitragssatz']*100)/100
st.session_state['uk_verwaltung_jaehrlich_pro_an'] = st.sidebar.number_input('UK Verwaltung jährlich pro AN', min_value=0, value=st.session_state['uk_verwaltung_jaehrlich_pro_an'])
st.session_state['uk_verwaltung_einmalig_im_ersten_jahr'] = st.sidebar.number_input('UK Verwaltung einmalig im ersten Jahr (%)', min_value=0.0, value=st.session_state['uk_verwaltung_einmalig_im_ersten_jahr']*100)/100
st.session_state['p1_anlage_liq'] = st.sidebar.number_input('Anlage Liquidität (%)', min_value=0.0, value=st.session_state['p1_anlage_liq']*100)/100
st.session_state['beitragsbemessungsgrenze'] = st.sidebar.number_input('Beitragsbemessungsgrenze pro Monat (€)', min_value=0, value=st.session_state['beitragsbemessungsgrenze'])

steuern_UK = 0.1583  # Fixed value
steuer_ersparnis = 0.3  # Fixed value

# Eröffnungsbilanz (Opening Balance Sheet)
st.sidebar.title('Eröffnungsbilanz')
col3, col4 = st.sidebar.columns(2)
col3.subheader('Aktiva')
col4.subheader('Passiva')

col1, col2 = st.sidebar.columns(2)
with col1:
    st.session_state['Anlagevermögen'] = st.number_input('Anlagevermögen', min_value=0, value=st.session_state['Anlagevermögen'])
    st.number_input('Umlaufvermögen', min_value=0, value=0, disabled=True)
    st.session_state['Vorräte'] = st.number_input('Vorräte', min_value=0, value=st.session_state['Vorräte'])
    st.session_state['Kurzfristige Forderungen'] = st.number_input('Kurzfristige Forderungen', min_value=0, value=st.session_state['Kurzfristige Forderungen'])
    st.session_state['Zahlungsmittel'] = st.number_input('Zahlungsmittel', min_value=0, value=st.session_state['Zahlungsmittel'])
with col2:
    st.number_input('Eigenkapital', min_value=0, value=0, disabled=True)
    st.number_input('Fremdkapital', min_value=0, value=0, disabled=True)
    st.session_state['kurzfristig (FK kurzfr.)'] = st.number_input('kurzfristig (FK kurzfr.)', min_value=0, value=st.session_state['kurzfristig (FK kurzfr.)'])
    st.session_state['langfristig (FK langfr.)'] = st.number_input('langfristig (FK langfr.)', min_value=0, value=st.session_state['langfristig (FK langfr.)'])

# Musterbilanz Einstellungen (Sample Balance Sheet Settings)
if st.session_state['groups']:
    laufzeit_max = max(group['laufzeit'] for group in st.session_state['groups'])
else:
    laufzeit_max = 0

options = list(range(1, laufzeit_max + 2))
st.sidebar.title('Musterbilanz')
c1, c2 = st.sidebar.columns(2)
with c1:
    bilanz_nach_jahren = st.selectbox('Bilanz nach X Jahren:', options, index=0)
    show_previous_balance_sheet = st.selectbox('Bilanzkennzahlen einblenden:', ('nein', 'ja'))
with c2:
    bilanzverlaengerung_j_n = st.selectbox('Bilanzverlängerung:', ('ja', 'nein'))
    bilanzanhang_einblenden = st.selectbox('Bilanzanhang einblenden:', ('nein', 'ja'))

# Finanzwirtschaftliche Bilanzkennzahlen (Financial Balance Sheet Ratios)
st.sidebar.title('Finanzwirtschaftliche Bilanzkennzahlen')
d1, d2 = st.sidebar.columns(2)
with d1:
    show_eigenkapital_quote = st.checkbox("Eigenkapitalquote", value=True)
    show_anspannungsgrad = st.checkbox("Anspannungsgrad", value=True)
    show_statischer_verschuldungsgrad = st.checkbox("Statischer Verschuldungsgrad", value=True)
    show_intensitaet_langfristiges_kapital = st.checkbox("Intensität langfristigen Kapitals", value=True)
    show_liquiditaet_1_grades = st.checkbox("Liquidität 1. Grades", value=True)
with d2:
    show_liquiditaet_2_grades = st.checkbox("Liquidität 2. Grades", value=True)
    show_liquiditaet_3_grades = st.checkbox("Liquidität 3. Grades", value=True)
    show_net_working_capital = st.checkbox("Net Working Capital", value=True)
    show_deckungsgrad_a = st.checkbox("Deckungsgrad A", value=True)
    show_deckungsgrad_b = st.checkbox("Deckungsgrad B", value=True)

# Parameter Saving Functionality
st.sidebar.title(' ')
if st.sidebar.button('Parameter Speichern'):
    # Creating a dictionary of parameters to save
    data_to_save = {
        'groups': st.session_state['groups'],
        'darlehenszins': st.session_state['darlehenszins'],
        'psv_beitragssatz': st.session_state['psv_beitragssatz'],
        'uk_verwaltung_jaehrlich_pro_an': st.session_state['uk_verwaltung_jaehrlich_pro_an'],
        'uk_verwaltung_einmalig_im_ersten_jahr': st.session_state['uk_verwaltung_einmalig_im_ersten_jahr'],
        'p1_anlage_liq': st.session_state['p1_anlage_liq'],
        'Anlagevermögen': st.session_state['Anlagevermögen'],
        'Vorräte': st.session_state['Vorräte'],
        'Kurzfristige Forderungen': st.session_state['Kurzfristige Forderungen'],
        'Zahlungsmittel': st.session_state['Zahlungsmittel'],
        'kurzfristig (FK kurzfr.)': st.session_state['kurzfristig (FK kurzfr.)'],
        'langfristig (FK langfr.)': st.session_state['langfristig (FK langfr.)'],
        'beitragsbemessungsgrenze': st.session_state['beitragsbemessungsgrenze']
    }

    # Convert dictionary to JSON string
    json_str = json.dumps(data_to_save, indent=4)

    # Convert the string to bytes
    b64 = base64.b64encode(json_str.encode()).decode()

    # Provide a link to download the JSON file
    href = f'<a href="data:file/json;base64,{b64}" download="parameters.json">Parameter Herunterladen</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# Assign variables from session state
darlehenszins = st.session_state['darlehenszins']
psv_beitragssatz = st.session_state['psv_beitragssatz']
uk_verwaltung_jaehrlich_pro_an = st.session_state['uk_verwaltung_jaehrlich_pro_an']
uk_verwaltung_einmalig_im_ersten_jahr = st.session_state['uk_verwaltung_einmalig_im_ersten_jahr']
p1_anlage_liq = st.session_state['p1_anlage_liq']
beitragsbemessungsgrenze = st.session_state['beitragsbemessungsgrenze']
anlagevermoegen = st.session_state['Anlagevermögen']
vorraete = st.session_state['Vorräte']
kurzfristige_forderungen = st.session_state['Kurzfristige Forderungen']
zahlungsmittel = st.session_state['Zahlungsmittel']
fk_kurzfristig = st.session_state['kurzfristig (FK kurzfr.)']
fk_langfristig = st.session_state['langfristig (FK langfr.)']

# Balance Sheet Calculations
umlaufvermögen = vorraete + kurzfristige_forderungen + zahlungsmittel
gesamtkapital_aktiva = anlagevermoegen + umlaufvermögen
fremdkapital = fk_kurzfristig + fk_langfristig
eigenkapital = gesamtkapital_aktiva - fremdkapital
gesamtkapital_passiva = eigenkapital + fremdkapital

# Initialize Variables for Group Calculations
arbeitnehmer_anzahl_gesamt = sum(group['arbeitnehmer_anzahl'] for group in st.session_state['groups'])
an_finanziert_jaehrlich_list = []
an_finanziert_jaehrlich_max_sv_frei_list = []
ag_finanziert_jaehrlich_list = []
an_ag_finanziert_jaehrlich_list = []
kapital_bei_ablauf_list = []
davon_an_list = []
laufzeit_list = []
zins_zusage_list = []

for idx, group in enumerate(st.session_state['groups']):
    arbeitnehmer_anzahl = group['arbeitnehmer_anzahl']
    zins_zusage = group['zins_zusage']
    an_fin_jaehrlich_pro_an = group['an_fin_jaehrlich_pro_an']
    ag_fin_jaehrlich_pro_an = group['ag_fin_jaehrlich_pro_an']
    laufzeit = group['laufzeit']

    an_finanziert_jaehrlich = arbeitnehmer_anzahl * an_fin_jaehrlich_pro_an
    an_finanziert_jaehrlich_list.append(an_finanziert_jaehrlich)
    an_finanziert_jaehrlich_max_sv_frei = arbeitnehmer_anzahl * (beitragsbemessungsgrenze * 12 * 0.04)
    an_finanziert_jaehrlich_max_sv_frei_list.append(an_finanziert_jaehrlich_max_sv_frei)
    ag_finanziert_jaehrlich = arbeitnehmer_anzahl * ag_fin_jaehrlich_pro_an
    ag_finanziert_jaehrlich_list.append(ag_finanziert_jaehrlich)
    an_ag_finanziert_jaehrlich = an_finanziert_jaehrlich + ag_finanziert_jaehrlich
    an_ag_finanziert_jaehrlich_list.append(an_ag_finanziert_jaehrlich)
    laufzeit_list.append(laufzeit)
    zins_zusage_list.append(zins_zusage)

    if zins_zusage != 0:
        kapital_bei_ablauf = safe_division((pow((1 + zins_zusage), laufzeit) - 1), zins_zusage) * (1 + zins_zusage) * an_ag_finanziert_jaehrlich
    else:
        kapital_bei_ablauf = an_ag_finanziert_jaehrlich * laufzeit
    kapital_bei_ablauf_list.append(kapital_bei_ablauf)

    if an_ag_finanziert_jaehrlich != 0:
        davon_an = safe_division(kapital_bei_ablauf, an_ag_finanziert_jaehrlich) * an_finanziert_jaehrlich
    else:
        davon_an = 0
    davon_an_list.append(davon_an)

# Sum Total Values from the Lists
an_finanziert_jaehrlich_gesamt = sum(an_finanziert_jaehrlich_list)
an_finanziert_jaehrlich_gesamt_max_sv_frei = sum(an_finanziert_jaehrlich_max_sv_frei_list)
ag_finanziert_jaehrlich_gesamt = sum(ag_finanziert_jaehrlich_list)
an_ag_finanziert_jaehrlich_gesamt = sum(an_ag_finanziert_jaehrlich_list)
kapital_bei_ablauf_gesamt = sum(kapital_bei_ablauf_list)
davon_an_gesamt = sum(davon_an_list)
laufzeit_max = max(laufzeit_list) if laufzeit_list else 0

# Initialize DataFrame for Calculations
df = pd.DataFrame()
df['Jahr'] = range(1, laufzeit_max + 2)
# Initialize all necessary columns in df
df['Zulässiges Kassenvemögen'] = 0
df['Höchstzulässiges Kassenvermögen'] = 0
#df['DEBUG'] = 0
df['Zulässige Dotierung'] = 0
df['Überdotierung'] = 0
df['Darlehenszinsen'] = 0

df['Zinsanteil Überdotierung'] = 0
df['Steuern UK (e.V.)'] = 0
df['Versorgung fällig'] = 0
df['Darlehensänderung'] = 0
df['Tatsächliches Kassenvermögen'] = 100
df['Kosten UK-Verwaltung'] = 0
df['PSV Beitrag'] = 0
df['EU + SV Ersparnis'] = 0
df['Steuerersparnis'] = 0
df['Liquiditätsänderung'] = 0
df['Anlage Liquidität'] = 0


# Initialize 'Barwert Versorgung' columns for each group
for idx in range(len(st.session_state['groups'])):
    df[f'Barwert Versorgung Gruppe {idx+1}'] = 0
df['Barwert Versorgung gesamt'] = 0

# Main Calculation Loop
# Main loop
for i in range(laufzeit_max+1):
    if i == 0:
        df.loc[i, 'Zulässiges Kassenvemögen'] = (kapital_bei_ablauf_gesamt / 10) * 0.25 * 8 #B
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = df.loc[i, 'Zulässiges Kassenvemögen']*1.25 #C
        df.loc[i, 'Zulässige Dotierung'] = (kapital_bei_ablauf_gesamt/10*0.25)
        df.loc[i, 'Tatsächliches Kassenvermögen'] =df.loc[i, 'Zulässige Dotierung'] #K
        df['Überdotierung'] = df.loc[i, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Höchstzulässiges Kassenvermögen']
        df['Darlehenszinsen'] = 0
        #df.loc[i, 'PSV Beitrag'] = (davon_an/10)*0.25*20*psv_beitragssatz #M ###vorGruppen
        df.loc[i, 'PSV Beitrag'] = (davon_an_gesamt/10)*0.25*20*psv_beitragssatz
        df.loc[i, 'Kosten UK-Verwaltung'] = (kapital_bei_ablauf_gesamt * uk_verwaltung_einmalig_im_ersten_jahr)+(arbeitnehmer_anzahl_gesamt * uk_verwaltung_jaehrlich_pro_an)
        df.loc[i, 'EU + SV Ersparnis'] = min(an_finanziert_jaehrlich_gesamt*1.2,an_finanziert_jaehrlich_gesamt_max_sv_frei*1.2) + max(0,(an_finanziert_jaehrlich_gesamt-an_finanziert_jaehrlich_gesamt_max_sv_frei)) #
        df.loc[i, 'Steuerersparnis'] = (df.loc[i, 'EU + SV Ersparnis']-df.loc[i,'PSV Beitrag']-df.loc[i,'Kosten UK-Verwaltung']-df.loc[i,'Zulässige Dotierung'])*steuer_ersparnis*-1
        df.loc[i, 'Liquiditätsänderung'] = df.loc[i, 'EU + SV Ersparnis']+ df.loc[i,'Steuerersparnis']-df.loc[i, 'PSV Beitrag']-df.loc[i, 'Kosten UK-Verwaltung']
        df.loc[i, 'Anlage Liquidität'] = df.loc[i, 'Liquiditätsänderung']
        #df.loc[i, 'Barwert Versorgung gesamt'] = df.loc[i, 'Barwert Versorgung Gruppe 1'] + df.loc[i, 'Barwert Versorgung Gruppe 2'] + df.loc[i, 'Barwert Versorgung Gruppe 3']
        pass
    elif i == (laufzeit_max):

        df.loc[i, 'Versorgung fällig'] = sum(
            kapital_bei_ablauf_list[idx]
            for idx, group in enumerate(st.session_state['groups'])
            if i == group['laufzeit']
        )
        df.loc[i, 'Zulässiges Kassenvemögen'] = 0
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = 0

        # Calculate 'Kosten UK-Verwaltung'
        remaining_arbeitnehmer_anzahl = sum(
            group['arbeitnehmer_anzahl']
            for idx, group in enumerate(st.session_state['groups'])
            if i <= group['laufzeit']
        )
        df.loc[i, 'Kosten UK-Verwaltung'] = remaining_arbeitnehmer_anzahl * uk_verwaltung_jaehrlich_pro_an

        df.loc[i, 'Darlehenszinsen'] = df.loc[i - 1, 'Tatsächliches Kassenvermögen'] * darlehenszins
        df.loc[i,'Tatsächliches Kassenvermögen'] = 0 ##ÄNDERUNG
        df.loc[i, 'Überdotierung'] = df.loc[i, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Höchstzulässiges Kassenvermögen'] #E
        #df.loc[df['Überdotierung'] >= 0, 'Steuern UK (e.V.)'] = (df['Zinsanteil Überdotierung']*steuern_UK)
        if df.loc[i-1, 'Überdotierung'] > 0:
            df.loc[i, 'Zinsanteil Überdotierung'] = (df.loc[i-1, 'Überdotierung'] / df.loc[i-1, 'Tatsächliches Kassenvermögen']) * df.loc[i-1, 'Darlehenszinsen'] #G
        else:
            df.loc[i, 'Zinsanteil Überdotierung'] = 0 ##ÄNDERUNG

        if df.loc[i, 'Überdotierung'] >= 0:
            df.loc[i, 'Steuern UK (e.V.)'] = df.loc[i, 'Zinsanteil Überdotierung']*steuern_UK
        else:
            df.loc[i, 'Steuern UK (e.V.)'] = 100 #ÄNDERN!!

        if i < 3:
            # Before year 4, use 'davon_an'
            if i == 0:
                psv_basis = davon_an_gesamt
            else:
                psv_basis = sum(
                    davon_an_list[idx]
                    for idx, group in enumerate(st.session_state['groups'])
                    if i <= group['laufzeit'] + 1  # Adjusted condition
                )
        else:
            # From year 4 onwards, use 'kapital_bei_ablauf'
            psv_basis = sum(
                kapital_bei_ablauf_list[idx]
                for idx, group in enumerate(st.session_state['groups'])
                if i <= group['laufzeit']  # Adjusted condition
            )
        df.loc[i, 'PSV Beitrag'] = (psv_basis/10)*0.25*20*psv_beitragssatz


        #df.loc[i, 'Steuerersparnis'] = (df['EU + SV Ersparnis'] - df['PSV Beitrag'] - df['Kosten UK-Verwaltung'] - df['Darlehenszinsen']-df['Zulässige Dotierung'])*steuer_ersparnis*-1 #O
        df.loc[i,'Zulässige Dotierung'] = df.loc[i, 'Zulässiges Kassenvemögen'] + df.loc[i, 'Versorgung fällig'] - df.loc[i, 'Darlehenszinsen'] - df.loc[i - 1, 'Tatsächliches Kassenvermögen'] + df.loc[i, 'Steuern UK (e.V.)']
        df.loc[i,'Darlehensänderung'] = df.loc[i, 'Zulässige Dotierung'] + df.loc[i, 'Darlehenszinsen'] - df.loc[i, 'Steuern UK (e.V.)'] - df.loc[i, 'Versorgung fällig']  #J ###ÄNDERUNG
        df.loc[i, 'Steuerersparnis'] = (df.loc[i, 'EU + SV Ersparnis'] - df.loc[i, 'PSV Beitrag'] - df.loc[i, 'Kosten UK-Verwaltung'] - df.loc[i, 'Darlehenszinsen'] - df.loc[i, 'Zulässige Dotierung']) * steuer_ersparnis * -1
        df.loc[i,'Liquiditätsänderung'] = df.loc[i,'EU + SV Ersparnis'] + df.loc[i,'Steuerersparnis'] - df.loc[i,'PSV Beitrag'] - df.loc[i,'Kosten UK-Verwaltung'] - df.loc[i,'Steuern UK (e.V.)'] - df.loc[i,'Versorgung fällig']
        df.loc[i, 'Anlage Liquidität'] = df.loc[i-1, 'Anlage Liquidität']*(1+p1_anlage_liq) +df.loc[i, 'Liquiditätsänderung'] #Q
        pass
    else:
        df.loc[i, 'Versorgung fällig'] = sum(
            kapital_bei_ablauf_list[idx]
            for idx, group in enumerate(st.session_state['groups'])
            if i == group['laufzeit']
        )

        # Remaining 'Kapital bei Ablauf' for active groups
        remaining_kapital_bei_ablauf = sum(
            kapital_bei_ablauf_list[idx]
            for idx, group in enumerate(st.session_state['groups'])
            if i < group['laufzeit']
        )
        df.loc[i, 'Zulässiges Kassenvemögen'] = (remaining_kapital_bei_ablauf / 10) * 0.25 * 8
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = df.loc[i, 'Zulässiges Kassenvemögen'] * 1.25

        if i < 3:
            # Before year 4, use 'davon_an'
            if i == 0:
                psv_basis = davon_an_gesamt
            else:
                psv_basis = sum(
                    davon_an_list[idx]
                    for idx, group in enumerate(st.session_state['groups'])
                    if i <= group['laufzeit'] + 1  # Adjusted condition
                )
        else:
            # From year 4 onwards, use 'kapital_bei_ablauf'
            psv_basis = sum(
                kapital_bei_ablauf_list[idx]
                for idx, group in enumerate(st.session_state['groups'])
                if i <= group['laufzeit']  # Adjusted condition
            )
        df.loc[i, 'PSV Beitrag'] = (psv_basis/10)*0.25*20*psv_beitragssatz

        total_an_finanziert_jaehrlich = sum(
            an_finanziert_jaehrlich_list[idx]
            for idx, group in enumerate(st.session_state['groups'])
            if i <= group['laufzeit'] - 1
        )
        total_an_finanziert_jaehrlich_max_sv_frei = sum(
            an_finanziert_jaehrlich_max_sv_frei_list[idx]
            for idx, group in enumerate(st.session_state['groups'])
            if i <= group['laufzeit'] - 1
        )
        df.loc[i, 'EU + SV Ersparnis'] = min(total_an_finanziert_jaehrlich * 1.2, total_an_finanziert_jaehrlich_max_sv_frei * 1.2) + max(0, total_an_finanziert_jaehrlich - total_an_finanziert_jaehrlich_max_sv_frei)

        # Calculate 'Kosten UK-Verwaltung'
        remaining_arbeitnehmer_anzahl = sum(
            group['arbeitnehmer_anzahl']
            for idx, group in enumerate(st.session_state['groups'])
            if i <= group['laufzeit']
        )
        df.loc[i, 'Kosten UK-Verwaltung'] = remaining_arbeitnehmer_anzahl * uk_verwaltung_jaehrlich_pro_an

        df.loc[i, 'Darlehenszinsen'] = df.loc[i - 1, 'Tatsächliches Kassenvermögen'] * darlehenszins

        if df.loc[i - 1, 'Überdotierung'] > 0:
            df.loc[i, 'Zinsanteil Überdotierung'] = (df.loc[i - 1, 'Überdotierung'] / df.loc[i - 1, 'Tatsächliches Kassenvermögen']) * df.loc[i, 'Darlehenszinsen']
            df.loc[i, 'Steuern UK (e.V.)'] = df.loc[i, 'Zinsanteil Überdotierung'] * steuern_UK
        else:
            df.loc[i, 'Zinsanteil Überdotierung'] = 0
            df.loc[i, 'Steuern UK (e.V.)'] = 0

        # Calculate 'Zulässige Dotierung'
        zulässige_dotierung_candidate = df.loc[i, 'Zulässiges Kassenvemögen'] + df.loc[i, 'Versorgung fällig'] - df.loc[i, 'Darlehenszinsen'] - df.loc[i - 1, 'Tatsächliches Kassenvermögen'] + df.loc[i, 'Steuern UK (e.V.)']

        if (df.loc[i - 1, 'Tatsächliches Kassenvermögen'] + df.loc[i, 'Darlehenszinsen'] + (remaining_kapital_bei_ablauf / 10) * 0.25) <= df.loc[i, 'Zulässiges Kassenvemögen']:
            df.loc[i, 'Zulässige Dotierung'] = (remaining_kapital_bei_ablauf / 10) * 0.25
        else:
            if (df.loc[i, 'Zulässiges Kassenvemögen'] + df.loc[i, 'Versorgung fällig'] - df.loc[i - 1, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Darlehenszinsen']) > 0:
                df.loc[i, 'Zulässige Dotierung'] = zulässige_dotierung_candidate ##Die hier Trifft
            else:
                df.loc[i, 'Zulässige Dotierung'] = 0


                # Calculate 'Darlehensänderung' and 'Tatsächliches Kassenvermögen'
        df.loc[i, 'Darlehensänderung'] = df.loc[i, 'Zulässige Dotierung'] + df.loc[i, 'Darlehenszinsen'] - df.loc[i, 'Steuern UK (e.V.)'] - df.loc[i, 'Versorgung fällig']
        df.loc[i, 'Tatsächliches Kassenvermögen'] = df.loc[i - 1, 'Tatsächliches Kassenvermögen'] + df.loc[i, 'Darlehensänderung']

        df.loc[i, 'Überdotierung'] = df.loc[i, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Höchstzulässiges Kassenvermögen']

        # Calculate 'Steuerersparnis'
        df.loc[i, 'Steuerersparnis'] = (df.loc[i, 'EU + SV Ersparnis'] - df.loc[i, 'PSV Beitrag'] - df.loc[i, 'Kosten UK-Verwaltung'] - df.loc[i, 'Darlehenszinsen'] - df.loc[i, 'Zulässige Dotierung']) * steuer_ersparnis * -1

        # Calculate 'Liquiditätsänderung'
        df.loc[i, 'Liquiditätsänderung'] = df.loc[i, 'EU + SV Ersparnis'] + df.loc[i, 'Steuerersparnis'] - df.loc[i, 'PSV Beitrag'] - df.loc[i, 'Kosten UK-Verwaltung'] - df.loc[i, 'Steuern UK (e.V.)'] - df.loc[i, 'Versorgung fällig']

        # Calculate 'Anlage Liquidität'
        df.loc[i, 'Anlage Liquidität'] = df.loc[i - 1, 'Anlage Liquidität'] * (1 + p1_anlage_liq) + df.loc[i, 'Liquiditätsänderung']

        # Calculate 'Barwert Versorgung' for each group
        for idx, group in enumerate(st.session_state['groups']):
            if i == 1:
                df.loc[i, f'Barwert Versorgung Gruppe {idx+1}'] = an_ag_finanziert_jaehrlich_list[idx] * (1 + zins_zusage_list[idx])
            else:
                if i <= group['laufzeit']-1:
                    df.loc[i, f'Barwert Versorgung Gruppe {idx+1}'] = df.loc[i - 1, f'Barwert Versorgung Gruppe {idx+1}'] * (1 + zins_zusage_list[idx]) + an_ag_finanziert_jaehrlich_list[idx] * (1 + zins_zusage_list[idx])
                else:
                    df.loc[i, f'Barwert Versorgung Gruppe {idx+1}'] = 0

        df.loc[i, 'Barwert Versorgung gesamt'] = sum(df.loc[i, f'Barwert Versorgung Gruppe {idx+1}'] for idx in range(len(st.session_state['groups'])))


# Logo Display
logo_path = "ressources/demak.png"  # Adjust the path to your logo file
logo = Image.open(logo_path)
new_size = (int(logo.width * 1), int(logo.height * 1))
resized_logo = logo.resize(new_size)
st.image(resized_logo)

# KPIs Display
st.title('KPIs')
col1, col2, col3, col4 = st.columns(4)
col1.markdown(custom_metric_html.format(label="AN finanziert jährlich gesamt", value=format_german(an_finanziert_jaehrlich_gesamt)), unsafe_allow_html=True)
col2.markdown(custom_metric_html.format(label="AG finanziert jährlich gesamt", value=format_german(ag_finanziert_jaehrlich_gesamt)), unsafe_allow_html=True)
col3.markdown(custom_metric_html.format(label="AN + AG finanziert jährlich gesamt", value=format_german(an_ag_finanziert_jaehrlich_gesamt)), unsafe_allow_html=True)
col4.markdown(custom_metric_html.format(label="Kapital bei Ablauf", value=format_german(kapital_bei_ablauf_gesamt)), unsafe_allow_html=True)

# Display the DataFrame
df = df.round(2)
st.dataframe(df)

# CSV Download Button
csv = df.to_csv(index=False)
st.download_button(
    label="Als CSV herunterladen",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
)

#Header
st.title("   ")
st.title("Eröffnungsbilanz")
aktiva, passiva = st.columns(2)
with aktiva:
    st.header("Aktiva")
with passiva:
    st.header("Passiva")

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

#Sheet
aktiva_label, aktiva_value, passiva_label, passiva_value = st.columns(4)

with aktiva_label:
    st.subheader("1 Anlagevermögen")
    st.subheader("2 Umlaufvermögen")
    st.subheader("2.1 Vorräte")
    st.subheader("2.2 kurzfristige Forderungen")
    st.subheader("2.3 Zahlungsmittel")
with aktiva_value:
    st.subheader(format_german(anlagevermoegen))
    st.subheader(format_german(umlaufvermögen))
    st.subheader(format_german(vorraete))
    st.subheader(format_german(kurzfristige_forderungen))
    st.subheader(format_german(zahlungsmittel))
with passiva_label:
    st.subheader("1 Eigenkapital")
    st.subheader("2 Fremdkapital")
    st.subheader("2.1 kurzfristig (FK kurzfr.)")
    st.subheader("2.2 langfristig (FK langfr.)")
with passiva_value:
    st.subheader(format_german(eigenkapital))
    st.subheader(format_german(fremdkapital))
    st.subheader(format_german(fk_kurzfristig))
    st.subheader(format_german(fk_langfristig))

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

# Create two columns for balance sheet
gk_aktiva_label, gk_aktiva_value, gk_passiva_label, gk_passiva_value = st.columns(4)
with gk_aktiva_label:
    st.subheader("Gesamtkapital Aktiva")
with gk_aktiva_value:
    formatted = gesamtkapital_aktiva #locale.format_string("%d", gesamtkapital_aktiva, grouping=True)
    st.subheader(format_german(gesamtkapital_aktiva)) #st.subheader(format_german())
with gk_passiva_label:
    st.subheader("Gesamtkapital Passiva")
with gk_passiva_value:
    formatted = gesamtkapital_passiva #locale.format_string("%d", gesamtkapital_passiva, grouping=True)
    st.subheader(format_german(gesamtkapital_passiva))


#Finanzwirtschaftliche Bilanzkennzahlen
eigenkapital_quote_1 = safe_division(eigenkapital,gesamtkapital_passiva)
anspannungsgrad_1 = safe_division(fremdkapital,gesamtkapital_passiva)
statischer_verschuldungsgrad_1 = safe_division(fremdkapital,eigenkapital)
intensitaet_langfristiges_kapital_1 = safe_division((eigenkapital+fk_langfristig),gesamtkapital_passiva)
liquiditaet_1_grades_1 = safe_division(zahlungsmittel,fk_kurzfristig)
liquiditaet_2_grades_1 = safe_division((zahlungsmittel+kurzfristige_forderungen),fk_kurzfristig)
liquiditaet_3_grades_1 = safe_division((zahlungsmittel+kurzfristige_forderungen+vorraete),fk_kurzfristig)
net_working_capital_1 = umlaufvermögen-fk_kurzfristig
deckungsgrad_a_1 = safe_division(eigenkapital,anlagevermoegen)
deckungsgrad_b_1 = safe_division((eigenkapital+fk_langfristig),anlagevermoegen)

st.title("   ")
st.title("Finanzwirtschaftliche Bilanzkennzahlen")
col1, col2, col3, col4, col5 = st.columns(5)

if show_eigenkapital_quote:
    col1.markdown(custom_metric_html.format(label="Eigenkapitalquote", value=to_percentage(eigenkapital_quote_1)), unsafe_allow_html=True)
if show_intensitaet_langfristiges_kapital:
    col1.markdown(custom_metric_html.format(label="Intensität langfristigen Kapitals", value=to_percentage(intensitaet_langfristiges_kapital_1)), unsafe_allow_html=True)
if show_liquiditaet_1_grades:
    col2.markdown(custom_metric_html.format(label="Liquidität 1. Grades", value=to_percentage(liquiditaet_1_grades_1)), unsafe_allow_html=True)
if show_anspannungsgrad:
    col2.markdown(custom_metric_html.format(label="Anspannungsgrad", value=to_percentage(anspannungsgrad_1)), unsafe_allow_html=True)
if show_liquiditaet_2_grades:
    col3.markdown(custom_metric_html.format(label="Liquidität 2. Grades", value=to_percentage(liquiditaet_2_grades_1)), unsafe_allow_html=True)
if show_statischer_verschuldungsgrad:
    col3.markdown(custom_metric_html.format(label="Statischer Verschuldungsgrad", value=to_percentage(statischer_verschuldungsgrad_1)), unsafe_allow_html=True)
if show_liquiditaet_3_grades:
    col4.markdown(custom_metric_html.format(label="Liquidität 3. Grades", value=to_percentage(liquiditaet_3_grades_1)), unsafe_allow_html=True)
if show_deckungsgrad_a:
    col4.markdown(custom_metric_html.format(label="Deckungsgrad A", value=to_percentage(deckungsgrad_a_1)), unsafe_allow_html=True)
if show_net_working_capital:
    col5.markdown(custom_metric_html.format(label="Net Working Capital", value=format_german(net_working_capital_1)), unsafe_allow_html=True)
if show_deckungsgrad_b:
    col5.markdown(custom_metric_html.format(label="Deckungsgrad B", value=to_percentage(deckungsgrad_b_1)), unsafe_allow_html=True)

if bilanzverlaengerung_j_n == 'ja':
    bilanzverlängerung_txt = 'bei'
elif bilanzverlaengerung_j_n == 'nein':
    bilanzverlängerung_txt = 'ohne'
else:
    bilanzverlängerung_txt = 'error'

#Header
st.title("   ")
st.title("Musterbilanz nach "+ f"{bilanz_nach_jahren} Jahren und Liquiditätsanlage "+ f"{to_percentage(p1_anlage_liq)} "+ f"{bilanzverlängerung_txt} Bilanzverlängerung ")

aktiva, passiva = st.columns(2)
with aktiva:
    st.header("Aktiva")
with passiva:
    st.header("Passiva")

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

#Sheet
aktiva_label, aktiva_value, passiva_label, passiva_value = st.columns(4)

#Balance sheet calculations
anlagevermoegen_2 = anlagevermoegen
vorraete_2 = vorraete
kurzfristige_forderungen_2 = kurzfristige_forderungen

if bilanzverlaengerung_j_n == 'ja':
    if bilanz_nach_jahren == laufzeit_max+1:
        zahlungsmittel_2 = df.loc[bilanz_nach_jahren-1, 'Anlage Liquidität'] + zahlungsmittel
    else:
        zahlungsmittel_2 = df.loc[bilanz_nach_jahren, 'Anlage Liquidität'] + zahlungsmittel
elif bilanzverlaengerung_j_n == 'nein':
    zahlungsmittel_2 = zahlungsmittel
else:
    zahlungsmittel_2 = 0

##umlaufvermögen_2 = vorraete_2 + kurzfristige_forderungen_2 + zahlungsmittel_2
##gesamtkapital_aktiva_2 = anlagevermoegen + umlaufvermögen_2
##fk_kurzfristig_2 = fk_kurzfristig

if bilanzverlaengerung_j_n == 'ja':
    fk_kurzfristig_2 = fk_kurzfristig
elif bilanzverlaengerung_j_n == 'nein':
    if bilanz_nach_jahren == laufzeit_max+1:
        fk_kurzfristig_2 = fk_kurzfristig - df.loc[bilanz_nach_jahren-1, 'Anlage Liquidität']
        if fk_kurzfristig_2 < 0:
            zahlungsmittel_2 = zahlungsmittel_2 + abs(fk_kurzfristig_2)
            fk_kurzfristig_2 = 0
    else:
        fk_kurzfristig_2 = fk_kurzfristig - df.loc[bilanz_nach_jahren, 'Anlage Liquidität']
        if fk_kurzfristig_2 < 0:
            zahlungsmittel_2 = zahlungsmittel_2 + abs(fk_kurzfristig_2)
            fk_kurzfristig_2 = 0
else:
    fk_kurzfristig_2 = 0

if bilanz_nach_jahren == laufzeit_max+1:
    fk_langfristig_2 = fk_langfristig
else:
    fk_langfristig_2 = fk_langfristig + df.loc[bilanz_nach_jahren, 'Tatsächliches Kassenvermögen']
if bilanz_nach_jahren != laufzeit_max+1:
    if (df.loc[bilanz_nach_jahren-1, 'Barwert Versorgung gesamt']-df.loc[bilanz_nach_jahren-1, 'Tatsächliches Kassenvermögen'])>0:
        bilanzanhang_2 = df.loc[bilanz_nach_jahren, 'Barwert Versorgung gesamt']-df.loc[bilanz_nach_jahren, 'Tatsächliches Kassenvermögen']
    else:
        bilanzanhang_2 = 0
else:
    bilanzanhang_2 = 0

umlaufvermögen_2 = vorraete_2 + kurzfristige_forderungen_2 + zahlungsmittel_2
gesamtkapital_aktiva_2 = anlagevermoegen + umlaufvermögen_2
#fk_kurzfristig_2 = fk_kurzfristig

fremdkapital_2 = fk_kurzfristig_2 + fk_langfristig_2 #+ bilanzanhang_2
eigenkapital_2 = gesamtkapital_aktiva_2 - fremdkapital_2
gesamtkapital_passiva_2 = eigenkapital_2 + fremdkapital_2

with aktiva_label:
    st.subheader("1 Anlagevermögen")
    st.subheader("2 Umlaufvermögen")
    st.subheader("2.1 Vorräte")
    st.subheader("2.2 kurzfristige Forderungen")
    st.subheader("2.3 Zahlungsmittel")
with aktiva_value:
    st.subheader(format_german(anlagevermoegen_2))
    st.subheader(format_german(umlaufvermögen_2))
    st.subheader(format_german(vorraete_2))
    st.subheader(format_german(kurzfristige_forderungen_2))
    st.subheader(format_german(zahlungsmittel_2))
with passiva_label:
    st.subheader("1 Eigenkapital")
    st.subheader("2 Fremdkapital")
    st.subheader("2.1 kurzfristig (FK kurzfr.)")
    st.subheader("2.2 langfristig (FK langfr.)")
    #st.subheader("3 Bilanzanhang")
with passiva_value:
    st.subheader(format_german(eigenkapital_2))
    st.subheader(format_german(fremdkapital_2))
    st.subheader(format_german(fk_kurzfristig_2))
    st.subheader(format_german(fk_langfristig_2))
    #st.subheader(format_german(bilanzanhang_2))

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

# Create two columns for balance sheet
gk_aktiva_label, gk_aktiva_value, gk_passiva_label, gk_passiva_value = st.columns(4)
with gk_aktiva_label:
    st.subheader("Gesamtkapital Aktiva")
with gk_aktiva_value:
    formatted = format_german(gesamtkapital_aktiva_2) #locale.format_string("%d", gesamtkapital_aktiva_2, grouping=True)
    st.subheader(format_german(gesamtkapital_aktiva_2))
    #st.subheader(f'{gesamtkapital_aktiva_2:,}'.replace(',','.'))
with gk_passiva_label:
    st.subheader("Gesamtkapital Passiva")
    if bilanzanhang_einblenden == "ja":
        st.subheader("_Bilanzanhang_")
with gk_passiva_value:
    formatted = gesamtkapital_passiva_2 #locale.format_string("%d", gesamtkapital_passiva_2, grouping=True)
    st.subheader(format_german(gesamtkapital_passiva_2))
    if bilanzanhang_einblenden == "ja":
        st.subheader(format_german(bilanzanhang_2))



#Finanzwirtschaftliche Bilanzkennzahlen
eigenkapital_quote_2 = safe_division(eigenkapital_2,gesamtkapital_passiva_2)
anspannungsgrad_2 = safe_division(fremdkapital_2,gesamtkapital_passiva_2)
statischer_verschuldungsgrad_2 = safe_division(fremdkapital_2,eigenkapital_2)
intensitaet_langfristiges_kapital_2 = safe_division((eigenkapital_2+fk_langfristig_2),gesamtkapital_passiva_2)
liquiditaet_1_grades_2 = safe_division(zahlungsmittel_2,fk_kurzfristig_2)
liquiditaet_2_grades_2 = safe_division((zahlungsmittel_2+kurzfristige_forderungen_2),fk_kurzfristig_2)
liquiditaet_3_grades_2 = safe_division((zahlungsmittel_2+kurzfristige_forderungen+vorraete_2),fk_kurzfristig_2)
net_working_capital_2 = umlaufvermögen_2-fk_kurzfristig_2
deckungsgrad_a_2 = safe_division(eigenkapital_2,anlagevermoegen_2)
deckungsgrad_b_2 = safe_division((eigenkapital_2+fk_langfristig_2),anlagevermoegen_2)

eigenkapital_quote_2_change = safe_division(eigenkapital_quote_2,eigenkapital_quote_1)-1
anspannungsgrad_2_change = safe_division(anspannungsgrad_2,anspannungsgrad_1)-1
statischer_verschuldungsgrad_2_change = safe_division(statischer_verschuldungsgrad_2,statischer_verschuldungsgrad_1)-1
intensitaet_langfristiges_kapital_2_change = safe_division(intensitaet_langfristiges_kapital_2,intensitaet_langfristiges_kapital_1)-1
liquiditaet_1_grades_2_change = safe_division(liquiditaet_1_grades_2,liquiditaet_1_grades_1)-1
liquiditaet_2_grades_2_change = safe_division(liquiditaet_2_grades_2,liquiditaet_2_grades_1)-1
liquiditaet_3_grades_2_change = safe_division(liquiditaet_3_grades_2,liquiditaet_3_grades_1)-1
net_working_capital_2_change = net_working_capital_2 - net_working_capital_1 #safe_division(net_working_capital_2,net_working_capital_1)-1
deckungsgrad_a_2_change = safe_division(deckungsgrad_a_2,deckungsgrad_a_1)-1
deckungsgrad_b_2_change = safe_division(deckungsgrad_b_2,deckungsgrad_b_1)-1


if show_previous_balance_sheet == "ja":
    st.title("   ")
    st.title("Finanzwirtschaftliche Bilanzkennzahlen Eröffnungsbilanz")
    col1, col2, col3, col4, col5 = st.columns(5)
    if show_eigenkapital_quote:
        col1.markdown(custom_metric_html.format(label="Eigenkapitalquote", value=to_percentage(eigenkapital_quote_1)), unsafe_allow_html=True)
    if show_intensitaet_langfristiges_kapital:
        col1.markdown(custom_metric_html.format(label="Intensität langfristigen Kapitals", value=to_percentage(intensitaet_langfristiges_kapital_1)), unsafe_allow_html=True)
    if show_liquiditaet_1_grades:
        col2.markdown(custom_metric_html.format(label="Liquidität 1. Grades", value=to_percentage(liquiditaet_1_grades_1)), unsafe_allow_html=True)
    if show_anspannungsgrad:
        col2.markdown(custom_metric_html.format(label="Anspannungsgrad", value=to_percentage(anspannungsgrad_1)), unsafe_allow_html=True)
    if show_liquiditaet_2_grades:
        col3.markdown(custom_metric_html.format(label="Liquidität 2. Grades", value=to_percentage(liquiditaet_2_grades_1)), unsafe_allow_html=True)
    if show_statischer_verschuldungsgrad:
        col3.markdown(custom_metric_html.format(label="Statischer Verschuldungsgrad", value=to_percentage(statischer_verschuldungsgrad_1)), unsafe_allow_html=True)
    if show_liquiditaet_3_grades:
        col4.markdown(custom_metric_html.format(label="Liquidität 3. Grades", value=to_percentage(liquiditaet_3_grades_1)), unsafe_allow_html=True)
    if show_deckungsgrad_a:
        col4.markdown(custom_metric_html.format(label="Deckungsgrad A", value=to_percentage(deckungsgrad_a_1)), unsafe_allow_html=True)
    if show_net_working_capital:
        col5.markdown(custom_metric_html.format(label="Net Working Capital", value=format_german(net_working_capital_1)), unsafe_allow_html=True)
    if show_deckungsgrad_b:
        col5.markdown(custom_metric_html.format(label="Deckungsgrad B", value=to_percentage(deckungsgrad_b_1)), unsafe_allow_html=True)

st.title("   ")
st.title("Finanzwirtschaftliche Bilanzkennzahlen nach "+ f"{bilanz_nach_jahren}" + " Jahren")
col1, col2, col3, col4, col5 = st.columns(5)




def get_change_color(change_value):
    return "green" if change_value > 0 else "red"

if show_eigenkapital_quote:
    col1.markdown(custom_metric_html_with_change.format(
        label="Eigenkapitalquote",
        value=to_percentage(eigenkapital_quote_2),
        change=to_percentage(eigenkapital_quote_2_change),
        change_color=get_change_color(eigenkapital_quote_2_change)),
        unsafe_allow_html=True)

if show_intensitaet_langfristiges_kapital:
    col1.markdown(custom_metric_html_with_change.format(
        label="Intensität langfristigen Kapitals",
        value=to_percentage(intensitaet_langfristiges_kapital_2),
        change=to_percentage(intensitaet_langfristiges_kapital_2_change),
        change_color=get_change_color(intensitaet_langfristiges_kapital_2_change)),
        unsafe_allow_html=True)

if show_liquiditaet_1_grades:
    col2.markdown(custom_metric_html_with_change.format(
        label="Liquidität 1. Grades",
        value=to_percentage(liquiditaet_1_grades_2),
        change=to_percentage(liquiditaet_1_grades_2_change),
        change_color=get_change_color(liquiditaet_1_grades_2_change)),
        unsafe_allow_html=True)

if show_anspannungsgrad:
    col2.markdown(custom_metric_html_with_change.format(
        label="Anspannungsgrad",
        value=to_percentage(anspannungsgrad_2),
        change=to_percentage(anspannungsgrad_2_change),
        change_color=get_change_color(anspannungsgrad_2_change)),
        unsafe_allow_html=True)

if show_liquiditaet_2_grades:
    col3.markdown(custom_metric_html_with_change.format(
        label="Liquidität 2. Grades",
        value=to_percentage(liquiditaet_2_grades_2),
        change=to_percentage(liquiditaet_2_grades_2_change),
        change_color=get_change_color(liquiditaet_2_grades_2_change)),
        unsafe_allow_html=True)

if show_statischer_verschuldungsgrad:
    col3.markdown(custom_metric_html_with_change.format(
        label="Statischer Verschuldungsgrad",
        value=to_percentage(statischer_verschuldungsgrad_2),
        change=to_percentage(statischer_verschuldungsgrad_2_change),
        change_color=get_change_color(statischer_verschuldungsgrad_2_change)),
        unsafe_allow_html=True)

if show_liquiditaet_3_grades:
    col4.markdown(custom_metric_html_with_change.format(
        label="Liquidität 3. Grades",
        value=to_percentage(liquiditaet_3_grades_2),
        change=to_percentage(liquiditaet_3_grades_2_change),
        change_color=get_change_color(liquiditaet_3_grades_2_change)),
        unsafe_allow_html=True)

if show_deckungsgrad_a:
    col4.markdown(custom_metric_html_with_change.format(
        label="Deckungsgrad A",
        value=to_percentage(deckungsgrad_a_2),
        change=to_percentage(deckungsgrad_a_2_change),
        change_color=get_change_color(deckungsgrad_a_2_change)),
        unsafe_allow_html=True)

if show_net_working_capital:
    col5.markdown(custom_metric_html_with_change.format(
        label="Net Working Capital",
        value=format_german(net_working_capital_2),
        change=format_german(net_working_capital_2_change),
        change_color=get_change_color(net_working_capital_2_change)),
        unsafe_allow_html=True)

if show_deckungsgrad_b:
    col5.markdown(custom_metric_html_with_change.format(
        label="Deckungsgrad B",
        value=to_percentage(deckungsgrad_b_2),
        change=to_percentage(deckungsgrad_b_2_change),
        change_color=get_change_color(deckungsgrad_b_2_change)),
        unsafe_allow_html=True)

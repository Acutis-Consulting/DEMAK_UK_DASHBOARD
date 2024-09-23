import streamlit as st
import pandas as pd
from PIL import Image
import plost
import json
import hmac
import base64

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
    if "password_correct" in st.session_state:
        st.error("Passwort falsch test")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

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

def to_percentage(value):
    #v1 = "{:,.2f}".format(value * 100).replace('.', ',')
    v1 = f'{value*100:,.2f} %'
    v2 = v1.replace(',','#')
    v3 = v2.replace('.','&')
    v4 = v3.replace('#','.')
    v5 = v4.replace('&',',')
    return v5

def format_german(value):
    v1 = f'{value:,.2f} €'
    v2 = v1.replace(',','#')
    v3 = v2.replace('.','%')
    v4 = v3.replace('#','.')
    v5 = v4.replace('%',',')
    return v5

#avoid dividing by 0 denominator
def safe_division(numerator, denominator):
    if denominator == 0:
        return 0 # Or whatever value makes sense in this context
    else:
        return numerator / denominator

st.sidebar.header('DEMAK Dashboard `Version 2`')
st.sidebar.title('Simulationsparameter')


uploaded_file = st.sidebar.file_uploader("Parameter Hochladen", type=["json"])

if uploaded_file:
    # Reading the uploaded JSON file
    uploaded_data = json.load(uploaded_file)

    # Update the values from the uploaded data
    #arbeitnehmer_anzahl = uploaded_data.get('Arbeitnehmeranzahl', arbeitnehmer_anzahl)
    #zins_zusage = uploaded_data.get('Zins Zusage', zins_zusage)


if uploaded_file:
    st.sidebar.title('Gruppe 1')
    arbeitnehmer_anzahl_g1 = st.sidebar.number_input('Arbeitnehmeranzahl (AN)',min_value=0,value= uploaded_data.get('Arbeitnehmeranzahl_g1'))
    zins_zusage_g1 = (st.sidebar.number_input('Zins Zusage (%)',min_value=0.0,value= uploaded_data.get('Zins Zusage_g1') )/100)
    an_fin_jaehrlich_pro_an_g1 = st.sidebar.number_input('AN finanziert jährlich pro AN (€)',min_value=0.0,value=uploaded_data.get('an_fin_jaehrlich_pro_an_g1'))
    ag_fin_jaehrlich_pro_an_g1 = st.sidebar.number_input('AG finanziert jährlich pro AN (€)',min_value=0.0,value=uploaded_data.get('ag_fin_jaehrlich_pro_an_g1'))
    laufzeit_g1 = st.sidebar.number_input('Laufzeit Zusage (Jahre)',min_value=0,value=uploaded_data.get('laufzeit_g1'))

    st.sidebar.title('Gruppe 2')
    arbeitnehmer_anzahl_g2 = st.sidebar.number_input('Arbeitnehmeranzahl (AN) ',min_value=0,value= uploaded_data.get('Arbeitnehmeranzahl_g2'))
    zins_zusage_g2 = (st.sidebar.number_input('Zins Zusage (%) ',min_value=0.0,value= uploaded_data.get('Zins Zusage_g2') )/100)
    an_fin_jaehrlich_pro_an_g2 = st.sidebar.number_input('AN finanziert jährlich pro AN (€) ',min_value=0.0,value=uploaded_data.get('an_fin_jaehrlich_pro_an_g2'))
    ag_fin_jaehrlich_pro_an_g2 = st.sidebar.number_input('AG finanziert jährlich pro AN (€) ',min_value=0.0,value=uploaded_data.get('ag_fin_jaehrlich_pro_an_g2'))
    laufzeit_g2 = st.sidebar.number_input('Laufzeit Zusage (Jahre) ',min_value=0,value=uploaded_data.get('laufzeit_g2'))

    st.sidebar.title('Gruppe 3')
    arbeitnehmer_anzahl_g3 = st.sidebar.number_input('Arbeitnehmeranzahl (AN)  ',min_value=0,value= uploaded_data.get('Arbeitnehmeranzahl_g3'))
    zins_zusage_g3 = (st.sidebar.number_input('Zins Zusage (%)  ',min_value=0.0,value= uploaded_data.get('Zins Zusage_g3') )/100)
    an_fin_jaehrlich_pro_an_g3 = st.sidebar.number_input('AN finanziert jährlich pro AN (€)  ',min_value=0.0,value=uploaded_data.get('an_fin_jaehrlich_pro_an_g3'))
    ag_fin_jaehrlich_pro_an_g3 = st.sidebar.number_input('AG finanziert jährlich pro AN (€)  ',min_value=0.0,value=uploaded_data.get('ag_fin_jaehrlich_pro_an_g3'))
    laufzeit_g3 = st.sidebar.number_input('Laufzeit Zusage (Jahre)  ',min_value=0,value=uploaded_data.get('laufzeit_g3'))

    st.sidebar.title('Allgemeine Parameter')
    darlehenszins = (st.sidebar.number_input('Darlehenszins (%)',min_value=0.0,value=uploaded_data.get('darlehenszins'))/100)
    psv_beitragssatz = (st.sidebar.number_input('PSV-Beitragssatz (%)',min_value=0.0,value=uploaded_data.get('psv_beitragssatz'))/100)
    uk_verwaltung_jaehrlich_pro_an = st.sidebar.number_input('UK Verwaltung jährlich pro AN',min_value=0,value=uploaded_data.get('uk_verwaltung_jaehrlich_pro_an'))
    uk_verwaltung_einmalig_im_ersten_jahr = (st.sidebar.number_input('UK Verwaltung einmalig im ersten Jahr (%)',min_value=0.0,value=uploaded_data.get('uk_verwaltung_einmalig_im_ersten_jahr'))/100)
    p1_anlage_liq = (st.sidebar.number_input('Anlage Liquidität (%)',min_value=0.0,value=uploaded_data.get('p1_anlage_liq'))/100)
    beitragsbemessungsgrenze = st.sidebar.number_input('Beitragsbemessungsgrenze pro Monat (€)',min_value=0,value=uploaded_data.get('beitragsbemessungsgrenze'))

else:
    st.sidebar.title('Gruppe 1')
    arbeitnehmer_anzahl_g1 = st.sidebar.number_input('Arbeitnehmeranzahl (AN)',min_value=0,value=100)
    zins_zusage_g1 = (st.sidebar.number_input('Zins Zusage (%)',min_value=0.0,value=0.00)/100)
    an_fin_jaehrlich_pro_an_g1 = st.sidebar.number_input('AN finanziert jährlich pro AN (€)',min_value=0.0,value=0.0)
    ag_fin_jaehrlich_pro_an_g1 = st.sidebar.number_input('AG finanziert jährlich pro AN (€)',min_value=0.0,value=0.0)
    laufzeit_g1 = st.sidebar.number_input('Laufzeit Zusage (Jahre)',min_value=0,value=0)

    st.sidebar.title('Gruppe 2')
    arbeitnehmer_anzahl_g2 = st.sidebar.number_input('Arbeitnehmeranzahl (AN) ',min_value=0,value=0)
    zins_zusage_g2 = (st.sidebar.number_input('Zins Zusage (%) ',min_value=0.0,value=0.00)/100)
    an_fin_jaehrlich_pro_an_g2 = st.sidebar.number_input('AN finanziert jährlich pro AN (€) ',min_value=0.0,value=0.0)
    ag_fin_jaehrlich_pro_an_g2 = st.sidebar.number_input('AG finanziert jährlich pro AN (€) ',min_value=0.0,value=0.0)
    laufzeit_g2 = st.sidebar.number_input('Laufzeit Zusage (Jahre) ',min_value=0,value=0)

    st.sidebar.title('Gruppe 3')
    arbeitnehmer_anzahl_g3 = st.sidebar.number_input('Arbeitnehmeranzahl (AN)  ',min_value=0,value=0)
    zins_zusage_g3 = (st.sidebar.number_input('Zins Zusage (%)  ',min_value=0.0,value=0.00)/100)
    an_fin_jaehrlich_pro_an_g3 = st.sidebar.number_input('AN finanziert jährlich pro AN (€)  ',min_value=0.0,value=0.0)
    ag_fin_jaehrlich_pro_an_g3 = st.sidebar.number_input('AG finanziert jährlich pro AN (€)  ',min_value=0.0,value=0.0)
    laufzeit_g3 = st.sidebar.number_input('Laufzeit Zusage (Jahre)  ',min_value=0,value=0)



    st.sidebar.title('Allgemeine Parameter')
    darlehenszins = (st.sidebar.number_input('Darlehenszins (%)',min_value=0.0,value=7.50)/100)
    psv_beitragssatz = (st.sidebar.number_input('PSV-Beitragssatz (%)',min_value=0.0,value=0.25)/100)
    uk_verwaltung_jaehrlich_pro_an = st.sidebar.number_input('UK Verwaltung jährlich pro AN',min_value=0,value=89)
    uk_verwaltung_einmalig_im_ersten_jahr = (st.sidebar.number_input('UK Verwaltung einmalig im ersten Jahr (%)',min_value=0.0,value=2.00)/100)
    p1_anlage_liq = (st.sidebar.number_input('Anlage Liquidität (%)',min_value=0.0,value=0.0)/100)
    beitragsbemessungsgrenze = st.sidebar.number_input('Beitragsbemessungsgrenze pro Monat (€)',min_value=0,value=7300) #7.300*12*0,04=3.504

steuern_UK = 0.1583 #(st.sidebar.number_input('Steuern UK (e.V.) (%)',min_value=0.0,value=15.83)/100)
steuer_ersparnis = 0.3 #(st.sidebar.number_input('Steuerersparnis (%)',min_value=0.0,value=30.00)/100)
passiva_2 = 0


st.sidebar.title('Eröffnungsbilanz')
col3, col4 = st.sidebar.columns(2)
col3.subheader('Aktiva')
col4.subheader('Passiva')

if uploaded_file:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        anlagevermoegen = st.number_input('Anlagevermögen',min_value=0,value=uploaded_data.get('Anlagevermögen'))
        umlaufvermögen = st.number_input('Umlaufvermögen',min_value=0,value=0, disabled=True)
        vorraete = st.number_input('Vorräte',min_value=0,value=uploaded_data.get('Vorräte'))
        kurzfristige_forderungen = st.number_input('Kurzfristige Forderungen',min_value=0,value=uploaded_data.get('Kurzfristige Forderungen'))
        zahlungsmittel = st.number_input('Zahlungsmittel',min_value=0,value=uploaded_data.get('Zahlungsmittel'))
    with col2:
        eigenkapital = st.number_input('Eigenkapital',min_value=0,value=0, disabled=True)
        fremdkapital = st.number_input('Fremdkapital',min_value=0,value=0, disabled=True)
        fk_kurzfristig = st.number_input('kurzfristig (FK kurzfr.)',min_value=0,value=uploaded_data.get('kurzfristig (FK kurzfr.)'))
        fk_langfristig = st.number_input('langfristig (FK langfr.)',min_value=0,value=uploaded_data.get('langfristig (FK langfr.)'))
else:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        anlagevermoegen = st.number_input('Anlagevermögen',min_value=0,value=0)
        umlaufvermögen = st.number_input('Umlaufvermögen',min_value=0,value=0, disabled=True)
        vorraete = st.number_input('Vorräte',min_value=0,value=0)
        kurzfristige_forderungen = st.number_input('Kurzfristige Forderungen',min_value=0,value=0)
        zahlungsmittel = st.number_input('Zahlungsmittel',min_value=0,value=0)
    with col2:
        eigenkapital = st.number_input('Eigenkapital',min_value=0,value=0, disabled=True)
        fremdkapital = st.number_input('Fremdkapital',min_value=0,value=0, disabled=True)
        fk_kurzfristig = st.number_input('kurzfristig (FK kurzfr.)',min_value=0,value=0)
        fk_langfristig = st.number_input('langfristig (FK langfr.)',min_value=0,value=0)

# Create options from 1 to x
default_index = 0
laufzeit_max = max(laufzeit_g1,laufzeit_g2,laufzeit_g3)
options = list(range(1, laufzeit_max + 2))
st.sidebar.title('Musterbilanz')
# Create a selectbox with the options

c1, c2 = st.sidebar.columns(2)
with c1:
    bilanz_nach_jahren = st.selectbox('Bilanz nach X Jahren:', options, index=default_index)
    show_previous_balance_sheet = st.selectbox('Bilanzkennzahlen einblenden:', ('nein','ja'))
with c2:
    bilanzverlaengerung_j_n = st.selectbox('Bilanzverlängerung:', ('ja', 'nein'))
    bilanzanhang_einblenden = st.selectbox('Bilanzanhang einblenden:', ('nein', 'ja'))

# Define flags for each metric's visibility
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

# Add a button to trigger the save
st.sidebar.title(' ')
if st.sidebar.button('Parameter Speichern'):
    # Creating a dictionary of parameters to save
    data_to_save = {
        ### Gruppe 1
        'Arbeitnehmeranzahl_g1': arbeitnehmer_anzahl_g1,
        'Zins Zusage_g1': zins_zusage_g1*100,
        'an_fin_jaehrlich_pro_an_g1': an_fin_jaehrlich_pro_an_g1,
        'ag_fin_jaehrlich_pro_an_g1': ag_fin_jaehrlich_pro_an_g1,
        'laufzeit_g1': laufzeit_g1,

        ### Gruppe 2
        'Arbeitnehmeranzahl_g2': arbeitnehmer_anzahl_g2,
        'Zins Zusage_g2': zins_zusage_g2*100,
        'an_fin_jaehrlich_pro_an_g2': an_fin_jaehrlich_pro_an_g2,
        'ag_fin_jaehrlich_pro_an_g2': ag_fin_jaehrlich_pro_an_g2,
        'laufzeit_g2': laufzeit_g2,

        ### Gruppe 3
        'Arbeitnehmeranzahl_g3': arbeitnehmer_anzahl_g3,
        'Zins Zusage_g3': zins_zusage_g3*100,
        'an_fin_jaehrlich_pro_an_g3': an_fin_jaehrlich_pro_an_g3,
        'ag_fin_jaehrlich_pro_an_g3': ag_fin_jaehrlich_pro_an_g3,
        'laufzeit_g3': laufzeit_g3,

        'darlehenszins': darlehenszins*100,
        'psv_beitragssatz': psv_beitragssatz*100,
        'uk_verwaltung_jaehrlich_pro_an': uk_verwaltung_jaehrlich_pro_an,
        'uk_verwaltung_einmalig_im_ersten_jahr': uk_verwaltung_einmalig_im_ersten_jahr*100,
        'p1_anlage_liq': p1_anlage_liq*100,
        'Anlagevermögen': anlagevermoegen,
        'Vorräte': vorraete,
        'Kurzfristige Forderungen': kurzfristige_forderungen,
        'Zahlungsmittel': zahlungsmittel,
        'kurzfristig (FK kurzfr.)': fk_kurzfristig,
        'langfristig (FK langfr.)': fk_langfristig,
        'beitragsbemessungsgrenze': beitragsbemessungsgrenze
    }

    # Convert dictionary to JSON string
    json_str = json.dumps(data_to_save, indent=4)

    # Convert the string to bytes
    b64 = base64.b64encode(json_str.encode()).decode()

    # Provide a link to download the JSON file
    href = f'<a href="data:file/json;base64,{b64}" download="parameters.json">Parameter Herunterladen</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

#Balance sheet calculations
umlaufvermögen = vorraete+kurzfristige_forderungen+zahlungsmittel
gesamtkapital_aktiva = anlagevermoegen + umlaufvermögen
fremdkapital = fk_kurzfristig + fk_langfristig
eigenkapital = gesamtkapital_aktiva - fremdkapital
gesamtkapital_passiva = eigenkapital + fremdkapital
arbeitnehmer_anzahl_gesamt = arbeitnehmer_anzahl_g1 + arbeitnehmer_anzahl_g2 + arbeitnehmer_anzahl_g3

# Create Dataframe
df = pd.DataFrame()
an_finanziert_jaehrlich_g1 = arbeitnehmer_anzahl_g1 * an_fin_jaehrlich_pro_an_g1
an_finanziert_jaehrlich_g2 = arbeitnehmer_anzahl_g2 * an_fin_jaehrlich_pro_an_g2
an_finanziert_jaehrlich_g3 = arbeitnehmer_anzahl_g3 * an_fin_jaehrlich_pro_an_g3
an_finanziert_jaehrlich_gesamt = an_finanziert_jaehrlich_g1 + an_finanziert_jaehrlich_g2 + an_finanziert_jaehrlich_g3

an_finanziert_jaehrlich_max_sv_frei_g1 = arbeitnehmer_anzahl_g1 * (beitragsbemessungsgrenze*12*0.04)
an_finanziert_jaehrlich_max_sv_frei_g2 = arbeitnehmer_anzahl_g2 * (beitragsbemessungsgrenze*12*0.04)
an_finanziert_jaehrlich_max_sv_frei_g3 = arbeitnehmer_anzahl_g3 * (beitragsbemessungsgrenze*12*0.04)
an_finanziert_jaehrlich_gesamt_max_sv_frei = an_finanziert_jaehrlich_max_sv_frei_g1 + an_finanziert_jaehrlich_max_sv_frei_g2 + an_finanziert_jaehrlich_max_sv_frei_g3

ag_finanziert_jaehrlich_g1 = arbeitnehmer_anzahl_g1*ag_fin_jaehrlich_pro_an_g1
ag_finanziert_jaehrlich_g2 = arbeitnehmer_anzahl_g2*ag_fin_jaehrlich_pro_an_g2
ag_finanziert_jaehrlich_g3 = arbeitnehmer_anzahl_g3*ag_fin_jaehrlich_pro_an_g3
ag_finanziert_jaehrlich_gesamt = ag_finanziert_jaehrlich_g1 + ag_finanziert_jaehrlich_g2 + ag_finanziert_jaehrlich_g3

an_ag_finanziert_jaehrlich_g1 = an_finanziert_jaehrlich_g1 + ag_finanziert_jaehrlich_g1
an_ag_finanziert_jaehrlich_g2 = an_finanziert_jaehrlich_g2 + ag_finanziert_jaehrlich_g2
an_ag_finanziert_jaehrlich_g3 = an_finanziert_jaehrlich_g3 + ag_finanziert_jaehrlich_g3
an_ag_finanziert_jaehrlich_gesamt = an_ag_finanziert_jaehrlich_g1 + an_ag_finanziert_jaehrlich_g2 + an_ag_finanziert_jaehrlich_g3

kapital_bei_ablauf_g1 = safe_division((pow((1+zins_zusage_g1),laufzeit_g1)-1),zins_zusage_g1)*(1+zins_zusage_g1)*an_ag_finanziert_jaehrlich_g1
kapital_bei_ablauf_g2 = safe_division((pow((1+zins_zusage_g2),laufzeit_g2)-1),zins_zusage_g2)*(1+zins_zusage_g2)*an_ag_finanziert_jaehrlich_g2
kapital_bei_ablauf_g3 = safe_division((pow((1+zins_zusage_g3),laufzeit_g3)-1),zins_zusage_g3)*(1+zins_zusage_g3)*an_ag_finanziert_jaehrlich_g3
kapital_bei_ablauf_gesamt = kapital_bei_ablauf_g1 + kapital_bei_ablauf_g2 + kapital_bei_ablauf_g3

debug = zins_zusage_g1


davon_an_g1 = (safe_division(kapital_bei_ablauf_g1,an_ag_finanziert_jaehrlich_g1))*an_finanziert_jaehrlich_g1
davon_an_g2 = (safe_division(kapital_bei_ablauf_g2,an_ag_finanziert_jaehrlich_g2))*an_finanziert_jaehrlich_g2
davon_an_g3 = (safe_division(kapital_bei_ablauf_g3,an_ag_finanziert_jaehrlich_g3))*an_finanziert_jaehrlich_g3
davon_an_gesamt = davon_an_g1 + davon_an_g2 + davon_an_g3

#Initialize Columns:
df['Jahr'] = range(1, laufzeit_max +2)

# initialize fields
df['Zulässiges Kassenvemögen'] = 0 #B
df['Höchstzulässiges Kassenvermögen'] = 0 #C
df['Zulässige Dotierung'] = 0 #D
df['Überdotierung'] = 0 #E
df['Darlehenszinsen'] = 0 #F
df['Zinsanteil Überdotierung'] = 0 #G
df['Steuern UK (e.V.)'] = 0 #H
df['Versorgung fällig'] = 0 #I
df['Darlehensänderung'] = 0 #J
df['Tatsächliches Kassenvermögen'] = 100 #K
df['Kosten UK-Verwaltung'] = 0 #L
df['PSV Beitrag'] = 0 #M
df['EU + SV Ersparnis'] = 0 #N
df['Steuerersparnis'] = 0 #O
df['Liquiditätsänderung'] = 0 #P
df['Anlage Liquidität'] = 0 #Q
df['Barwert Versorgung Gruppe 1'] = 0
df['Barwert Versorgung Gruppe 2'] = 0
df['Barwert Versorgung Gruppe 3'] = 0
df['Barwert Versorgung gesamt'] = 0


# Main loop
for i in range(laufzeit_max+1):
    if i == 0:
        df.loc[i, 'Zulässiges Kassenvemögen'] = (kapital_bei_ablauf_gesamt / 10) * 0.25 * 8 #B
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = df.loc[i, 'Zulässiges Kassenvemögen']*1.25 #C
        df.loc[i, 'Zulässige Dotierung'] = (kapital_bei_ablauf_gesamt/10*0.25)
        df.loc[i, 'Tatsächliches Kassenvermögen'] =df.loc[i, 'Zulässige Dotierung']
        #df.loc[i, 'PSV Beitrag'] = (davon_an/10)*0.25*20*psv_beitragssatz #M ###vorGruppen
        df.loc[i, 'PSV Beitrag'] = (davon_an_gesamt/10)*0.25*20*psv_beitragssatz
        df.loc[i, 'Kosten UK-Verwaltung'] = (kapital_bei_ablauf_gesamt * uk_verwaltung_einmalig_im_ersten_jahr)+(arbeitnehmer_anzahl_gesamt * uk_verwaltung_jaehrlich_pro_an)
        df.loc[i, 'EU + SV Ersparnis'] = min(an_finanziert_jaehrlich_gesamt*1.2,an_finanziert_jaehrlich_gesamt_max_sv_frei*1.2) + max(0,(an_finanziert_jaehrlich_gesamt-an_finanziert_jaehrlich_gesamt_max_sv_frei)) #
        df.loc[i, 'Steuerersparnis'] = (df.loc[i, 'EU + SV Ersparnis']-df.loc[i,'PSV Beitrag']-df.loc[i,'Kosten UK-Verwaltung']-df.loc[i,'Zulässige Dotierung'])*steuer_ersparnis*-1
        df.loc[i, 'Liquiditätsänderung'] = df.loc[i, 'EU + SV Ersparnis']+ df.loc[i,'Steuerersparnis']-df.loc[i, 'PSV Beitrag']-df.loc[i, 'Kosten UK-Verwaltung']
        df.loc[i, 'Anlage Liquidität'] = df.loc[i, 'Liquiditätsänderung']
        df.loc[i, 'Barwert Versorgung Gruppe 1'] = 0
        df.loc[i, 'Barwert Versorgung Gruppe 2'] = 0
        df.loc[i, 'Barwert Versorgung Gruppe 3'] = 0
        df.loc[i, 'Barwert Versorgung gesamt'] = df.loc[i, 'Barwert Versorgung Gruppe 1'] + df.loc[i, 'Barwert Versorgung Gruppe 2'] + df.loc[i, 'Barwert Versorgung Gruppe 3']
        pass

    elif i == (laufzeit_max):
        df.loc[i, 'Zulässiges Kassenvemögen'] = 0
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = 0

        if i == laufzeit_g1:
            df.loc[i, 'Versorgung fällig'] = kapital_bei_ablauf_g1
        elif i == laufzeit_g2:
            df.loc[i, 'Versorgung fällig'] = kapital_bei_ablauf_g2
        elif i == laufzeit_g3:
            df.loc[i, 'Versorgung fällig'] = kapital_bei_ablauf_g3
        else:
            df.loc[i, 'Versorgung fällig'] = 0 #I

        df['Darlehenszinsen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) * darlehenszins #F ###Check
        df.loc[i,'Tatsächliches Kassenvermögen'] = 0 ##ÄNDERUNG
        df['Überdotierung'] = df['Tatsächliches Kassenvermögen'] - df['Höchstzulässiges Kassenvermögen'] #E

        if df.loc[i-1, 'Überdotierung'] > 0:
            df.loc[i, 'Zinsanteil Überdotierung'] = (df.loc[i-1, 'Überdotierung'] / df.loc[i-1, 'Tatsächliches Kassenvermögen']) * df.loc[i-1, 'Darlehenszinsen'] #G
        else:
            df.loc[i, 'Zinsanteil Überdotierung'] = 0 ##ÄNDERUNG

        df.loc[df['Überdotierung'] >= 0, 'Steuern UK (e.V.)'] = (df['Zinsanteil Überdotierung']*steuern_UK) #H

        if (i == laufzeit_g1 or i == laufzeit_g2 or i == laufzeit_g3):
            df.loc[i,'Zulässige Dotierung'] = df.loc[i, 'Zulässiges Kassenvemögen'] + df.loc[i, 'Versorgung fällig'] - df.loc[i, 'Darlehenszinsen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] + df.loc[i, 'Steuern UK (e.V.)']

        df.loc[i,'Darlehensänderung'] = df.loc[i, 'Zulässige Dotierung'] + df.loc[i, 'Darlehenszinsen'] - df.loc[i, 'Steuern UK (e.V.)'] - df.loc[i, 'Versorgung fällig']  #J ###ÄNDERUNG

        df.loc[i, 'EU + SV Ersparnis'] = 0

        if i < laufzeit_g1+1 and i < laufzeit_g2+1 and i < laufzeit_g3+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g1+arbeitnehmer_anzahl_g2+arbeitnehmer_anzahl_g3)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g1+1 and i < laufzeit_g2+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g1+arbeitnehmer_anzahl_g2)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g2 and i < laufzeit_g3:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g2+arbeitnehmer_anzahl_g3)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g1 and i < laufzeit_g3:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g1+arbeitnehmer_anzahl_g3)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g1+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g1)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g2+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g2)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g3+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g3)*uk_verwaltung_jaehrlich_pro_an
        else:
            df.loc[i, 'Kosten UK-Verwaltung'] = 0

        if i > 2:
            if i < laufzeit_g1+1 and i < laufzeit_g2+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g2+kapital_bei_ablauf_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1 and i < laufzeit_g2+1:
                df.loc[i, 'PSV Beitrag'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g2)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g2+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((kapital_bei_ablauf_g2+kapital_bei_ablauf_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1:
                df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf_g1/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g2+1:
                df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf_g2/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf_g3/10)*0.25*20*psv_beitragssatz
            else:
                df.loc[i, 'PSV Beitrag'] = 0
        else:
            if i < laufzeit_g1+1 and i < laufzeit_g2+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((davon_an_g1+davon_an_g2+davon_an_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1 and i < laufzeit_g2+1:
                df.loc[i, 'PSV Beitrag'] = ((davon_an_g1+davon_an_g2)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g2+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((davon_an_g2+davon_an_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((davon_an_g1+davon_an_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1:
                df.loc[i, 'PSV Beitrag'] = (davon_an_g1/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g2+1:
                df.loc[i, 'PSV Beitrag'] = (davon_an_g2/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = (davon_an_g3/10)*0.25*20*psv_beitragssatz
            else:
                df.loc[i, 'PSV Beitrag'] = 0

        df['Steuerersparnis'] = (df['EU + SV Ersparnis']-df['PSV Beitrag']-df['Kosten UK-Verwaltung']-df['Darlehenszinsen']-df['Zulässige Dotierung'])*steuer_ersparnis*-1 #O
        df['Liquiditätsänderung'] = df['EU + SV Ersparnis']+df['Steuerersparnis']-df['PSV Beitrag']-df['Kosten UK-Verwaltung']-df['Steuern UK (e.V.)']-df['Versorgung fällig']
        df.loc[i, 'Anlage Liquidität'] = df.loc[i-1, 'Anlage Liquidität']*(1+p1_anlage_liq)+df.loc[i, 'Liquiditätsänderung']
        df.loc[i, 'Barwert Versorgung gesamt'] = df.loc[i, 'Barwert Versorgung Gruppe 1'] + df.loc[i, 'Barwert Versorgung Gruppe 2'] + df.loc[i, 'Barwert Versorgung Gruppe 3']
        pass

    else:
        # calculations for subsequent years
        if i < laufzeit_g1 and i < laufzeit_g2 and i < laufzeit_g3:
            df.loc[i, 'Zulässiges Kassenvemögen'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g2+kapital_bei_ablauf_g3) / 10) * 0.25 * 8 #B
        elif i < laufzeit_g1 and i < laufzeit_g2:
            df.loc[i, 'Zulässiges Kassenvemögen'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g2) / 10) * 0.25 * 8 #B
        elif i < laufzeit_g2 and i < laufzeit_g3:
            df.loc[i, 'Zulässiges Kassenvemögen'] = ((kapital_bei_ablauf_g2+kapital_bei_ablauf_g3) / 10) * 0.25 * 8 #B
        elif i < laufzeit_g1 and i < laufzeit_g3:
            df.loc[i, 'Zulässiges Kassenvemögen'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g3) / 10) * 0.25 * 8 #B
        elif i < laufzeit_g1:
            df.loc[i, 'Zulässiges Kassenvemögen'] = ((kapital_bei_ablauf_g1) / 10) * 0.25 * 8 #B
        elif i < laufzeit_g2:
            df.loc[i, 'Zulässiges Kassenvemögen'] = ((kapital_bei_ablauf_g2) / 10) * 0.25 * 8 #B
        elif i < laufzeit_g3:
            df.loc[i, 'Zulässiges Kassenvemögen'] = ((kapital_bei_ablauf_g3) / 10) * 0.25 * 8 #B
        else:
            df.loc[i, 'Zulässiges Kassenvemögen'] = 0

        if i > 2:
            if i < laufzeit_g1+1 and i < laufzeit_g2+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g2+kapital_bei_ablauf_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1 and i < laufzeit_g2+1:
                df.loc[i, 'PSV Beitrag'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g2)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g2+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((kapital_bei_ablauf_g2+kapital_bei_ablauf_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((kapital_bei_ablauf_g1+kapital_bei_ablauf_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1:
                df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf_g1/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g2+1:
                df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf_g2/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf_g3/10)*0.25*20*psv_beitragssatz
            else:
                df.loc[i, 'PSV Beitrag'] = 0
        else:
            if i < laufzeit_g1+1 and i < laufzeit_g2+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((davon_an_g1+davon_an_g2+davon_an_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1 and i < laufzeit_g2+1:
                df.loc[i, 'PSV Beitrag'] = ((davon_an_g1+davon_an_g2)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g2+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((davon_an_g2+davon_an_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1 and i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = ((davon_an_g1+davon_an_g3)/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g1+1:
                df.loc[i, 'PSV Beitrag'] = (davon_an_g1/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g2+1:
                df.loc[i, 'PSV Beitrag'] = (davon_an_g2/10)*0.25*20*psv_beitragssatz
            elif i < laufzeit_g3+1:
                df.loc[i, 'PSV Beitrag'] = (davon_an_g3/10)*0.25*20*psv_beitragssatz
            else:
                df.loc[i, 'PSV Beitrag'] = 0

        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = df.loc[i, 'Zulässiges Kassenvemögen']*1.25 #C
        df['Darlehenszinsen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) * darlehenszins #F ###Check

        if i == laufzeit_g1:
            df.loc[i, 'Versorgung fällig'] = kapital_bei_ablauf_g1
        elif i == laufzeit_g2:
            df.loc[i, 'Versorgung fällig'] = kapital_bei_ablauf_g2
        elif i == laufzeit_g3:
            df.loc[i, 'Versorgung fällig'] = kapital_bei_ablauf_g3
        else:
            df.loc[i, 'Versorgung fällig'] = 0 #I

        if df.loc[i-1, 'Überdotierung'] > 0:
            df.loc[i, 'Zinsanteil Überdotierung'] = (df.loc[i-1, 'Überdotierung'] / df.loc[i-1, 'Tatsächliches Kassenvermögen']) * df.loc[i-1, 'Darlehenszinsen'] #G
        else:
            df.loc[i, 'Zinsanteil Überdotierung'] = 0 ##ÄNDERUNG

        df.loc[df['Überdotierung'] > 0, 'Steuern UK (e.V.)'] = (df['Zinsanteil Überdotierung']*steuern_UK) #H

        if (df.loc[i-1, 'Tatsächliches Kassenvermögen']+df.loc[i, 'Darlehenszinsen']+(kapital_bei_ablauf_gesamt/10)*0.25) <= df.loc[i, 'Zulässiges Kassenvemögen']:
            df.loc[i,'Zulässige Dotierung'] = (kapital_bei_ablauf_gesamt/10)*0.25
        elif ((df.loc[i-1, 'Tatsächliches Kassenvermögen']+df.loc[i, 'Darlehenszinsen']+(kapital_bei_ablauf_gesamt/10)*0.25) > df.loc[i, 'Zulässiges Kassenvemögen']):
            if (df.loc[i, 'Zulässiges Kassenvemögen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Darlehenszinsen'])>0:
                df.loc[i,'Zulässige Dotierung'] = df.loc[i, 'Zulässiges Kassenvemögen'] + df.loc[i, 'Versorgung fällig'] - df.loc[i, 'Darlehenszinsen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] + df.loc[i, 'Steuern UK (e.V.)']
            else:
                df.loc[i,'Zulässige Dotierung'] = 0
        else:
            df.loc[i,'Zulässige Dotierung'] = 0

        if (i == laufzeit_g1 or i == laufzeit_g2 or i == laufzeit_g3):# and df.loc[i-1, 'Tatsächliches Kassenvermögen'] <= df.loc[i,'Versorgung fällig']:
            df.loc[i,'Zulässige Dotierung'] = max(df.loc[i, 'Zulässiges Kassenvemögen'] + df.loc[i, 'Versorgung fällig'] - df.loc[i, 'Darlehenszinsen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] + df.loc[i, 'Steuern UK (e.V.)'],0)



        df.loc[i,'Darlehensänderung'] = df.loc[i,'Zulässige Dotierung'] + df.loc[i,'Darlehenszinsen'] - df.loc[i,'Steuern UK (e.V.)'] - df.loc[i, 'Versorgung fällig']#J ###ÄNDERUNG
        df.loc[i,'Tatsächliches Kassenvermögen'] = df.loc[i-1,'Tatsächliches Kassenvermögen'] + df.loc[i,'Darlehensänderung'] #- df.loc[i,'Versorgung fällig'] #K

        df['Überdotierung'] = df['Tatsächliches Kassenvermögen'] - df['Höchstzulässiges Kassenvermögen'] #E


        #df.loc[i, 'Kosten UK-Verwaltung'] = arbeitnehmer_anzahl_gesamt*uk_verwaltung_jaehrlich_pro_an #L

        if i < laufzeit_g1+1 and i < laufzeit_g2+1 and i < laufzeit_g3+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g1+arbeitnehmer_anzahl_g2+arbeitnehmer_anzahl_g3)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g1+1 and i < laufzeit_g2+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g1+arbeitnehmer_anzahl_g2)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g2+1 and i < laufzeit_g3+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g2+arbeitnehmer_anzahl_g3)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g1+1 and i < laufzeit_g3+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g1+arbeitnehmer_anzahl_g3)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g1+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g1)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g2+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g2)*uk_verwaltung_jaehrlich_pro_an
        elif i < laufzeit_g3+1:
            df.loc[i, 'Kosten UK-Verwaltung'] = (arbeitnehmer_anzahl_g3)*uk_verwaltung_jaehrlich_pro_an
        else:
            df.loc[i, 'Kosten UK-Verwaltung'] = 0



        if i < laufzeit_g1 and i < laufzeit_g2 and i < laufzeit_g3:
            df.loc[i, 'EU + SV Ersparnis'] = min((an_finanziert_jaehrlich_g1+an_finanziert_jaehrlich_g2+an_finanziert_jaehrlich_g3)*1.2,(an_finanziert_jaehrlich_max_sv_frei_g1+an_finanziert_jaehrlich_max_sv_frei_g2+an_finanziert_jaehrlich_max_sv_frei_g3)*1.2) + max(0,((an_finanziert_jaehrlich_g1+an_finanziert_jaehrlich_g2+an_finanziert_jaehrlich_g3)-(an_finanziert_jaehrlich_max_sv_frei_g1+an_finanziert_jaehrlich_max_sv_frei_g2+an_finanziert_jaehrlich_max_sv_frei_g3))) #
        elif i < laufzeit_g1 and i < laufzeit_g2:
            df.loc[i, 'EU + SV Ersparnis'] = min((an_finanziert_jaehrlich_g1+an_finanziert_jaehrlich_g2)*1.2,(an_finanziert_jaehrlich_max_sv_frei_g1+an_finanziert_jaehrlich_max_sv_frei_g2)*1.2) + max(0,((an_finanziert_jaehrlich_g1+an_finanziert_jaehrlich_g2)-(an_finanziert_jaehrlich_max_sv_frei_g1+an_finanziert_jaehrlich_max_sv_frei_g2)))
        elif i < laufzeit_g2 and i < laufzeit_g3:
            df.loc[i, 'EU + SV Ersparnis'] = min((an_finanziert_jaehrlich_g2+an_finanziert_jaehrlich_g3)*1.2,(an_finanziert_jaehrlich_max_sv_frei_g2+an_finanziert_jaehrlich_max_sv_frei_g3)*1.2) + max(0,((an_finanziert_jaehrlich_g2+an_finanziert_jaehrlich_g3)-(an_finanziert_jaehrlich_max_sv_frei_g2+an_finanziert_jaehrlich_max_sv_frei_g3)))
        elif i < laufzeit_g1 and i < laufzeit_g3:
            df.loc[i, 'EU + SV Ersparnis'] = min((an_finanziert_jaehrlich_g1+an_finanziert_jaehrlich_g3)*1.2,(an_finanziert_jaehrlich_max_sv_frei_g1+an_finanziert_jaehrlich_max_sv_frei_g3)*1.2) + max(0,((an_finanziert_jaehrlich_g1+an_finanziert_jaehrlich_g3)-(an_finanziert_jaehrlich_max_sv_frei_g1+an_finanziert_jaehrlich_max_sv_frei_g3)))
        elif i < laufzeit_g1:
            df.loc[i, 'EU + SV Ersparnis'] = min((an_finanziert_jaehrlich_g1)*1.2,(an_finanziert_jaehrlich_max_sv_frei_g1)*1.2) + max(0,(an_finanziert_jaehrlich_g1-an_finanziert_jaehrlich_max_sv_frei_g1)) #
        elif i < laufzeit_g2:
            df.loc[i, 'EU + SV Ersparnis'] = min((an_finanziert_jaehrlich_g2)*1.2,(an_finanziert_jaehrlich_max_sv_frei_g2)*1.2) + max(0,(an_finanziert_jaehrlich_g2-an_finanziert_jaehrlich_max_sv_frei_g2)) #
        elif i < laufzeit_g3:
            df.loc[i, 'EU + SV Ersparnis'] = min((an_finanziert_jaehrlich_g3)*1.2,(an_finanziert_jaehrlich_max_sv_frei_g3)*1.2) + max(0,(an_finanziert_jaehrlich_g3-an_finanziert_jaehrlich_max_sv_frei_g3)) #
        else:
            df.loc[i, 'EU + SV Ersparnis'] = 0
        #






        #df.loc[i, 'EU + SV Ersparnis'] = min(an_finanziert_jaehrlich_gesamt*1.2,an_finanziert_jaehrlich_gesamt_max_sv_frei*1.2) + max(0,(an_finanziert_jaehrlich_gesamt-an_finanziert_jaehrlich_gesamt_max_sv_frei)) #
        df['Steuerersparnis'] = (df['EU + SV Ersparnis']-df['PSV Beitrag']-df[ 'Kosten UK-Verwaltung']-df['Darlehenszinsen']-df['Zulässige Dotierung'])*steuer_ersparnis*-1 #O
        df['Liquiditätsänderung'] = df['EU + SV Ersparnis']+df['Steuerersparnis']-df['PSV Beitrag']-df['Kosten UK-Verwaltung']-df['Steuern UK (e.V.)'] - df.loc[i, 'Versorgung fällig']  #P #Check if we have to make a different case for row 1
        df.loc[i, 'Anlage Liquidität'] = df.loc[i-1, 'Anlage Liquidität']*(1+p1_anlage_liq) +df.loc[i, 'Liquiditätsänderung'] #Q

        if i == 1:
            df.loc[i, 'Barwert Versorgung Gruppe 1'] = an_ag_finanziert_jaehrlich_g1*(1+zins_zusage_g1)
            df.loc[i, 'Barwert Versorgung Gruppe 2'] = an_ag_finanziert_jaehrlich_g2*(1+zins_zusage_g2)
            df.loc[i, 'Barwert Versorgung Gruppe 3'] = an_ag_finanziert_jaehrlich_g3*(1+zins_zusage_g3)
        else:
            if i < laufzeit_g1:
                df.loc[i, 'Barwert Versorgung Gruppe 1'] = df.loc[i-1, 'Barwert Versorgung Gruppe 1']*(1+zins_zusage_g1) + an_ag_finanziert_jaehrlich_g1*(1+zins_zusage_g1)
            else:
                df.loc[i, 'Barwert Versorgung Gruppe 1'] = 0
            if i < laufzeit_g2:
                df.loc[i, 'Barwert Versorgung Gruppe 2'] = df.loc[i-1, 'Barwert Versorgung Gruppe 2']*(1+zins_zusage_g2) + an_ag_finanziert_jaehrlich_g2*(1+zins_zusage_g2)
            else:
                df.loc[i, 'Barwert Versorgung Gruppe 2'] = 0
            if i < laufzeit_g3:
                df.loc[i, 'Barwert Versorgung Gruppe 3'] = df.loc[i-1, 'Barwert Versorgung Gruppe 3']*(1+zins_zusage_g3) + an_ag_finanziert_jaehrlich_g3*(1+zins_zusage_g3)
            else:
                df.loc[i, 'Barwert Versorgung Gruppe 3'] = 0

        df.loc[i, 'Barwert Versorgung gesamt'] = df.loc[i, 'Barwert Versorgung Gruppe 1'] + df.loc[i, 'Barwert Versorgung Gruppe 2'] + df.loc[i, 'Barwert Versorgung Gruppe 3']



#Logo
logo_path = "ressources/demak.png"  # Adjust the path to your logo file
logo = Image.open(logo_path)
new_size = (int(logo.width * 1), int(logo.height * 1))
resized_logo = logo.resize(new_size)
st.image(resized_logo)

# Row A1
st.title('KPIs')
col1, col2, col3, col4 = st.columns(4)
# Example for AN financed metric using HTML instead of st.metric
col1.markdown(custom_metric_html.format(label="AN finanziert jährlich gesamt", value=format_german(an_finanziert_jaehrlich_gesamt)), unsafe_allow_html=True)
col2.markdown(custom_metric_html.format(label="AG finanziert jährlich gesamt", value=format_german(ag_finanziert_jaehrlich_gesamt)), unsafe_allow_html=True)
col3.markdown(custom_metric_html.format(label="AN + AG finanziert jährlich gesamt", value=format_german(an_ag_finanziert_jaehrlich_gesamt)), unsafe_allow_html=True)
col4.markdown(custom_metric_html.format(label="Kapital bei Ablauf", value=format_german(kapital_bei_ablauf_gesamt)), unsafe_allow_html=True)
#Row A2
col1, col2, col3, col4 = st.columns(4)
#col1.metric("DEBUG",format_german(debug))
col4.markdown(custom_metric_html.format(label="davon AN", value=format_german(davon_an_gesamt)), unsafe_allow_html=True)

# Display the DataFrame as a table in Streamlit
df = df.round(2)
st.dataframe(df)

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
net_working_capital_2_change = safe_division(net_working_capital_2,net_working_capital_1)-1
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
        change=to_percentage(net_working_capital_2_change),
        change_color=get_change_color(net_working_capital_2_change)),
        unsafe_allow_html=True)

if show_deckungsgrad_b:
    col5.markdown(custom_metric_html_with_change.format(
        label="Deckungsgrad B",
        value=to_percentage(deckungsgrad_b_2),
        change=to_percentage(deckungsgrad_b_2_change),
        change_color=get_change_color(deckungsgrad_b_2_change)),
        unsafe_allow_html=True)




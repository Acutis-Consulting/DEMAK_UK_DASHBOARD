import streamlit as st
import pandas as pd
import plost
import locale

locale.setlocale(locale.LC_ALL, 'deu_deu')

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def to_percentage(value):
    percentage = "{:,.2f}".format(value * 100).replace('.', ',')
    return f"{percentage}%"

def format_german(value):
    return str('{0:n}'.format(round(value))) + " €"


st.sidebar.header('test `version 2`')

st.sidebar.title('Simulationsparameter')

arbeitnehmer_anzahl = st.sidebar.number_input('Arbeitnehmeranzahl (AN)',min_value=0,value=100)
zins_zusage = (st.sidebar.number_input('Zins Zusage (%)',min_value=0.0,value=3.00)/100)
an_fin_jaehrlich_pro_an = st.sidebar.number_input('AN finanziert jährlich pro AN (€)',min_value=0.0,value=1200.0)
ag_fin_jaehrlich_pro_an = st.sidebar.number_input('AG finanziert jährlich pro AN (€)',min_value=0.0,value=360.0)
laufzeit = st.sidebar.number_input('Laufzeit Zusage (Jahre)',min_value=0,value=30)
darlehenszins = (st.sidebar.number_input('Darlehenszins (%)',min_value=0.0,value=7.50)/100)
psv_beitragssatz = (st.sidebar.number_input('PSV-Beitragssatz (%)',min_value=0.0,value=0.25)/100)
uk_verwaltung_jaehrlich_pro_an = st.sidebar.number_input('UK Verwaltung jährlich pro AN',min_value=0,value=89)
uk_verwaltung_einmalig_im_ersten_jahr = (st.sidebar.number_input('UK Verwaltung einmalig im ersten Jahr (%)',min_value=0.0,value=2.00)/100)
steuern_UK = (st.sidebar.number_input('Steuern UK (e.V.) (%)',min_value=0.0,value=15.83)/100)
steuer_ersparnis = (st.sidebar.number_input('Steuerersparnis (%)',min_value=0.0,value=30.00)/100)
p1_anlage_liq = (st.sidebar.number_input('Parameter 1 Anlage Liquidität (%)',min_value=0.0,value=0.0)/100) #how do I name this parameter correctly?
p2_anlage_liq = (st.sidebar.number_input('Parameter 2 Anlage Liquidität (%)',min_value=0.0,value=8.0)/100) #how do I name this parameter correctly?
p3_anlage_liq = (st.sidebar.number_input('Parameter 3 Anlage Liquidität (%)',min_value=0.0,value=6.0)/100) #how do I name this parameter correctly?

passiva_2 = 0

st.sidebar.title('Eröffnungsbilanz')
col3, col4 = st.sidebar.columns(2)
col3.subheader('Aktiva')
col4.subheader('Passiva')

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

#Balance sheet calculations
umlaufvermögen = vorraete+kurzfristige_forderungen+zahlungsmittel
gesamtkapital_aktiva = anlagevermoegen + umlaufvermögen
fremdkapital = fk_kurzfristig + fk_langfristig
eigenkapital = gesamtkapital_aktiva - fremdkapital
gesamtkapital_passiva = eigenkapital + fremdkapital

# Create Dataframe
df = pd.DataFrame()

an_finanziert_jaehrlich_gesamt = arbeitnehmer_anzahl * an_fin_jaehrlich_pro_an
ag_finanziert_jaehrlich_gesamt = arbeitnehmer_anzahl * ag_fin_jaehrlich_pro_an
an_ag_finanziert_jaehrlich_gesamt = an_finanziert_jaehrlich_gesamt+ag_finanziert_jaehrlich_gesamt
kapital_bei_ablauf = (pow((1+zins_zusage),laufzeit)-1)/zins_zusage*(1+zins_zusage)*an_ag_finanziert_jaehrlich_gesamt
davon_an = (kapital_bei_ablauf/an_ag_finanziert_jaehrlich_gesamt)*an_finanziert_jaehrlich_gesamt

#Initialize Columns:
df['Jahr'] = range(1, laufzeit + 3)

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
df['Anlage Liquidität 1'] = 0 #Q
df['Anlage Liquidität 2'] = 0 #R
df['Anlage Liquidität 3'] = 0 #S
df['Barwert Versorgung'] = 0 #T


# Main loop
for i in range(laufzeit+2):
    if i == 0:
        df.loc[i, 'Zulässige Dotierung'] = (kapital_bei_ablauf/10*0.25)
        df.loc[i,'Tatsächliches Kassenvermögen'] =df.loc[i, 'Zulässige Dotierung']
        df.loc[i, 'PSV Beitrag'] = (davon_an/10)*0.25*20*psv_beitragssatz #M
        df.loc[i, 'Kosten UK-Verwaltung'] = (kapital_bei_ablauf*uk_verwaltung_einmalig_im_ersten_jahr)+(arbeitnehmer_anzahl*uk_verwaltung_jaehrlich_pro_an)

        pass  # replace with your actual calculations

    #elif i < 4:
    #df.loc[i, 'PSV Beitrag'] = (davon_an/10)*0.25*20*psv_beitragssatz
    #pass  # replace with your actual calculations

    elif i == (laufzeit):
        df.loc[i, 'Zulässiges Kassenvemögen'] = 0
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = 0
        #df.loc[i, 'Zulässige Dotierung'] = 0
        pass  # replace with your actual calculations

    #elif i == (laufzeit+1):
    #df.loc[i, 'Zulässiges Kassenvemögen'] = 0
    #df.loc[i, 'Höchstzulässiges Kassenvermögen'] = 0
    #df['Darlehenszinsen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) * darlehenszins #F ###Check
    #df.loc[i, 'Zinsanteil Überdotierung'] = df.loc[i, 'Darlehenszinsen']
    #df.loc[i, 'Zulässige Dotierung'] = 0
    #pass  # replace with your actual calculations

    else:
        # calculations for subsequent years

        df['Zulässiges Kassenvemögen'] = (kapital_bei_ablauf / 10) * 0.25 * 8 #B
        df['Höchstzulässiges Kassenvermögen'] = df['Zulässiges Kassenvemögen']*1.25 #C
        df.loc[df['Überdotierung'] > 0, 'Zinsanteil Überdotierung'] = (df['Überdotierung'] / df['Tatsächliches Kassenvermögen']) * df['Darlehenszinsen'] #G

        df['Darlehenszinsen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) * darlehenszins #F ###Check
        df.loc[df['Überdotierung'] > 0, 'Steuern UK (e.V.)'] = (df['Zinsanteil Überdotierung']*steuern_UK) #H
        #I ####ANPASSEN
        if (df.loc[i-1, 'Tatsächliches Kassenvermögen']+df.loc[i, 'Darlehenszinsen']+(kapital_bei_ablauf/10)*0.25) <= df.loc[i, 'Zulässiges Kassenvemögen']:
            df.loc[i,'Zulässige Dotierung'] = (kapital_bei_ablauf/10)*0.25
        elif ((df.loc[i-1, 'Tatsächliches Kassenvermögen']+df.loc[i, 'Darlehenszinsen']+(kapital_bei_ablauf/10)*0.25) > df.loc[i, 'Zulässiges Kassenvemögen']):
            if (df.loc[i, 'Zulässiges Kassenvemögen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Darlehenszinsen'])>0:
                df.loc[i,'Zulässige Dotierung'] = df.loc[i, 'Zulässiges Kassenvemögen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Darlehenszinsen']
            else:
                df.loc[i,'Zulässige Dotierung'] = 0
            #df.loc[i,'Zulässige Dotierung'] = df.loc[i, 'Zulässiges Kassenvemögen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Darlehenszinsen']
        else:
            df.loc[i,'Zulässige Dotierung'] = 0

        df['Darlehensänderung'] = df['Zulässige Dotierung'] + df['Darlehenszinsen'] - df['Steuern UK (e.V.)'].shift(fill_value=0) #J ###Check
        #df['Tatsächliches Kassenvermögen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) + df['Darlehensänderung'] - df['Versorgung fällig'] #K ###Check
        df.loc[i,'Tatsächliches Kassenvermögen'] = df.loc[i-1,'Tatsächliches Kassenvermögen'] + df.loc[i,'Darlehensänderung'] - df.loc[i,'Versorgung fällig'] #K
        df['Überdotierung'] = df['Tatsächliches Kassenvermögen'] - df['Höchstzulässiges Kassenvermögen'] #E
        #tatsaechliches_kassenvermoegen_backup = df['Tatsächliches Kassenvermögen']
        df.loc[i, 'Kosten UK-Verwaltung'] = arbeitnehmer_anzahl*uk_verwaltung_jaehrlich_pro_an #L

        if i > 2:
            df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf/10)*0.25*20*psv_beitragssatz
        else:
            df.loc[i, 'PSV Beitrag'] = (davon_an/10)*0.25*20*psv_beitragssatz  #M ####ANPASSEN

        #df['PSV Beitrag'] = (kapital_bei_ablauf/10)*0.25*20*psv_beitragssatz

        df['EU + SV Ersparnis'] = an_finanziert_jaehrlich_gesamt*1.2 #N
        df['Steuerersparnis'] = (df['EU + SV Ersparnis']-df['PSV Beitrag']-df[ 'Kosten UK-Verwaltung']-df['Darlehenszinsen']-df['Zulässige Dotierung'])*steuer_ersparnis*-1 #O
        df['Liquiditätsänderung'] = df['EU + SV Ersparnis']+df['Steuerersparnis']-df['PSV Beitrag']-df['Kosten UK-Verwaltung']-df['Steuern UK (e.V.)'].shift(fill_value=0) #P #Check if we have to make a different case for row 1
        df['Anlage Liquidität 1'] = df['Anlage Liquidität 1'].shift(fill_value=0)*(1+p1_anlage_liq)+df['Liquiditätsänderung'] #Q
        df['Anlage Liquidität 2'] = df['Anlage Liquidität 2'].shift(fill_value=0)*(1+p2_anlage_liq)+df['Anlage Liquidität 1'] #R

csv = df.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
)
################################
st.sidebar.subheader('Heat map parameter')
time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max'))

st.sidebar.subheader('Donut chart parameter')
donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown('''
---
Created with ❤️ by [Data Professor](https://youtube.com/dataprofessor/).
''')


# Row A1
st.markdown('### Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("AN finanziert jährlich gesamt",format_german(an_finanziert_jaehrlich_gesamt))
col2.metric("AG finanziert jährlich gesamt",format_german(ag_finanziert_jaehrlich_gesamt))
col3.metric("AN + AG finanziert jährlich gesamt",format_german(an_ag_finanziert_jaehrlich_gesamt))
col4.metric("Kapital bei Ablauf",format_german(kapital_bei_ablauf))
#col5.metric("Humidity", str(zins_zusage)+"%", "4%")

#Row A2
col1, col2, col3, col4 = st.columns(4)
#col1.metric("Metric 1", "Value 1", "Delta 1")
#col2.metric("Metric 2", "Value 2", "Delta 2")
#col3.metric("Metric 3", "Value 3", "Delta 3")
col4.metric("davon AN",str('{0:n}'.format(round(davon_an))) + " €")

# Display the DataFrame as a table in Streamlit
#st.table(df)
#st.dataframe(df.style.hide(axis="index"))
st.dataframe(df)


#Header
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
    formatted = locale.format_string("%d", anlagevermoegen, grouping=True)
    st.subheader(f"{formatted} €")
    formatted = locale.format_string("%d", umlaufvermögen, grouping=True)
    st.subheader(f"{formatted} €")
    formatted = locale.format_string("%d", vorraete, grouping=True)
    st.subheader(f"{formatted} €")
    formatted = locale.format_string("%d", kurzfristige_forderungen, grouping=True)
    st.subheader(f"{formatted} €")
    formatted = locale.format_string("%d", zahlungsmittel, grouping=True)
    st.subheader(f"{formatted} €")
with passiva_label:
    st.subheader("1 Eigenkapital")
    st.subheader("2 Fremdkapital")
    st.subheader("2.1 kurzfristig (FK kurzfr.)")
    st.subheader("2.2 langfristig (FK langfr.)")
with passiva_value:
    formatted = locale.format_string("%d", eigenkapital, grouping=True)
    st.subheader(f"{formatted} €")
    formatted = locale.format_string("%d", fremdkapital, grouping=True)
    st.subheader(f"{formatted} €")
    formatted = locale.format_string("%d", fk_kurzfristig, grouping=True)
    st.subheader(f"{formatted} €")
    formatted = locale.format_string("%d", fk_langfristig, grouping=True)
    st.subheader(f"{formatted} €")

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

# Create two columns for balance sheet
gk_aktiva_label, gk_aktiva_value, gk_passiva_label, gk_passiva_value = st.columns(4)
with gk_aktiva_label:
    st.subheader("Gesamtkapital Aktiva")
with gk_aktiva_value:
    formatted = locale.format_string("%d", gesamtkapital_aktiva, grouping=True)
    st.subheader(f"{formatted} €")
with gk_passiva_label:
    st.subheader("Gesamtkapital Passiva")
with gk_passiva_value:
    formatted = locale.format_string("%d", gesamtkapital_passiva, grouping=True)
    st.subheader(f"{formatted} €")

### avoid dividing by 0 denominator
def safe_division(numerator, denominator):
    if denominator == 0:
        return 0 # Or whatever value makes sense in this context
    else:
        return numerator / denominator

#Finanzwirtschaftliche Bilanzkennzahlen
eigenkapital_quote_1 = safe_division(eigenkapital,gesamtkapital_passiva)
anspannungsgrad_1 = safe_division(fremdkapital,gesamtkapital_passiva)
statischer_verschuldungsgrad_1 = safe_division(fremdkapital,eigenkapital)
intensitaet_langfristiges_kapital_1 = safe_division((eigenkapital+fk_langfristig),gesamtkapital_passiva)
liquiditaet_1_grades_1 = safe_division(zahlungsmittel,fk_kurzfristig)
liquiditaet_2_grades_1 = safe_division((zahlungsmittel+kurzfristige_forderungen),fk_kurzfristig)
liquiditaet_3_grades_1 = safe_division((zahlungsmittel+kurzfristige_forderungen+vorraete),fk_kurzfristig)
net_working_capital = umlaufvermögen-fk_kurzfristig
deckungsgrad_a_1 = safe_division(eigenkapital,anlagevermoegen)
deckungsgrad_b_1 = safe_division((eigenkapital+fk_langfristig),anlagevermoegen)


st.title("Finanzwirtschaftliche Bilanzkennzahlen")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Eigenkapitalquote", to_percentage(eigenkapital_quote_1))
col1.metric("Liquidität 2. Grades", to_percentage(liquiditaet_2_grades_1))
col2.metric("Anspannungsgrad", to_percentage(anspannungsgrad_1))
col2.metric("Liquidität 3. Grades", to_percentage(liquiditaet_3_grades_1))
col3.metric("Statischer Verschuldungsgrad", to_percentage(statischer_verschuldungsgrad_1))
col3.metric("Net Working Capital", format_german(net_working_capital))
col4.metric("Intensität langfristigen Kapitals", to_percentage(intensitaet_langfristiges_kapital_1))
col4.metric("Deckungsgrad A", to_percentage(deckungsgrad_a_1))
col5.metric("Liquidität 1. Grades", to_percentage(liquiditaet_1_grades_1))
col5.metric("Deckungsgrad B", to_percentage(deckungsgrad_b_1))
#col5.metric("debug", format_german(tatsaechliches_kassenvermoegen_backup))


###Markdowns
st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    padding: 5% 5% 5% 10%;
    border-radius: 15px;
    border-left: 0.5rem solid #9AD8E1 !important;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: black;
}
</style>
"""
            , unsafe_allow_html=True)


import streamlit as st
import pandas as pd
from PIL import Image
import plost
import json
import numpy as np
import base64
import array


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Functions
def format_german(value):
    v1 = f'{value:,.2f} €'
    v2 = v1.replace(',','#')
    v3 = v2.replace('.','%')
    v4 = v3.replace('#','.')
    v5 = v4.replace('%',',')
    return v5

st.sidebar.header('Vergleichsrechner Einmaleinlage `version 1`')

uploaded_file = st.sidebar.file_uploader("Parameter Hochladen", type=["json"])
if uploaded_file:
    # Reading the uploaded JSON file
    uploaded_data = json.load(uploaded_file)

# Eingabe Fondspolice
st.sidebar.markdown('Fondspolice')
if uploaded_file:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        einmalbeitrag_police = st.number_input('Einmalbeitrag',min_value=0,value=uploaded_data.get('einmalbeitrag_police'))
        rendite_mischfonds_police = (st.number_input('Rendite Mischfonds(%)',min_value=0.0,value=uploaded_data.get('rendite_mischfonds_police'))/100)
        rendite_rentenfonds_police = (st.number_input('Rendite Rentenfonds(%)',min_value=0.0,value=uploaded_data.get('rendite_rentenfonds_police'))/100)
        rendite_aktienfonds_police = (st.number_input('Rendite Aktienfonds(%)',min_value=0.0,value=uploaded_data.get('rendite_aktienfonds_police'))/100)
    with col2:
        teilfreistellung_police = (st.number_input('Teilfreistellung(%)',min_value=0.0,value=uploaded_data.get('teilfreistellung_police'))/100)
        effektivkosten_police = (st.number_input('Effektivkosten pro Jahr(%)',min_value=0.0,value=uploaded_data.get('effektivkosten_police'))/100)
        steuersatz_police = (st.number_input('Persönl. Steuersatz bei Auszahlung(%)',min_value=0.0,value=uploaded_data.get('steuersatz_police'))/100)


else:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        einmalbeitrag_police = st.number_input('Einmalbeitrag',min_value=0,value=0)
        rendite_mischfonds_police = (st.number_input('Rendite Mischfonds(%)',min_value=0.0,value=8.0)/100)
        rendite_rentenfonds_police = (st.number_input('Rendite Rentenfonds(%)',min_value=0.0,value=8.0)/100)
        rendite_aktienfonds_police = (st.number_input('Rendite Aktienfonds(%)',min_value=0.0,value=8.0)/100)
    with col2:
        teilfreistellung_police = (st.number_input('Teilfreistellung(%)',min_value=0.0,value=15.00)/100)
        effektivkosten_police = (st.number_input('Effektivkosten pro Jahr(%)',min_value=0.0,value=1.00)/100)
        steuersatz_police = (st.number_input('Persönl. Steuersatz bei Auszahlung(%)',min_value=0.0,value=42.0)/100)


# Eingabe Fondssparplan
st.sidebar.markdown('Fondssparplan')
if uploaded_file:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        einmalbeitrag_sparplan = st.number_input('Einmalbeitrag ',min_value=0,value=uploaded_data.get('einmalbeitrag_sparplan'))
        rendite_aktienfonds_sparplan = (st.number_input('Rendite Aktienfonds(%) ',min_value=0.0,value=uploaded_data.get('rendite_aktienfonds_sparplan'))/100)
        rendite_mischfonds_sparplan = (st.number_input('Rendite Mischfonds(%) ',min_value=0.0,value=uploaded_data.get('rendite_mischfonds_sparplan'))/100)
        rendite_rentenfonds_sparplan = (st.number_input('Rendite Rentenfonds(%) ',min_value=0.0,value=uploaded_data.get('rendite_rentenfonds_sparplan'))/100)
        freistellungsauftrag_sparplan = st.number_input('Freistellungsauftrag ',min_value=0,value=uploaded_data.get('freistellungsauftrag_sparplan'))
    with col2:
        teilfreistellung_aktienfonds_sparplan = (st.number_input('Teilfreistellung Aktienfonds(%) ',min_value=0.0,value=uploaded_data.get('teilfreistellung_aktienfonds_sparplan'))/100)
        teilfreistellung_mischfonds_sparplan = (st.number_input('Teilfreistellung Mischfonds(%)',min_value=0.0,value=uploaded_data.get('teilfreistellung_mischfonds_sparplan'))/100)
        teilfreistellung_rentenfonds_sparplan = (st.number_input('Teilfreistellung Rentenfonds(%) ',min_value=0.0,value=uploaded_data.get('teilfreistellung_rentenfonds_sparplan'))/100)
        basiszins_sparplan = (st.number_input('Basiszins(%) ',min_value=0.0,value=uploaded_data.get('basiszins_sparplan'))/100)

        effektivkosten_sparplan = (st.number_input('Effektivkosten pro Jahr(%) ',min_value=0.0,value=uploaded_data.get('effektivkosten_sparplan'))/100)
        ausgabeaufschlag_sparplan = (st.number_input('Ausgabeaufschlag auf Wiederanlage(%) ',min_value=0.0,value=uploaded_data.get('ausgabeaufschlag_sparplan'))/100)
        steuerlast_sparplan = (st.number_input('Steuerlast(%) ',min_value=0.0,value=uploaded_data.get('steuerlast_sparplan'))/100)
        steuerlast_auszahlung_sparplan = (st.number_input('Steuerlast bei Auszahlung(%) ',min_value=0.0,value=uploaded_data.get('steuerlast_auszahlung_sparplan'))/100)
else:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        einmalbeitrag_sparplan = st.number_input('Einmalbeitrag ',min_value=0,value=0)
        rendite_aktienfonds_sparplan = (st.number_input('Rendite Aktienfonds(%) ',min_value=0.0,value=0.0)/100)
        rendite_mischfonds_sparplan = (st.number_input('Rendite Mischfonds(%) ',min_value=0.0,value=0.0)/100)
        rendite_rentenfonds_sparplan = (st.number_input('Rendite Rentenfonds(%) ',min_value=0.0,value=0.0)/100)
        freistellungsauftrag_sparplan = st.number_input('Freistellungsauftrag ',min_value=0,value=0)
    with col2:
        teilfreistellung_aktienfonds_sparplan = (st.number_input('Teilfreistellung Aktienfonds(%) ',min_value=0.0,value=0.0)/100)
        teilfreistellung_mischfonds_sparplan = (st.number_input('Teilfreistellung Mischfonds(%) ',min_value=0.0,value=0.0)/100)
        teilfreistellung_rentenfonds_sparplan = (st.number_input('Teilfreistellung Rentenfonds(%) ',min_value=0.0,value=0.0)/100)
        basiszins_sparplan = (st.number_input('Basiszins(%) ',min_value=0.0,value=0.0)/100)

        effektivkosten_sparplan = (st.number_input('Effektivkosten pro Jahr(%) ',min_value=0.0,value=0.0)/100)
        ausgabeaufschlag_sparplan = (st.number_input('Ausgabeaufschlag auf Wiederanlage(%) ',min_value=0.0,value=0.0)/100)
        steuerlast_sparplan = (st.number_input('Steuerlast(%) ',min_value=0.0,value=0.0)/100)
        steuerlast_auszahlung_sparplan = (st.number_input('Steuerlast bei Auszahlung(%) ',min_value=0.0,value=0.0)/100)



st.sidebar.subheader('Weitere Parameter')
if uploaded_file:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        laufzeit = st.number_input('Laufzeit',min_value=0,value=uploaded_data.get('laufzeit'))-1
        anzahl_umschichtungen = st.number_input('Anzahl der Umschichtungen',min_value=0,value=uploaded_data.get('anzahl_umschichtungen'))
        anteil_umschichtung =  (st.number_input('Anteil Umschichtung(%)',min_value=0.0,value=uploaded_data.get('anteil_umschichtung'))/100)
else:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        laufzeit = st.number_input('Laufzeit ',min_value=0,value=1)-1
        anzahl_umschichtungen = st.number_input('Anzahl der Umschichtungen ',min_value=0,value=0)
        anteil_umschichtung = (st.number_input('Anteil Umschichtung(%)',min_value=0.0,value=0.0)/100)



#Umschichtungen police
def create_rollover_dataframe_police(laufzeit, anzahl_umschichtungen):
    # Create a dataframe with "years" number of rows
    df_police = pd.DataFrame({'Jahr': range(0, laufzeit+1)})

    # Calculate the positions for rollovers
    sequence = np.linspace(1, laufzeit, anzahl_umschichtungen + 2, dtype=int)[1:-1]
    positions = np.append(sequence, laufzeit)
    #positions = [19,29,laufzeit] #TEST

    # Initialize the rollover column with zeros
    df_police['UmschichtungJN'] = 0

    # Set rollovers at calculated positions
    df_police.loc[positions, 'UmschichtungJN'] = 1

    return df_police

def create_rollover_dataframe_depot(laufzeit, anzahl_umschichtungen):
    # Create a dataframe with "years" number of rows
    df_depot = pd.DataFrame({'Jahr': range(0, laufzeit+1)})

    # Calculate the positions for rollovers
    sequence = np.linspace(1, laufzeit, anzahl_umschichtungen + 2, dtype=int)[1:-1]
    positions = np.append(sequence, laufzeit)
    positions = [19,29,laufzeit] #TEST

    # Initialize the rollover column with zeros
    df_depot['UmschichtungJN'] = 0

    # Set rollovers at calculated positions
    df_depot.loc[positions, 'UmschichtungJN'] = 1

    return df_depot


#POLICE TABELLE
df_police = create_rollover_dataframe_police(laufzeit, anzahl_umschichtungen)


#df_police['Jahr'] = range(1, laufzeit +1)
df_police['Jahresbeginn'] = 0
df_police['Nach Beitragskosten und Abschlusskosten'] = 0
df_police['Rendite'] = 0
df_police['Wertsteigerung'] = 0
df_police['Jahresende'] = 0
df_police['Kosten Fondsguthaben'] = 0
df_police['Jahresende nach Kosten'] = 0
df_police['Einzahlung'] = 0
df_police['Umschichtung'] = 0
df_police['Umschichten oder Auszahlen'] = 0
df_police['Steuerlast'] = 0

for i in range (laufzeit+1):
    if i == 0:
        df_police.loc[i, 'Jahr'] = i+1 #A
        df_police.loc[i, 'Jahresbeginn'] = einmalbeitrag_police #B
        df_police.loc[i, 'Nach Beitragskosten und Abschlusskosten'] = df_police.loc[i,'Jahresbeginn'] #DELETE? #D
        df_police.loc[i, 'Rendite'] = rendite_aktienfonds_police #E
        df_police.loc[i, 'Wertsteigerung'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']*df_police.loc[i,'Rendite'] #F
        df_police.loc[i, 'Jahresende'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']+df_police.loc[i,'Wertsteigerung'] #G
        df_police.loc[i, 'Kosten Fondsguthaben'] = df_police.loc[i,'Jahresende']*effektivkosten_police #J
        df_police.loc[i, 'Jahresende nach Kosten'] = df_police.loc[i,'Jahresende']-df_police.loc[i,'Kosten Fondsguthaben'] #K
        df_police.loc[i, 'Einzahlung'] = einmalbeitrag_police #L
        df_police.loc[i, 'Umschichtung'] = df_police.loc[i, 'UmschichtungJN']*anteil_umschichtung #M %-Zahl einfügen
        df_police.loc[i, 'Umschichten oder Auszahlen'] = df_police.loc[i, 'Jahresende nach Kosten']*df_police.loc[i, 'Umschichtung'] #N

    else:
        df_police.loc[i, 'Jahr'] = i+1 #A
        df_police.loc[i,'Jahresbeginn'] = df_police.loc[i-1, 'Jahresende nach Kosten'] #B
        df_police.loc[i,'Nach Beitragskosten und Abschlusskosten'] = df_police.loc[i,'Jahresbeginn'] #DELETE? #D
        df_police.loc[i, 'Rendite'] = rendite_aktienfonds_police #E
        df_police.loc[i, 'Wertsteigerung'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']*df_police.loc[i,'Rendite'] #F
        df_police.loc[i, 'Jahresende'] = df_police.loc[i,'Nach Beitragskosten und Abschlusskosten']+df_police.loc[i,'Wertsteigerung'] #G
        df_police.loc[i, 'Kosten Fondsguthaben'] = df_police.loc[i,'Jahresende']*effektivkosten_police #J
        df_police.loc[i, 'Jahresende nach Kosten'] = df_police.loc[i,'Jahresende']-df_police.loc[i,'Kosten Fondsguthaben'] #K
        df_police.loc[i, 'Einzahlung'] = 0 #L
        df_police.loc[i, 'Umschichtung'] = df_police.loc[i, 'UmschichtungJN']*anteil_umschichtung #M %-Zahl einfügen
        df_police.loc[i, 'Umschichten oder Auszahlen'] = df_police.loc[i, 'Jahresende nach Kosten']*df_police.loc[i, 'Umschichtung'] #N

#DEPOT TABELLE
#df_depot = pd.DataFrame()
df_depot = create_rollover_dataframe_depot(laufzeit, anzahl_umschichtungen)

#df_depot['Jahr'] = range(1, laufzeit+1)
df_depot['Jahresbeginn'] = 0
df_depot['Nach Orderprov. und Ausgabeaufschl.'] = 0
df_depot['Rendite'] = 0
df_depot['Wertsteigerung'] = 0
df_depot['Wertsteigerunglaufend'] = 0
df_depot['Jahresende'] = 0
df_depot['Kosten auf Fondsguthaben'] = 0
df_depot['Jahresende nach Kosten'] = 0
df_depot['Basisertrag'] = 0
df_depot['Vorabpauschale'] = 0
df_depot['Vorabpauschalelaufend'] = 0
df_depot['Teilfreistellung'] = 0
df_depot['zu besteuern'] = 0
df_depot['Freistellungsauftrag'] = 0
df_depot['Freistellung übrig'] = 0
df_depot['danach zu besteuern'] = 0
df_depot['Steuerlast'] = 0
df_depot['Einzahlung'] = 0
df_depot['Umschichtung'] = 0
df_depot['Umschichten'] = 0
df_depot['Erträgelaufend'] = 0
df_depot['Erträge'] = 0
df_depot['minus Vorabpauschale'] = 0
df_depot['Teilfreistellung '] = 0
df_depot['zu besteuern '] = 0
df_depot['nach Freistellungsauftrag'] = 0
df_depot['Steuerlast '] = 0
df_depot['Kapital abzüglich Steuer'] = 0

for i in range (laufzeit+1):
    if i == 0:
        df_depot.loc[i, 'Jahr'] = i+1 #A
        df_depot.loc[i, 'Jahresbeginn'] = einmalbeitrag_sparplan #B
        df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'] = df_depot.loc[i, 'Jahresbeginn'] #E
        df_depot.loc[i, 'Rendite'] = rendite_aktienfonds_sparplan #F
        df_depot.loc[i, 'Wertsteigerung'] = df_depot.loc[i, 'Jahresbeginn'] * rendite_aktienfonds_sparplan #G
        df_depot.loc[i, 'Jahresende'] = df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'] + df_depot.loc[i, 'Wertsteigerung'] #H
        df_depot.loc[i, 'Kosten auf Fondsguthaben'] = df_depot.loc[i, 'Jahresende'] * effektivkosten_sparplan #K
        df_depot.loc[i, 'Basisertrag'] = df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']*0.7*basiszins_sparplan #M
        if(df_depot.loc[i, 'Jahresende']-df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) <= df_depot.loc[i, 'Basisertrag'] and (df_depot.loc[i, 'Jahresende']-df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) >= 0:
            df_depot.loc[i, 'Vorabpauschale'] = 0  #N
        elif(df_depot.loc[i, 'Jahresende']-df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'])>=df_depot.loc[i, 'Basisertrag']:
            df_depot.loc[i, 'Vorabpauschale'] = df_depot.loc[i, 'Basisertrag'] #N
        else:
            df_depot.loc[i, 'Vorabpauschale'] = 0 #N
        df_depot.loc[i, 'Vorabpauschalelaufend'] = df_depot.loc[i, 'Vorabpauschale']
        df_depot.loc[i, 'Teilfreistellung'] = df_depot.loc[i, 'Vorabpauschale']*teilfreistellung_aktienfonds_sparplan #O
        df_depot.loc[i, 'zu besteuern'] = df_depot.loc[i, 'Vorabpauschale'] - df_depot.loc[i, 'Teilfreistellung'] #P
        df_depot.loc[i, 'Freistellungsauftrag'] = freistellungsauftrag_sparplan #R

        if df_depot.loc[i, 'zu besteuern'] >= df_depot.loc[i, 'Freistellungsauftrag']:
            df_depot.loc[i, 'Freistellung übrig'] = 0
        else:
            df_depot.loc[i, 'Freistellung übrig'] = df_depot.loc[i, 'Freistellungsauftrag'] - df_depot.loc[i, 'zu besteuern'] #S

        if df_depot.loc[i, 'Freistellungsauftrag'] >= df_depot.loc[i, 'zu besteuern']:
            df_depot.loc[i, 'danach zu besteuern'] = 0 #T
        else:
            df_depot.loc[i, 'danach zu besteuern'] = df_depot.loc[i, 'zu besteuern'] - df_depot.loc[i, 'Freistellungsauftrag'] #T

        df_depot.loc[i, 'Steuerlast'] = df_depot.loc[i, 'danach zu besteuern']*steuerlast_sparplan #U
        df_depot.loc[i, 'Jahresende nach Kosten'] = df_depot.loc[i, 'Jahresende'] - df_depot.loc[i, 'Kosten auf Fondsguthaben'] - df_depot.loc[i, 'Steuerlast']  #L
        df_depot.loc[i, 'Einzahlung'] = einmalbeitrag_sparplan #V
        df_depot.loc[i, 'Umschichtung'] = df_depot.loc[i, 'UmschichtungJN']*anteil_umschichtung #W %-Zahl einfügen
        df_depot.loc[i, 'Umschichten'] = df_depot.loc[i, 'Jahresende nach Kosten']*df_depot.loc[i, 'Umschichtung'] #X
        df_depot.loc[i, 'Erträgelaufend'] = df_depot.loc[i, 'Wertsteigerung'] #NICHT ANZEIGEN
        df_depot.loc[i, 'Erträge'] = df_depot.loc[i, 'Erträgelaufend']*df_depot.loc[i, 'UmschichtungJN'] #Z
        df_depot.loc[i, 'minus Vorabpauschale'] = (df_depot.loc[i, 'Erträgelaufend'] - df_depot.loc[i, 'Vorabpauschalelaufend'])*df_depot.loc[i, 'UmschichtungJN'] #AA
        df_depot.loc[i, 'Teilfreistellung '] = df_depot.loc[i, 'minus Vorabpauschale']*teilfreistellung_aktienfonds_sparplan #AB
        df_depot.loc[i, 'zu besteuern '] = df_depot.loc[i, 'minus Vorabpauschale'] - df_depot.loc[i, 'Teilfreistellung '] #AC

        if df_depot.loc[i, 'Freistellung übrig'] > df_depot.loc[i, 'zu besteuern ']:
            df_depot.loc[i, 'nach Freistellungsauftrag'] = 0 #AD
        else:
            df_depot.loc[i, 'nach Freistellungsauftrag'] = df_depot.loc[i, 'zu besteuern '] - df_depot.loc[i, 'Freistellung übrig'] #AD

        df_depot.loc[i, 'Steuerlast '] = df_depot.loc[i, 'nach Freistellungsauftrag']*steuerlast_sparplan #AE
        df_depot.loc[i, 'Kapital abzüglich Steuer'] = df_depot.loc[i, 'Umschichten'] - df_depot.loc[i, 'Steuerlast '] #AF

    else:
        df_depot.loc[i, 'Jahr'] = i+1 #A
        df_depot.loc[i,'Jahresbeginn'] = df_depot.loc[i-1, 'Jahresende nach Kosten'] - df_depot.loc[i-1, 'Steuerlast '] #B
        df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.'] = df_depot.loc[i, 'Jahresbeginn'] #E
        df_depot.loc[i, 'Rendite'] = rendite_aktienfonds_sparplan #F
        df_depot.loc[i, 'Wertsteigerung'] = df_depot.loc[i, 'Jahresbeginn'] * rendite_aktienfonds_sparplan #G
        df_depot.loc[i, 'Jahresende'] = df_depot.loc[i, 'Jahresbeginn'] + df_depot.loc[i, 'Wertsteigerung'] #H
        df_depot.loc[i, 'Kosten auf Fondsguthaben'] = df_depot.loc[i, 'Jahresende'] * effektivkosten_sparplan #K
        df_depot.loc[i, 'Basisertrag'] = df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']*0.7*basiszins_sparplan #M

        if(df_depot.loc[i, 'Jahresende']-df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) <= df_depot.loc[i, 'Basisertrag'] and (df_depot.loc[i, 'Jahresende']-df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) >= 0:
            df_depot.loc[i, 'Vorabpauschale'] = 0  #N
        elif(df_depot.loc[i, 'Jahresende']-df_depot.loc[i, 'Nach Orderprov. und Ausgabeaufschl.']) >= df_depot.loc[i, 'Basisertrag']:
            df_depot.loc[i, 'Vorabpauschale'] = df_depot.loc[i, 'Basisertrag'] #N
        else:
            df_depot.loc[i, 'Vorabpauschale'] = 0 #N

        df_depot.loc[i, 'Vorabpauschalelaufend'] = df_depot.loc[i-1, 'Vorabpauschalelaufend'] + df_depot.loc[i, 'Vorabpauschale']
        df_depot.loc[i, 'Teilfreistellung'] = df_depot.loc[i, 'Vorabpauschale']*teilfreistellung_aktienfonds_sparplan #O ############
        df_depot.loc[i, 'zu besteuern'] = df_depot.loc[i, 'Vorabpauschale'] - df_depot.loc[i, 'Teilfreistellung'] #P
        df_depot.loc[i, 'Freistellungsauftrag'] = freistellungsauftrag_sparplan #R

        if df_depot.loc[i, 'zu besteuern'] >= df_depot.loc[i, 'Freistellungsauftrag']:
            df_depot.loc[i, 'Freistellung übrig'] = 0
        else:
            df_depot.loc[i, 'Freistellung übrig'] = df_depot.loc[i, 'Freistellungsauftrag'] - df_depot.loc[i, 'zu besteuern'] #S

        if df_depot.loc[i, 'Freistellungsauftrag'] >= df_depot.loc[i, 'zu besteuern']:
            df_depot.loc[i, 'danach zu besteuern'] = 0 #T
        else:
            df_depot.loc[i, 'danach zu besteuern'] = df_depot.loc[i, 'zu besteuern'] - df_depot.loc[i, 'Freistellungsauftrag'] #T

        df_depot.loc[i, 'Steuerlast'] = df_depot.loc[i, 'danach zu besteuern']*steuerlast_sparplan #U
        df_depot.loc[i, 'Jahresende nach Kosten'] = df_depot.loc[i, 'Jahresende'] - df_depot.loc[i, 'Kosten auf Fondsguthaben'] - df_depot.loc[i, 'Steuerlast']  #L
        df_depot.loc[i, 'Einzahlung'] = 0 #V
        df_depot.loc[i, 'Umschichtung'] = df_depot.loc[i, 'UmschichtungJN']*anteil_umschichtung #W %-Zahl einfügen
        df_depot.loc[i, 'Umschichten'] = df_depot.loc[i, 'Jahresende nach Kosten']*df_depot.loc[i, 'Umschichtung'] #X
        df_depot.loc[i, 'Erträgelaufend'] = df_depot.loc[i-1, 'Erträgelaufend'] + df_depot.loc[i, 'Wertsteigerung'] #NICHT ANZEIGEN
        df_depot.loc[i, 'Erträge'] = df_depot.loc[i, 'Erträgelaufend']*df_depot.loc[i, 'UmschichtungJN'] #Z
        df_depot.loc[i, 'minus Vorabpauschale'] = (df_depot.loc[i, 'Erträgelaufend'] - df_depot.loc[i, 'Vorabpauschalelaufend'])*df_depot.loc[i, 'UmschichtungJN'] #AA
        df_depot.loc[i, 'Teilfreistellung '] = df_depot.loc[i, 'minus Vorabpauschale']*teilfreistellung_aktienfonds_sparplan #AB
        df_depot.loc[i, 'zu besteuern '] = df_depot.loc[i, 'minus Vorabpauschale'] - df_depot.loc[i, 'Teilfreistellung '] #AC

        if df_depot.loc[i, 'Freistellung übrig'] > df_depot.loc[i, 'zu besteuern ']:
            df_depot.loc[i, 'nach Freistellungsauftrag'] = 0 #AD
        else:
            df_depot.loc[i, 'nach Freistellungsauftrag'] = df_depot.loc[i, 'zu besteuern '] - df_depot.loc[i, 'Freistellung übrig'] #AD

        df_depot.loc[i, 'Steuerlast '] = df_depot.loc[i, 'nach Freistellungsauftrag']*steuerlast_sparplan #AE
        df_depot.loc[i, 'Kapital abzüglich Steuer'] = df_depot.loc[i, 'Umschichten'] - df_depot.loc[i, 'Steuerlast '] #AF

# Display the DataFrame as a table in Streamlit
st.markdown('### Fondspolice')
df_police = df_police.round(2)
st.dataframe(df_police)

csv = df_police.to_csv(index=False)
st.download_button(
    label="Als CSV herunterladen",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
)


st.markdown('### Fondssparplan')
df_depot = df_depot.round(2)
st.dataframe(df_depot)

csv = df_depot.to_csv(index=False)
st.download_button(
    label="Als CSV herunterladen",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
)



# Row A1
st.title('Ergebnis')
col1, col2, col3 = st.columns(3)

fondspolice_rentenkapital = df_police.loc[i, 'Jahresende nach Kosten']
col1.metric("Fondspolice Rentenkapital",format_german(fondspolice_rentenkapital))

fondspolice_ertraege = fondspolice_rentenkapital - einmalbeitrag_police
fondspolice_teilfreistellung_result = fondspolice_ertraege * teilfreistellung_police
fondspolice_zu_besteuern_result = fondspolice_ertraege - fondspolice_teilfreistellung_result
fondspolice_hev_result = fondspolice_zu_besteuern_result/2
fondspolice_steuerlast_result = fondspolice_hev_result * steuersatz_police
fondspolice = fondspolice_rentenkapital - fondspolice_steuerlast_result
col1.metric("Fondspolice",format_german(fondspolice))
col1.metric("test12",format_german(1))











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

# Add a button to trigger the save
st.sidebar.title(' ')
if st.sidebar.button('Parameter Speichern'):
    # Creating a dictionary of parameters to save
    data_to_save = {
        ### Parameter Police
        'einmalbeitrag_police': einmalbeitrag_police,
        'rendite_mischfonds_police': rendite_mischfonds_police*100,
        'rendite_rentenfonds_police': rendite_rentenfonds_police*100,
        'rendite_aktienfonds_police': rendite_aktienfonds_police*100,
        'teilfreistellung_police': teilfreistellung_police*100,
        'effektivkosten_police': effektivkosten_police*100,
        'steuersatz_police': steuersatz_police*100,
    ### Parameter Sparplan
        'einmalbeitrag_sparplan': einmalbeitrag_sparplan,
        'rendite_aktienfonds_sparplan': rendite_aktienfonds_sparplan*100,
        'rendite_mischfonds_sparplan': rendite_mischfonds_sparplan*100,
        'rendite_rentenfonds_sparplan': rendite_rentenfonds_sparplan*100,
        'freistellungsauftrag_sparplan': freistellungsauftrag_sparplan*100,
        'teilfreistellung_aktienfonds_sparplan': teilfreistellung_aktienfonds_sparplan*100,
        'teilfreistellung_mischfonds_sparplan': teilfreistellung_mischfonds_sparplan*100,
        'teilfreistellung_rentenfonds_sparplan': teilfreistellung_rentenfonds_sparplan*100,
        'basiszins_sparplan': basiszins_sparplan*100,
        'effektivkosten_sparplan': effektivkosten_sparplan*100,
        'ausgabeaufschlag_sparplan': ausgabeaufschlag_sparplan*100,
        'steuerlast_sparplan': steuerlast_sparplan*100,
        'steuerlast_auszahlung_sparplan': steuerlast_auszahlung_sparplan*100,
        ### Weitere Parameter
        'laufzeit': laufzeit+1,
        'anzahl_umschichtungen': anzahl_umschichtungen,
        'anteil_umschichtung': anteil_umschichtung*100
    }

    # Convert dictionary to JSON string
    json_str = json.dumps(data_to_save, indent=4)

    # Convert the string to bytes
    b64 = base64.b64encode(json_str.encode()).decode()

    # Provide a link to download the JSON file
    href = f'<a href="data:file/json;base64,{b64}" download="parameters.json">Parameter Herunterladen</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)




















# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

st.markdown('### Test')
st.number_input('Enter a number')

# Row B
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

c1, c2 = st.columns((7,3))
with c1:
    st.markdown('### Heatmap')
    plost.time_hist(
        data=seattle_weather,
        date='date',
        x_unit='week',
        y_unit='day',
        color=time_hist_color,
        aggregate='median',
        legend=None,
        height=345,
        use_container_width=True)
with c2:
    st.markdown('### Donut chart')
    plost.donut_chart(
        data=stocks,
        theta=donut_theta,
        color='company',
        legend='bottom',
        use_container_width=True)

# Row C
st.markdown('### Line chart')
st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)



###Markdowns
st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    padding: 5% 5% 5% 10%;
    border-radius: 15px;
    border-left: 0.5rem solid #fdff00 !important;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
   overflow-wrap: break-word;
}

</style>
"""
            , unsafe_allow_html=True)
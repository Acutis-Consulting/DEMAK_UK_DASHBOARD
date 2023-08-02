import streamlit as st
import pandas as pd
import plost
import locale

locale.setlocale(locale.LC_ALL, 'deu_deu')

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('test `version 2`')

st.sidebar.subheader('Simulationsparameter')

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


#Darlehenszins:
#PSV-Beitragssatz:
#UK Verwaltung jährlich pro AN:
#UK Verwaltung einmalig im ersten Jahr:

# Create Dataframe
#df = pd.DataFrame(index=range(laufzeit))
df = pd.DataFrame()



an_finanziert_jaehrlich_gesamt = arbeitnehmer_anzahl * an_fin_jaehrlich_pro_an
ag_finanziert_jaehrlich_gesamt = arbeitnehmer_anzahl * ag_fin_jaehrlich_pro_an
an_ag_finanziert_jaehrlich_gesamt = an_finanziert_jaehrlich_gesamt+ag_finanziert_jaehrlich_gesamt
kapital_bei_ablauf = (pow((1+zins_zusage),laufzeit)-1)/zins_zusage*(1+zins_zusage)*an_ag_finanziert_jaehrlich_gesamt
davon_an = (kapital_bei_ablauf/an_ag_finanziert_jaehrlich_gesamt)*an_finanziert_jaehrlich_gesamt

#Initialize Columns:






# Calculate Dataframe columns
df['Jahr'] = range(1, laufzeit + 1)

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
for i in range(laufzeit):
    if i == 0:

        df.loc[i, 'Kosten UK-Verwaltung'] = (kapital_bei_ablauf*uk_verwaltung_einmalig_im_ersten_jahr)+(arbeitnehmer_anzahl*uk_verwaltung_jaehrlich_pro_an)
        #df.loc[i, 'Liquiditätsänderung'] = df['EU + SV Ersparnis']+df['Steuerersparnis']-df['PSV Beitrag']-df['Liquiditätsänderung']
        #df.loc[i, 'Anlage Liquidität'] = df['Liquiditätsänderung']
        pass  # replace with your actual calculations
    else:
        # calculations for subsequent years

        df['Zulässiges Kassenvemögen'] = (kapital_bei_ablauf / 10) * 0.25 * 8 #B
        df['Höchstzulässiges Kassenvermögen'] = df['Zulässiges Kassenvemögen']*1.25 #C
        df['Zulässige Dotierung'] = kapital_bei_ablauf/10*0.25 #D ####ANPASSEN
        df['Überdotierung'] = df['Tatsächliches Kassenvermögen'] - df['Höchstzulässiges Kassenvermögen'] #E
        df['Darlehenszinsen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) * darlehenszins #F
        df.loc[df['Überdotierung'] > 0, 'Zinsanteil Überdotierung'] = (df['Überdotierung'] / df['Tatsächliches Kassenvermögen']) * df['Darlehenszinsen'] #G
        df.loc[df['Überdotierung'] > 0, 'Steuern UK (e.V.)'] = (df['Zinsanteil Überdotierung']*steuern_UK) #H
        #I ####ANPASSEN
        df['Darlehensänderung'] = df['Zulässige Dotierung'] + df['Darlehenszinsen'] - df['Steuern UK (e.V.)'].shift(fill_value=0) #J
        df['Tatsächliches Kassenvermögen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) + df['Darlehensänderung'] - df['Versorgung fällig'] #K
        df.loc[i, 'Kosten UK-Verwaltung'] = arbeitnehmer_anzahl*uk_verwaltung_jaehrlich_pro_an #L
        df['PSV Beitrag'] = (davon_an/10)*0.25*20*psv_beitragssatz #M ####ANPASSEN
        df['EU + SV Ersparnis'] = an_finanziert_jaehrlich_gesamt*1.2 #N
        df['Steuerersparnis'] = (df['EU + SV Ersparnis']-df['PSV Beitrag']-df[ 'Kosten UK-Verwaltung']-df['Darlehenszinsen']-df['Zulässige Dotierung'])*steuer_ersparnis*-1 #O
        df['Liquiditätsänderung'] = df['EU + SV Ersparnis']+df['Steuerersparnis']-df['PSV Beitrag']-df['Kosten UK-Verwaltung']-df['Steuern UK (e.V.)'].shift(fill_value=0) #P #Check if we have to make a different case for row 1
        df['Anlage Liquidität 1'] = df['Anlage Liquidität 1'].shift(fill_value=0)*(1+p1_anlage_liq)+df['Liquiditätsänderung'] #Q
        df['Anlage Liquidität 2'] = df['Anlage Liquidität 2'].shift(fill_value=0)*(1+p2_anlage_liq)+df['Anlage Liquidität 1'] #R

#L
#M
#N
#O
#P
#Q
#R
#S
#T








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
col1.metric("AN finanziert jährlich gesamt",str('{0:n}'.format(an_finanziert_jaehrlich_gesamt)) + " €")
col2.metric("AG finanziert jährlich gesamt",str('{0:n}'.format(ag_finanziert_jaehrlich_gesamt)) + " €")
col3.metric("AN + AG finanziert jährlich gesamt",str('{0:n}'.format(an_ag_finanziert_jaehrlich_gesamt)) + " €")
col4.metric("Kapital bei Ablauf",str('{0:n}'.format(round(kapital_bei_ablauf))) + " €")
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
#st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)



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

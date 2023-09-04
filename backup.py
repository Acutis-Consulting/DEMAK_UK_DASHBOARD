col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Eigenkapitalquote", to_percentage(eigenkapital_quote_1))
col1.metric("Liquidität 2. Grades", to_percentage(liquiditaet_2_grades_1))
col2.metric("Anspannungsgrad", to_percentage(anspannungsgrad_1))
col2.metric("Liquidität 3. Grades", to_percentage(liquiditaet_3_grades_1))
col3.metric("Statischer Verschuldungsgrad", to_percentage(statischer_verschuldungsgrad_1))
col3.metric("Net Working Capital", format_german(net_working_capital_1))
col4.metric("Intensität langfristigen Kapitals", to_percentage(intensitaet_langfristiges_kapital_1))
col4.metric("Deckungsgrad A", to_percentage(deckungsgrad_a_1))
col5.metric("Liquidität 1. Grades", to_percentage(liquiditaet_1_grades_1))
col5.metric("Deckungsgrad B", to_percentage(deckungsgrad_b_1))
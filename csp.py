import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

import constraint
import math

st.set_page_config(layout="wide")

st.title('Vaccine Distribution Modelling')

st.write("Table 1. Vaccine names and types")
st.write(pd.DataFrame({
    'Name': ['Vac-A', 'Vac-B', 'Vac-C'],
    'Criteria': ['Age > 60', 'Age between 35 to 60', 'Age < 35']
}))

st.write("Table 2. Vaccination Centre Type")
st.write(pd.DataFrame({
    'Type': ['CR-1', 'CR-2', 'CR-3', 'CR-4', 'CR-5'],
    'Max Capacity': [200, 500, 1000, 2500, 4000],
    'Rental per Day': [100, 250, 500, 800, 1200]
}))

st.write("Table 3. State and Population")
st.write(pd.DataFrame({
    'Type': ['ST-1', 'ST-2', 'ST-3', 'ST-4', 'ST-5'],
    'Age < 35': [115900, 100450, 223400, 269300, 221100],
    'Age between 35 to 60': [434892, 378860, 643320, 859900, 450500],
    'Age > 60': [15000, 35234, 22318, 23893, 19284]
}))

st.write("Table 4. State and Number of Vaccination Centres")
st.write(pd.DataFrame({
    'Type': ['ST-1', 'ST-2', 'ST-3', 'ST-4', 'ST-5'],
    'CR-1': [20, 30, 22, 16, 19],
    'CR-2': [15, 16, 15, 16, 10],
    'CR-3': [10, 15, 11, 16, 20],
    'CR-4': [21, 10, 12, 15, 15],
    'CR-5': [5, 2, 3, 1, 1]
}))

st.write("Table 5. States and the Max Vaccination Capacity per Day")
st.write(pd.DataFrame({
    'Type': ['ST-1', 'ST-2', 'ST-3', 'ST-4', 'ST-5'],
    'Max Capacity': [5000, 10000, 7500, 8500, 9500]
}))

df1 = pd.DataFrame({
    'select_state': [1, 2, 3, 4, 5],

    'select_pop_a': [115900,100450,223400,269300,221100],
    'select_pop_b': [434890,378860,643320,859900,450500],
    'select_pop_c': [15000,35234,22318,23893,19284],

    'select_CR1': [20, 30, 22, 16, 19],
    'select_CR3': [10, 15, 11, 16, 20],
    'select_capacity': [5000,10000,7500,8500,9500]
    })

df2 = pd.DataFrame({
    'select_CR2': [15, 16, 10]
})

df3 = pd.DataFrame({
    'select_CR4': [21, 10, 12, 15],
    'select_CR5': [5, 2, 3, 1]
})

# Add a selectbox to the sidebar:
no_of_states = st.sidebar.selectbox(
    'Which state?',
    df1['select_state']
)

capacity = st.sidebar.selectbox(
    'What is the max capacity in the state?',
    df1['select_capacity']
)

pop_a = st.sidebar.selectbox(
    'How many people age less than 35?',
    df1['select_pop_a']
)
pop_b = st.sidebar.selectbox(
    'How many people age between 35 to 60?',
    df1['select_pop_b']
)
pop_c = st.sidebar.selectbox(
    'How many people age more than 60?',
    df1['select_pop_c']
)

cr1 = st.sidebar.selectbox(
    'How many available vaccination centres for CR-1?',
    df1['select_CR1']
)
cr2 = st.sidebar.selectbox(
    'How many available vaccination centres for CR-2?',
    df2['select_CR2']
)
cr3 = st.sidebar.selectbox(
    'How many available vaccination centres for CR-3?',
    df1['select_CR3']
)
cr4 = st.sidebar.selectbox(
    'How many available vaccination centres for CR-4?',
    df3['select_CR4']
)
cr5 = st.sidebar.selectbox(
    'How many available vaccination centres for CR-5?',
    df3['select_CR5']
)

population = pop_a + pop_b + pop_c
no_of_days = math.ceil(population/capacity)

problem = constraint.Problem()

problem.addVariable('c1', range(cr1+1))
problem.addVariable('c2', range(cr2+1))
problem.addVariable('c3', range(cr3+1))
problem.addVariable('c4', range(cr4+1))
problem.addVariable('c5', range(cr5+1))

def capacity_constraint(c1,c2,c3,c4,c5):
    cap = c1*200 + c2*500 + c3*1000 + c4*2500 + c5*4000
    if cap == capacity:
        return True

problem.addConstraint(capacity_constraint,['c1','c2','c3','c4','c5'])

solutions = problem.getSolutions()

min_rental=9999999
solution_found={}
for solution in solutions:
    rental = solution['c1']*100 + solution['c2']*250 + solution['c3']*500 + solution['c4']*800 + solution['c5']*1200
    if rental<min_rental:
        min_rental=rental
        solution_found=solution

new_title = '<sp style="font-family:sans-serif; color:Green; font-size: 42px;">Result</p>'
st.markdown(new_title, unsafe_allow_html=True)
'State ',no_of_states
'Minimum rental fee per day : RM ',min_rental
'Maximum total vaccines distributed per day : ',capacity
'Distribution of vaccine centers:'
'CR-1: ',solution_found['c1']
'CR-2: ',solution_found['c2']
'CR-3: ',solution_found['c3']
'CR-4: ',solution_found['c4']
'CR-5: ',solution_found['c5']
'Total number of Vac-A (age > 60) per day : ',math.ceil(pop_c/no_of_days)
'Total number of Vac-B (age between 35 to 60) per day : ',math.ceil(pop_b/no_of_days)
'Total number of Vac-C (age < 35) per day : ',math.ceil(pop_a/no_of_days)
'Estimated number of days for completion : ',no_of_days

df4 = pd.DataFrame({
    'Criteria': ['Age > 60', 'Age between 35 to 60', 'Age < 35'],
    'Population': [math.ceil(pop_c/no_of_days),math.ceil(pop_b/no_of_days),math.ceil(pop_a/no_of_days)]
})

bar = alt.Chart(df4).mark_bar().encode(
    x='Criteria',
    y='Population'
)

st.altair_chart(bar)
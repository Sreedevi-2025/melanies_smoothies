#Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
#Page title
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
"""
Choose the fruits you want in your custom smoothie!
"""
)
#Name box
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)
#Snowflake session
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
#Retrieve fruit options
my_dataframe = (
session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
.select(col("FRUIT_NAME"))
.to_pandas()
)
#Multi-select list
ingredients_list = st.multiselect(
'Choose up to 5 ingredients:',
my_dataframe["FRUIT_NAME"],
max_selections=5
)
if ingredients_list:
  ingredients_string = ''
  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    st.subheader(fruit_chosen + ' Nutrition Information')
    smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/" + fruit_chosen.lower()
    ) 
    if smoothiefroot_response.status_code == 200:
      st.dataframe(
      data=smoothiefroot_response.json(),
      use_container_width=True
      )
    else:
      st.write('Sorry, that fruit is not in our database.')
# Submit button
time_to_insert = st.button('Submit Order')
if time_to_insert:
  my_insert_stmt = """
  insert into smoothies.public.orders(ingredients, name_on_order)
  values ('""" + ingredients_string + """','""" + name_on_order + """')
  """
  session.sql(my_insert_stmt).collect()
  st.success(
  'Your Smoothie is ordered, ' + name_on_order + '!',
  icon='✅'
  )

 

import base64
import streamlit as st
from product_info import get_locations, get_rule_drivers, get_rules,set_locations,apply_rules,set_rule_drivers,get_selected_location,set_selected_location
st.set_page_config(layout="wide",page_icon="static/favicon.ico")
# Sample data

data = get_locations()
edited_data=data
logo_url = './static/apple-touch-icon.png'
st.sidebar.image(logo_url)
class WebPage:
    
    # Function to update data based on edits
    def process_change(self,item):
        edited_rows = st.session_state["edited_data"]["edited_rows"]
        product_data=get_locations()
        # print("edited_rows")
        for i in range(0,len(product_data)):
            # print("i",i)
            if i in edited_rows.keys():
                # print("True",edited_rows.keys())
                for key in edited_rows[i].keys():
                    # print("entered",edited_rows[i][key],key)
                    product_data[i][key]=edited_rows[i][key]
        rule_drivers=get_rule_drivers()
        for data in product_data:
            if data["location"]==get_selected_location()["selected_location"]:
                for rule in rule_drivers:
                    rule['parameter_value']=data[rule['condition_parameter']]
        set_rule_drivers(rule_drivers)
        print("#########3",product_data)
        set_locations(product_data)
        apply_rules()
        
    

    def update_value(self,item):
        update_data = st.session_state
        driver_rules=get_rule_drivers()
        for driver in driver_rules:
            # print("driver",driver['condition_parameter'],item['condition_parameter'])
            if driver['condition_parameter']==item['condition_parameter']:
                    # print("updated data",update_data)
                    # print("item data",item)
                    driver['parameter_value']=update_data[item['condition_parameter']+'_value']
        set_rule_drivers(driver_rules)
        apply_rules()

    
        
    def setup_page(self):
        st.markdown(f"""<h1 style='text-align: center; color:white; background-color: #007F00; padding: 5px;'>Dynamic Pricing</h1>""", unsafe_allow_html=True)
        with open("templates/style.css") as f:
            css = f.read()
            st.markdown("<style>{}</style>".format(css), unsafe_allow_html=True)

        
        rules=get_rules()
        container1 = st.container(border=True)
        container1.header("Promotions")
        for rule in rules:
            # print("rules",rule)
            new_range=""
            if rule["condition_lower_limit"]!="NA" and rule["condition_upper_limit"]!="NA":
                new_range=rule["condition_lower_limit"]+" and "+rule["condition_upper_limit"]
            else:
                if rule["condition_lower_limit"]!="NA":
                    new_range=rule["condition_lower_limit"]
                else:
                    new_range=rule["condition_upper_limit"]
            container1.write(f'{rule["rule_id"]}. If {rule["condition_parameter"]} is {rule["condition"]} {new_range} make product {rule["product_id"]} higher by {rule["discount_percentage"]}%.')
            

        container2 = st.container(border=True)
        container2.header("Rule Drivers")
        with container2:
            location_dict=get_locations()
            edited_data = st.data_editor(location_dict,
            disabled=["location"],
            column_config={
                "location":"Location",
                "time":"Time",
                "temperature":"Temperature"
            },
            column_order=["location","time","temperature"],
            key="edited_data",
            width=800,
            on_change=self.process_change,
            args=[location_dict]
            )

        
# Run the app
if __name__ == "__main__":
    web_page=WebPage()
    web_page.setup_page()

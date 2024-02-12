import base64
import streamlit as st
from product_info import get_locations, get_products, get_rule_drivers, get_selected_location, set_selected_location,set_products,apply_rules,set_rule_drivers
# Sample data
data = get_products()
edited_data=data
st.set_page_config(layout="wide",page_icon="static/favicon.ico")
logo_url = './static/apple-touch-icon.png'
st.sidebar.image(logo_url)
class WebPage:
    
    # Function to update data based on edits

    def convert_numbers_to_strings(self,json_data):
        """
        Modifies a JSON-like object (list, dict) to convert all numbers and floats to strings.

        Args:
            json_data (list or dict): The JSON-like object to modify.

        Returns:
            list or dict: The modified JSON-like object.
        """

        if isinstance(json_data, list):
            # Recursively transform list elements
            modified_data = [self.convert_numbers_to_strings(item) for item in json_data]
        elif isinstance(json_data, dict):
            # Convert numeric values in dict
            modified_data = {
                key: self.convert_numbers_to_strings(value) if isinstance(key, str) else key
                for key, value in json_data.items()
            }
        else:
            # Convert numbers or floats to strings
            modified_data = str(json_data) if isinstance(json_data, (int, float)) else json_data

        return modified_data

    def currency_formatter(self,x):
        try:
            new_value=int(x)
            return "£%.2f"
        except:
            return x
        
    
    drivers_data = get_rule_drivers()

    # def update_value(self,item):
    #     update_data = st.session_state
    #     driver_rules=get_rule_drivers()
    #     for driver in driver_rules:
    #         # print("driver",driver['condition_parameter'],item['condition_parameter'])
    #         if driver['condition_parameter']==item['condition_parameter']:
    #                 # print("updated data",update_data)
    #                 # print("item data",item)
    #                 driver['parameter_value']=update_data[item['condition_parameter']+'_value']
    #     set_rule_drivers(driver_rules)
    #     apply_rules()

    def fetch_locations(self):
        print("Received option", st.session_state['location'])
        rule_drivers=get_rule_drivers()
        product_data=get_locations()
        set_selected_location({"selected_location":st.session_state['location']})
        for data in product_data:
            if data["location"]==get_selected_location()["selected_location"]:
                for rule in rule_drivers:
                    rule['parameter_value']=data[rule['condition_parameter']]
        print("Rule drivers",rule_drivers)
        set_rule_drivers(rule_drivers)
        apply_rules()
        
    def process_change(self,new_data):
        edited_rows = st.session_state["edited_data"]["edited_rows"]
        product_data=get_products()
        print("edited_rows")
        for i in range(0,len(product_data)):
            print("i",i)
            if i in edited_rows.keys():
                print("True",edited_rows.keys())
                for key in edited_rows[i].keys():
                    print("entered",edited_rows[i][key],key)
                    product_data[i][key]=edited_rows[i][key]
        product_data=self.convert_numbers_to_strings(product_data)
        # print("###########",product_data)
        set_products(product_data)
        apply_rules()
        
    def setup_page(self):
        # Display table with editable columns
        with open("templates/style.css") as f:
            css = f.read()
            st.markdown("<style>{}</style>".format(css), unsafe_allow_html=True)
        st.markdown(f"""<h1 style='text-align: center; color:white; background-color: #007F00; padding: 5px;'>Dynamic Pricing</h1>""", unsafe_allow_html=True)
        with st.container(border=True):
            columns = st.columns(len(self.drivers_data))
            locations=['Bangalore', 'Bochum','London', 'New York']
            for i in range(0,len(self.drivers_data)):
                with columns[i]:
                    with st.container(border=True):
                        if self.drivers_data[i]["condition_parameter"].lower()=="location":
                            index=locations.index(self.drivers_data[i]["parameter_value"])
                            st.selectbox("Current "+self.drivers_data[i]["condition_parameter"].title()+self.drivers_data[i]["emoji"],options=locations,index=index,key="location",on_change=self.fetch_locations)
                        else:
                            st.write("Current "+self.drivers_data[i]["condition_parameter"].title())
                            st.write(self.drivers_data[i]["emoji"]+" "+self.drivers_data[i]["parameter_value"])
                    # st.button("Update", key=item["condition_parameter"] + "_button")
        new_data=get_products()
        st.header("Table of Products")
        st.markdown(
            """<style>
            .st-data-editor td:nth-child(1) {
                text-align: left !important;
            }
            </style>""",
            unsafe_allow_html=True,
        )

        edited_data = st.data_editor(new_data,
        disabled=[ "product_id","product_image_location","final_price"],
        column_config={
            "product_id":"Product Id",
            "product_name":"Product Name",
            "product_image_location":st.column_config.ImageColumn("Product Image",width="small"),
            "product_price": st.column_config.NumberColumn("Product Price",format="£%.2f"), # Format currency
            "final_price":st.column_config.NumberColumn("Final Price", format="£%.2f") 
        },
        column_order=["product_id","product_image_location","product_name","product_price","final_price"],
        key="edited_data",
        width=800,
        on_change=self.process_change,
        args=[new_data]
        )
        # st.markdown("<p style='text-align: center; color: white; background-color: #007F00; padding: 1rem;'>© 2024 BP p.l.c.</p>", unsafe_allow_html=True)
        # set_products(edited_data)
        # apply_rules()
            
# Run the app
if __name__ == "__main__":
    web_page=WebPage()
    web_page.setup_page()

import json
from datetime import datetime, time

RULES_FILE = 'rules.json'
RULE_DRIVER_FILE = 'rule_driver.json'
PRODUCTS_FILE = 'product_data.json'
LOCATION_FILE='location_driver_details.json'
SELECTED_FILE='selected_location.json'
def read_json(file_name):
    with open(file_name, 'r') as f:
        json_data = json.load(f)
    # print("json_data",json_data)
    return json_data

def write_json(file_name, data_dict):
    with open(file_name, 'w') as f:
        json.dump(data_dict, f, indent=2)

def get_selected_location():
    rules = read_json(file_name=SELECTED_FILE)
    return rules

def set_selected_location(seledted_dict):
    write_json(file_name=SELECTED_FILE, data_dict=seledted_dict)
    
def get_locations():
    rules = read_json(file_name=LOCATION_FILE)
    return rules

def set_locations(locations_dict):
    write_json(file_name=LOCATION_FILE, data_dict=locations_dict)

def get_rules():
    rules = read_json(file_name=RULES_FILE)
    return rules

def set_rules(rules_dict):
    write_json(file_name=RULES_FILE, data_dict=rules_dict)

def get_products():
    products = read_json(file_name=PRODUCTS_FILE)
    return products

def set_products(products_data):
    write_json(file_name=PRODUCTS_FILE,data_dict=products_data)

def get_rule_drivers():
    rule_drivers = read_json(file_name=RULE_DRIVER_FILE)
    return rule_drivers

def set_rule_drivers(rule_drivers_data):
    write_json(file_name=RULE_DRIVER_FILE, data_dict=rule_drivers_data)

def check_higher_condition(current_value, rule_lower_limit, rule_upper_limit = 0):
    # print('current value is ', current_value)
    # print('lower value is ', rule_lower_limit)
    if float(current_value) > float(rule_lower_limit):
        return True
    else:
        return False
    
def check_range_condition(current_value, rule_lower_limit, rule_upper_limit):
    time_format = "%H:%M"
    current_time = datetime.strptime(current_value, time_format).time()
    lower_limit_time = datetime.strptime(rule_lower_limit, time_format).time()
    upper_limit_time = datetime.strptime(rule_upper_limit, time_format).time()
    # print("lower_limit_time",lower_limit_time)
    # print("upper_limit_time",upper_limit_time)
    # print("current_time",current_time)
    if current_time > lower_limit_time and current_time < upper_limit_time:
        return True
    else:
        return False


condition_function_map = {'temperature': check_higher_condition,
                          'time': check_range_condition}

def apply_rules():
    rule_driver_data = get_rule_drivers()
    rules_data = get_rules()
    product_data = get_products()
    discount_percentage_map={}
    for each_rule in rules_data:
        for product_id in each_rule["product_id"]:
            for each_rule_driver in rule_driver_data:
                if each_rule.get('condition_parameter') == each_rule_driver.get('condition_parameter'):
                    if condition_function_map[each_rule.get('condition_parameter')](each_rule_driver.get('parameter_value'), each_rule.get('condition_lower_limit'), each_rule.get('condition_upper_limit')):
                        if product_id not in discount_percentage_map:
                            discount_percentage_map[product_id]=each_rule["discount_percentage"]
                        else:
                            discount_percentage_map[product_id]=max(discount_percentage_map[product_id],each_rule["discount_percentage"])
    # print("discount percentage",discount_percentage_map)
    final_products = []
    for each_product in product_data:
        if each_product["product_id"] in discount_percentage_map:
            # print("entered condition")
            each_product['final_price'] = float(each_product['product_price']) + float(each_product['product_price']) * float(discount_percentage_map[each_product['product_id']]) / 100.0
            each_product['final_price'] = str(round(float(each_product['final_price']), 2))
            # print("final price",each_product['final_price'] )
        else:
            each_product['final_price'] = str(round(float(each_product['product_price']), 2))
        final_products.append(each_product)
    # print('Final Products are :', final_products)
    set_products(final_products)

def update_products(product_data):
    set_products(product_data)
    apply_rules()
    product_data = get_products()
    return product_data

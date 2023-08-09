from datetime import datetime
from itertools import zip_longest
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
# filename = "./examples/hotdocs/hotdocs_blank6.anx"
filename = "./examples/hotdocs/subordinations_example.anx"
# from main import filename2 as filename
print(filename)
tree = ET.parse(filename)

def find_answer(name_tag: str, answer_set: ElementTree = tree.getroot()):
    '''Searches through the .anx file for any element with the given name. 
    If the given name is found, return the element with that name. Otherwise, return None.
    '''
    for child in answer_set[1:]:
        if ('name' in child.attrib) and (child.attrib["name"] == name_tag):
            return child
    # raise Exception(f"Sorry, could not find anything with a name tag equal to \"{name_tag}\"")
    return None

def parse_TextValue(text: str) -> str:
    if text is None: return None
    
    return text

def parse_NumValue(text: str) -> int | float:
    # If the number is a perfect integer, just return the integer.
    # Otherwise, return the float value of that number.
    # (e.g. a HD NumValue of 6.0000000 just becomes 6, but a HD NumValue of 6.5250000 becomes 6.525)
    if text is None: return None
    
    f = float(text)
    if f.is_integer():
        return int(f)
    else:
        return float(text)
    
def parse_DateValue(text: str) -> str:
    if text is None: return None
    
    date_object = datetime.strptime(text, '%d/%m/%Y')
    return date_object.strftime('%Y-%m-%d')

def parse_TFValue(text: str) -> bool:
    if text is None: return None
    
    if text == 'false': return False 
    else: return True

def parse_MCValue(text: str, as_list: bool = False) -> str | list:
    pass

def parse_primitive(name_tag: str, mc_as_list: bool = False):
    answer_element = find_answer(name_tag)
    
    # If the element isn't found, immediately return None
    if answer_element == None:
        return None
    
    child = answer_element[0]
    _type = child.tag
    
    if _type == "TextValue":
        return parse_TextValue(child.text)
    elif _type == "NumValue":
        return parse_NumValue(child.text)
    elif _type == "DateValue":
        return parse_DateValue(child.text)
    elif _type == "TFValue":
        return parse_TFValue(child.text)
    elif _type == "MCValue":
        # If the user wants the MCValue to just appear as a string, make sure theres only one SelValue. 
        # This is the default option because most of the time (like with U.S. state selections) you just want the name of the state.
        if not mc_as_list:
            if (len(child) == 1):
                return child[0].text
            else:
                raise Exception(f"expected only 1 selection, but found {len(child)} in the answer \"{name_tag}\"")
        
        # Otherwise, return all of the SelValues as a list.
        return [value.text for value in child]
    else:
        raise Exception(f'um this is weird this should never pop up. The type was {_type}')
    
def parse_Address(street_element_name, city_element_name, state_element_name, zip_element_name, county_element_name=None):
    result = {
        "street": parse_primitive(street_element_name),
        "city": parse_primitive(city_element_name),
        "state": parse_primitive(state_element_name),
        "zip": parse_primitive(zip_element_name),
        "county": parse_primitive(county_element_name)
    }
    
    # Remove any keys where the value for that key is None (the element was not found).
    result = {key: value for key, value in result.items() if value is not None}
    
def parse_interestStepSpreadsheet(duration_cmp_name, rate_cmp_name):
    interest_step_durations_element = find_answer(duration_cmp_name)
    interest_step_rates_element = find_answer(rate_cmp_name)

    # If the Interest Step TF variable is false, or if both of the columns arent there, just return None for this spreadsheet immediately
    if (not parse_primitive("Interest Step TF")) or ((interest_step_durations_element is None) and (interest_step_rates_element is None)):
        return None
    
    # print('here')
    if interest_step_durations_element is not None:
        durations_as_list = [parse_NumValue(duration.text if duration is not None else None) for duration in interest_step_durations_element[0]]
    else:
        durations_as_list = []
        
    if interest_step_rates_element is not None:
        rates_as_list = [parse_NumValue(rate.text) for rate in interest_step_rates_element[0]]
    else:
        rates_as_list = []
    
    
    # result = [{'duration': duration, 'rate': rate} for duration, rate in zip(durations_as_list, rates_as_list)]
    result = []
    for duration, rate in zip_longest(durations_as_list, rates_as_list, fillvalue=None):
        temp_dict = {}
        if duration is not None:
            temp_dict['duration'] = duration
        if rate is not None:
            temp_dict['rate'] = rate
        if temp_dict:
            result.append(temp_dict)
    return result

def parse_Completion(percent_cmp_name: str, days_cmp_name: str) -> list:
    contract_percent_element = find_answer(percent_cmp_name)
    contract_days_element = find_answer(days_cmp_name)
    
    if contract_percent_element is not None:
        percents_as_list = [parse_NumValue(percent.text) for percent in contract_percent_element[0]]
    else:
        percents_as_list = []
        
    if contract_days_element is not None:
        days_as_list = [parse_NumValue(day.text) for day in contract_days_element[0]]
    else:
        days_as_list = []
        
    result = []
    for percent, day in zip_longest(percents_as_list, days_as_list, fillvalue=None):
        temp_dict = {}
        if percent is not None:
            temp_dict['Percent'] = percent
        if day is not None:
            temp_dict['Deadline'] = day
        if temp_dict:
            result.append(temp_dict)
    return result

def parse_completionGuarantors(guarantor_cmp_name: str) -> list:
    construction_guaranty_name_element = find_answer(guarantor_cmp_name)
    
    if construction_guaranty_name_element is None: return None
    
    result = [name.text for name in construction_guaranty_name_element[0]]
    
    return result

def parse_lenderUCCInformation(lender_name_cmp_name: str, is_individual_cmp_name: str) -> list:
    name_element = find_answer(lender_name_cmp_name)
    is_individual_element = find_answer(is_individual_cmp_name)
    
    if name_element is not None:
        names_as_list = [parse_TextValue(name.text) for name in name_element[0]]
    else:
        names_as_list = []
        
    if is_individual_element is not None:
        is_individuals_as_list = [parse_TFValue(individual.text) for individual in is_individual_element[0]]
    else:
        is_individuals_as_list = []
        
    result = []
    for name, is_individual in zip_longest(names_as_list, is_individuals_as_list, fillvalue=None):
        temp_dict = {}
        if name is not None:
            temp_dict['name'] = name
        if is_individual is not None:
            temp_dict['isIndividual'] = is_individual
        if temp_dict:
            result.append(temp_dict)
    
    if not result:
        return None
    else:
        return result

def parse_DebtServiceType(interest_reserve_cmp_name: str, interest_reserve_months_cmp_name: str) -> str:
    interest_reserve_element = find_answer(interest_reserve_cmp_name)
    interest_reserve_months_element = find_answer(interest_reserve_months_cmp_name)
    
    if (interest_reserve_element is None) or (interest_reserve_element[0].text == 'false'): return 'None'
    
    if interest_reserve_months_element[0].text == 'true': 
        return 'Monthly Payments'
    elif interest_reserve_months_element[0].text == 'false': 
        return 'Dollar Amount'
    else:
        return 'Um this should never appear for DebtServiceType'
    
def parse_security_OwnershipSpreadsheet(name_cmp: str, individual_cmp: str, signer_1_cmp: str, title_cmp: str, state_cmp: str) -> list[dict]:
    name_element = find_answer(name_cmp) # Membership Pledgor Name TE
    individual_element = find_answer(individual_cmp) # Membership Pledgor Ind TF
    signer_1_element = find_answer(signer_1_cmp) # Membership Pledgor Signer 1 TE
    title_element = find_answer(title_cmp) # Membership Pledgor Title TE
    state_element = find_answer(state_cmp) # Membership Pledgor State MC
    
    if name_element is not None: names_list = [parse_TextValue(name.text) for name in name_element[0]]
    else: names_list = []
    
    if individual_element is not None: individuals_list = [parse_TFValue(individual.text) for individual in individual_element[0]]
    else: individuals_list = []
    
    if signer_1_element is not None: signers_list = [parse_TextValue(signer.text) for signer in signer_1_element[0]]
    else: signers_list = []
    
    if title_element is not None: titles_list = [parse_TextValue(title.text) for title in title_element[0]]
    else: titles_list = []
    
    if state_element is not None:
        states_list = [parse_TextValue(state[0].text) for state in state_element[0] if len(state)]
    else: 
        states_list = []
    
    result = []
    for name, individual, signer, title, state in zip_longest(names_list, individuals_list, signers_list, titles_list, states_list):
        temp_dict = {}
        if name is not None: temp_dict['name'] = name
        if individual is not None: temp_dict['isIndividual'] = individual
        if signer is not None: temp_dict['signerForPledgor'] = signer
        if title is not None: temp_dict['title'] = title
        if state is not None: temp_dict['state'] = state
        
        if (name is None) and (signer is None) and (title is None) and (state is None):
            continue # If the row is all empty besides individual, just skip it. This is because there will always be one extra TFValue (i think)
        
        if temp_dict:
            result.append(temp_dict)
    return result
    
def parse_Security_CSADebtorSpreadsheet(name_cmp: str, individual_cmp: str, title_cmp: str, signer_cmp: str, state_cmp: str) -> list[dict]:
    name_element = find_answer(name_cmp) # CSA Debtor Name TE
    individual_element = find_answer(individual_cmp) # CSA Debtor Ind TF
    title_element = find_answer(title_cmp) # CSA Debtor Signer 1 Title TE
    signer_element = find_answer(signer_cmp) # CSA Debtor Signer 1 TE
    state_element = find_answer(state_cmp) # CSA Debtor State MC
    
    if name_element is not None: names_list = [parse_TextValue(name.text) for name in name_element[0]]
    else: names_list = []
    
    if individual_element is not None: individuals_list = [parse_TFValue(individual.text) for individual in individual_element[0]]
    else: individuals_list = []
    
    if title_element is not None: titles_list = [parse_TextValue(title.text) for title in title_element[0]]
    else: titles_list = []
    
    if signer_element is not None: signers_list = [parse_TextValue(signer.text) for signer in signer_element[0]]
    else: signers_list = []
    
    if state_element is not None:
        states_list = [parse_TextValue(state[0].text) for state in state_element[0] if len(state)]
    else:
        states_list = []
        
    result = []
    for name, individual, title, signer, state in zip_longest(names_list, individuals_list, titles_list, signers_list, states_list):
        temp_dict = {}
        if name is not None: temp_dict['debtorNameWithVesting'] = name
        if individual is not None: temp_dict['isIndividual'] = individual
        if title is not None: temp_dict['title'] = title
        if signer is not None: temp_dict['signerForDebtor'] = signer
        if state is not None: temp_dict['state'] = state
        
        if (name is None) and (signer is None) and (title is None) and (state is None):
            continue # If the row is all empty besides individual, just skip it. This is because there will always be one extra TFValue
        
        if temp_dict:
            result.append(temp_dict)
    return result
    
def parse_MultipleLenders(name_cmp: str, amount_cmp: str) -> list[dict]:
    name_element = find_answer(name_cmp) # Lender Name TE
    amount_element = find_answer(amount_cmp) # Lender Invest Amount NU
    
    if (name_element is None) and (amount_element is None): return None
    
    if name_element is not None:
        names_list = [parse_TextValue(name.text) for name in name_element[0]]
    else:
        names_list = []
        
    if amount_element is not None:
        amounts_list = [parse_NumValue(amount.text) for amount in amount_element[0]]
    else:
        amounts_list = []
        
    result = []
    for name, amount in zip_longest(names_list, amounts_list):
        temp_dict = {}
        if name is not None: temp_dict['Name'] = name
        if amount is not None: temp_dict['Amount'] = amount
        
        if temp_dict:
            result.append(temp_dict)
    return result

def parse_isExhibitALenders(exhibit_a_cmp: str) -> bool:
    exhibit_a_element = find_answer(exhibit_a_cmp)
    
    for answer in exhibit_a_element[0]:
        if answer.text == 'true': return True
    return False

def parse_Lender(lender_cmp: str) -> str:
    lender_element = find_answer(lender_cmp)
    isMultipleLenders = parse_primitive("seth_MultipleLendersTF")
    isLenderUnknown = parse_TFValue(find_answer("Exhibit A Lender List TF")[0][0].text)
    
    if isMultipleLenders: 
        return None
    
    if isLenderUnknown:
        return None
    
    return lender_element[0][0].text
    
def parse_isEscrow(dropdown_cmp: str) -> bool:
    dropdown_element = find_answer(dropdown_cmp)
    selection = dropdown_element[0][0].text
    
    if selection == 'Escrow and Title':
        return True
    elif selection == 'Title Only':
        return False
    else:
        raise Exception("i have no idea how I got here. The selection was \"{selection}\"")
    
def parse_FeesSpreadsheet(fee_cmp: str, description_cmp: str, comment_cmp: str, paid_to_cmp: str=None) -> list[dict]:
    fee_element = find_answer(fee_cmp)
    description_element = find_answer(description_cmp)
    comment_element = find_answer(comment_cmp)
    paid_to_element = find_answer(paid_to_cmp) if paid_to_cmp is not None else None
    
    if fee_element is not None:
        fees_list = [parse_NumValue(fee.text) for fee in fee_element[0]]
    else:
        fees_list = []
        
    if description_element is not None:
        descriptions_list = [parse_TextValue(description.text) for description in description_element[0]]
    else:
        descriptions_list = []
    
    if comment_element is not None:
        # comments_list = [comment[0].text for comment in comment_element[0] if len(comment)]
        comments_list = [comment[0].text if len(comment) else None for comment in comment_element[0]]
    else:
        comments_list = []
        
    if paid_to_element is not None:
        paid_to_list = [answer.text for answer in paid_to_element[0]]
    else:
        paid_to_list = []
        
    result = []
    for fee, description, comment, paid_to in zip_longest(fees_list, descriptions_list, comments_list, paid_to_list):
        temp_dict = {}
        if fee is not None: temp_dict['amount'] = fee
        if description is not None: temp_dict['description'] = description
        if comment is not None: temp_dict['comment'] = comment
        if paid_to is not None: temp_dict['paidTo'] = paid_to
        
        if temp_dict:
            result.append(temp_dict)
    return result
    
def parse_geraciFee(fee_cmp: str) -> int:
    fee_element = find_answer(fee_cmp)
    
    if fee_element is None: return None
    
    if len(fee_element[0]) != 1:
        raise Exception(f"thats weird, there should really only be one value for {fee_cmp}, but there was {len(fee_element[0])}")
    
    return parse_NumValue(fee_element[0][0].text)

def parse_geraciFeeDelivery(delivery_cmp: str) -> str:
    delivery_element = find_answer(delivery_cmp)
    if delivery_element is None: return None
    
    if len(delivery_element[0]) != 1:
        raise Exception(f"thats weird, there should really only be one value for {delivery_cmp}, but there was actually {len(delivery_element[0])}")
    
    return parse_TextValue(delivery_element[0][0][0].text)

def parse_assignment_Spreadsheet_list(property_cmp: str, manager_cmp: str, date_cmp: str, street_cmp: str, city_cmp: str, state_cmp: str, zip_cmp: str) -> list[dict]:
    property_element = find_answer(property_cmp)
    manager_element = find_answer(manager_cmp)
    date_element = find_answer(date_cmp)
    street_element = find_answer(street_cmp)
    city_element = find_answer(city_cmp)
    state_element = find_answer(state_cmp)
    zip_element = find_answer(zip_cmp)
    
    properties_list = []
    if property_element is not None: properties_list = [prop[0].text if len(prop) else None for prop in property_element[0]]
    
    managers_list = []
    if manager_element is not None: managers_list = [parse_TextValue(manager.text) for manager in manager_element[0]]
    
    dates_list = []
    if date_element is not None: dates_list = [parse_DateValue(date.text) for date in date_element[0]]
    
    streets_list = []
    if street_element is not None: streets_list = [parse_TextValue(street.text) for street in street_element[0]]
    
    cities_list = []
    if city_element is not None: cities_list = [parse_TextValue(city.text) for city in city_element[0]]
    
    states_list = []
    if state_element is not None: states_list = [parse_TextValue(state[0].text) for state in state_element[0] if len(state)]
    
    zips_list = []
    if zip_element is not None: zips_list = [parse_TextValue(zipcode.text) for zipcode in zip_element[0]]
    
    result = []
    for property, manager, date, street, city, state, zipcode in zip_longest(properties_list, managers_list, dates_list, streets_list, cities_list, states_list, zips_list):
        temp_dict = {}
        if property is not None: temp_dict['Property'] = property
        if manager is not None: temp_dict['propertyManager'] = manager
        if date is not None: temp_dict['agreementDate'] = date
        address = {}
        if street is not None: address['street'] = street
        if city is not None: address['city'] = city
        if state is not None: address['state'] = state
        if zipcode is not None: address['zip'] = zipcode
        if address:
            temp_dict['address'] = address
        if temp_dict:
            result.append(temp_dict)
    return result

def parse_isSubordinations(loan_docs_cmp: str) -> bool:
    loan_docs_element = find_answer(loan_docs_cmp)
    
    if loan_docs_element is None: return None
    
    selected_choices = [selection.text for selection in loan_docs_element[0]]
    if "Subordination" in selected_choices:
        return True
    else:
        return False
    
def parse_subordinations_list(docs_cmp: str, property_cmp: str, post_closing_cmp: str, document_name_cmp: str, document_date_cmp: str, months_cmp: str, tenants_cmp: str) -> list[dict]:
    docs_element = find_answer(docs_cmp)
    property_element = find_answer(property_cmp)
    post_closing_element = find_answer(post_closing_cmp)
    document_name_element = find_answer(document_name_cmp)
    document_date_element = find_answer(document_date_cmp)
    months_element = find_answer(months_cmp)
    tenants_element = find_answer(tenants_cmp)
    
    docs_as_list = []
    if docs_element is not None:
        for MCValue in docs_element[0]:
            if len(MCValue) == 0:
                docs_as_list.append(None)
            else:
                choices = []
                for SelValue in MCValue:
                    choices.append(SelValue.text)
                docs_as_list.append(choices)
                
    property_as_list = []
    if property_element is not None:
        property_as_list = [prop.text for prop in property_element[0]]
        
    post_closing_as_list = []
    if post_closing_element is not None:
        post_closing_as_list = [parse_TFValue(answer.text) for answer in post_closing_element[0]]
        
    document_name_as_list = []
    if document_name_element is not None:
        document_name_as_list = [name.text for name in document_name_element[0]]
        
    document_date_as_list = []
    if document_date_element is not None:
        document_date_as_list = [parse_DateValue(date.text) for date in document_date_element[0]]
    
    months_as_list = []
    if months_element is not None:
        months_as_list = [parse_NumValue(num_months.text) for num_months in months_element[0]]
        
    tenants_as_list = []
    if tenants_element is not None:
        for RpTValue in tenants_element[0][:-1]: # Use '[:-1]' to exclude the last element, since it is always unanswered / unnecessary
            if len(RpTValue) == 0:
                tenants_as_list.append(None)
            else:
                tenants = [tenant.text for tenant in RpTValue if tenant.text is not None]
                if len(tenants): tenants_as_list.append(tenants)
                else: tenants_as_list.append(None)
    if len(tenants_as_list) == 0:
        tenants_as_list = None
                
    result = []
    for docs, property, post_closing, document_name, document_date, months, tenants in zip_longest(docs_as_list, property_as_list, post_closing_as_list, document_name_as_list, document_date_as_list, months_as_list, tenants_as_list):
        temp_dict = {}
        if docs is not None: temp_dict['documentType'] = docs
        if property is not None: temp_dict['property'] = property
        if post_closing is not None: temp_dict['postClosing'] = post_closing
        if document_name is not None: temp_dict['documentName'] = document_name
        if document_date is not None: temp_dict['documentDate'] = document_date
        if months is not None: temp_dict['leaseMonths'] = months
        if tenants is not None: temp_dict['tenantNames'] = tenants
        
        if temp_dict:
            result.append(temp_dict)
    if len(result): return result
    else: return None
    
def remove_none_values(dictionary: dict) -> dict:
    new_dict = {}
    for key, value in list(dictionary.items()):
        if isinstance(value, dict):
            new_dict[key] = remove_none_values(value)
        elif value is not None:
            new_dict[key] = value
            
    return new_dict

def main():
    # print(find_answer('Borrower City TE'))
    # print(parse_primitive("Assignment and Allonge Concurrent MC"))
    print(parse_primitive("Loan Documents MC", True))
    # pass

if __name__ == "__main__":
    main()
def type_address(
    street: str = None,
    city: str = None,
    state: str = None,
    zip: str = None,
    county: str = None,
) -> dict:
    x = {"street": street, "city": city, "state": state, "zip": zip, "county": county}
    y = {key: value for key, value in x.items() if value is not None}
    return y


def type_interestStepSpreadsheet(duration: int, rate: int) -> dict:
    x = {"duration": duration, "rate": rate}
    y = {key: value for key, value in x.items() if value is not None}
    return y


def type_construction_completion(percent: int, deadline: int) -> dict:
    x = {"Percent": percent, "Deadline": deadline}
    y = {key: value for key, value in x.items() if value is not None}
    return y


def type_completion_guarantors(names: list) -> list:
    return names


def type_deferred_broker_type(deferred_broker_fees_tf: bool, question: str) -> str:
    if deferred_broker_fees_tf and question == "Deferred Broker Fee NU":
        return "Dollar"
    if deferred_broker_fees_tf and question == "Deferred Broker Fee Percent NU":
        return "Percentage"
    else:
        return None


def type_debt_service_type(
    interest_reserve_tf: bool, interest_reserve_months_tf: bool
) -> str:
    if interest_reserve_tf and interest_reserve_months_tf:
        return "Monthly Payments"
    elif interest_reserve_tf:
        return "Dollar Amount"
    else:
        return None


def type_security_ownership_spreadsheet(
    name: str = None,
    is_individual: bool = None,
    signer_for_pledgor: str = None,
    title: str = None,
    state: str = None,
):
    x = {
        "name": name,
        "isIndividual": is_individual,
        "signerForPledgor": signer_for_pledgor,
        "title": title,
        "state": state,
    }
    y = {key: value for key, value in x.items() if value is not None}
    return y


def type_security_csa_debtor_spreadsheet(
    debtor_name_with_vesting: str = None,
    is_individual: bool = None,
    title: str = None,
    signer_for_debtor: str = None,
    state: str = None,
):
    x = {
        "debtorNameWithVesting": debtor_name_with_vesting,
        "isIndividual": is_individual,
        "title": title,
        "signerForDebtor": signer_for_debtor,
        "state": state,
    }
    y = {key: value for key, value in x.items() if value is not None}
    return y


def type_lender_ucc_information(name: str = None, is_individual: bool = None):
    x = {"name": name, "isIndividual": is_individual}
    y = {key: value for key, value in x.items() if value is not None}
    return y


def type_is_escrow(multiple_choice: str = None) -> list:
    if multiple_choice == "Escrow and Title":
        return True
    else:
        return False


def type_loan_documents_mc():
    return "wwwwwwwwwwww"


def main():
    pass


if __name__ == "__main__":
    main()

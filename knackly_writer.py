from bson import ObjectId
from itertools import zip_longest
from pprint import pprint

from anx_parser import ANX_Parser


class Knackly_Writer:
    def __init__(self, anx_parser: ANX_Parser):
        self.anx = anx_parser
        self.json = {"id$": str(ObjectId())}
        self.uuid_map = {
            "Borrowers": {},
            "Signers": {},
            "Guarantors": {},
            "Trustees": {},
            "Properties": {},
        }
        # In the uuid map for borrowers, the key will be the entities name, and the value will be the generated uuid
        # For example:
        # self.uuid_map = {
        #     "Borrowers": {
        #         "Borrower A": "653fea131c45e2b8dddef937",
        #         "Borrower B": "653fea131c45e2b8dddef938",
        #         "Borrower C": "653fea131c45e2b8dddef939"
        #     }
        # }

    def remove_none_values(self, dictionary: dict) -> dict:
        """Recursively removes all occurrences of "None" within a dictionary
        This is moreso a helper function to make sure that self.json is kept clean.

        Args:
            dictionary (dict): The dictionary to which "None" values will be removed.

        Returns:
            dict: The new dictionary, without any "None" values
        """
        if isinstance(dictionary, dict):
            return {
                key: self.remove_none_values(value)
                for key, value in dictionary.items()
                if value is not None
            }
        elif isinstance(dictionary, list):
            return [
                self.remove_none_values(item) for item in dictionary if item is not None
            ]
        else:
            return dictionary

    def address(
        self,
        street: str,
        city: str,
        state: str,
        zip: str,
        county: str = None,
    ) -> dict:
        """Returns a Knackly "Address" object.

        Args:
            street (str): The street name
            city (str): The city
            state (str): The state
            zip (str): The zip code
            county (str, optional): The county. Defaults to None.

        Returns:
            dict: The Knackly "Address" dictionary.
        """
        result = {
            "id$": str(ObjectId()),
            "street": street,
            "city": city,
            "state": state,
            "zip": zip,
            "county": county,
        }

        return self.remove_none_values(result)

    def borrower_information(
        self,
    ) -> (
        dict
    ):  # This isn't complete yet. Doesn't account for BorrowerSigners, BorrowerOwners, or Trustee stuff. I am leaving it incomplete because I am losing my mind trying to do this right now, and need to work on something else.
        """Creates the "Borrower" dictionary (on the top level of the Knackly interview)

        Returns:
            dict: The properly formatted "Borrower" dictionary
        """

        def borrower_setup() -> list[dict]:
            pass

            def create_borrower(
                name: str,
                type: str,
                is_aif: bool,
                aif_name: str,
                borrower_org_state: str,
            ) -> dict:
                id_ = str(ObjectId())
                self.uuid_map["Borrowers"].update({name: id_})

                result = {
                    "id$": id_,
                    "BorrowerName": name,
                    "BorrowerEntityType": type,
                    "IsBorrowerAIF": is_aif,
                    "AIFName": aif_name,
                    "BorrowerOrgState": borrower_org_state,
                }

                return self.remove_none_values(result)

            result = []
            for name, entity_type, is_aif, aif_name, borrower_org_state in zip_longest(
                self.anx.parse_RptValue(self.anx.find_answer("Borrower Name TE"))[:-1],
                self.anx.parse_RptValue(
                    self.anx.find_answer("Borrower Entity Type MC")
                )[:-1],
                self.anx.parse_RptValue(
                    self.anx.find_answer("B signature attorney in fact TF")
                ),
                self.anx.parse_RptValue(
                    self.anx.find_answer("B signature attorney in fact name TX")
                ),
                self.anx.parse_RptValue(
                    self.anx.find_answer("Borrower Organization State MC")
                ),
            ):
                new_borrower = create_borrower(
                    name, entity_type, is_aif, aif_name, borrower_org_state
                )
                result.append(new_borrower)
            return result

        result = {
            "id$": str(ObjectId()),
            "Borrowers": borrower_setup(),
            "BorrowerNoticeSentTo": self.anx.parse_MCValue(
                self.anx.find_answer("Borrower Notice MC")
            ),
            "Notice": self.address(
                street=self.anx.parse_TextValue(
                    self.anx.find_answer("Borrower Street Address TE")
                ),
                city=self.anx.parse_TextValue(self.anx.find_answer("Borrower City TE")),
                state=self.anx.parse_MCValue(self.anx.find_answer("Borrower State MC")),
                zip=self.anx.parse_TextValue(
                    self.anx.find_answer("Borrower Zip Code TE")
                ),
            ),
            "BorrowerDeliveryTo": self.anx.parse_TextValue(
                self.anx.find_answer("Borrower Delivery To Notice TE")
            ),
        }

        return self.remove_none_values(result)

    def non_borrower_property_owners(self) -> dict:
        raise NotImplementedError

    def property_information(self) -> dict:
        raise NotImplementedError

    def standard_loan_terms(self) -> dict:
        """Produces the top level `loanTerms` object in the Knackly json.

        Returns:
            dict: The top level `loanTerms` object. For any values that ended up being `None`, they are removed before returning.
        """

        def variable_rate_setup() -> dict:
            """Produce the variableRate object for the Knackly json.

            Returns:
                dict: The full variableRate object. For any values that were `None`, they are removed before returning.
            """
            result = {
                "id$": str(ObjectId()),
                "margin": self.anx.parse_NumValue(
                    self.anx.find_answer("Variable Margin NM")
                ),
                "isDailyFloatingRate": self.anx.parse_TFValue(
                    self.anx.find_answer("Rate Adjust Daily TF")
                ),
                "changeDate": self.anx.parse_NumValue(
                    self.anx.find_answer("Variable Change Date NU")
                ),
                "armAdjustmentPeriod": self.anx.parse_NumValue(
                    self.anx.find_answer("Variable ARM Adjustment Period NM")
                ),
                "firstInterestCap": self.anx.parse_NumValue(
                    self.anx.find_answer("Variable First Interest Cap NM")
                ),
                "subsequentInterestCap": self.anx.parse_NumValue(
                    self.anx.find_answer("Variable Subsequent Interest Cap NM")
                ),
                "floorRate": self.anx.parse_NumValue(
                    self.anx.find_answer("Variable Floor Rate NM")
                ),
                "maximumInterestRateCap": self.anx.parse_NumValue(
                    self.anx.find_answer("Variable Maximum interest Rate Cap NM")
                ),
                "interestRateIndex": self.anx.parse_MCValue(
                    self.anx.find_answer("Variable Interest Rate Index MC")
                ),
            }

            return self.remove_none_values(result)

        def interest_step_spreadsheet_setup() -> list[dict]:
            """Produces the entire interestStepSpreadsheet object for the Knackly json.

            Returns:
                list[dict]: A list where each element is a dictionary containing an interest step object
            """

            def create_interest_step(rate: int | float, duration: int) -> dict:
                """Produces an interest_step object

                Args:
                    rate (int | float): The interest rate (%)
                    duration (int): The number of months

                Returns:
                    dict: A dictionary containing the rate, duration, and a bson uuid. If both rate and duration are `None`, then returns `None`.
                """
                if rate is None and duration is None:
                    return None
                result = {"id$": str(ObjectId()), "rate": rate, "duration": duration}
                return self.remove_none_values(result)

            interest_step_rate_nu = self.anx.parse_RptValue(
                self.anx.find_answer("Interest Step Rate NU")
            )
            interest_step_duration_nu = self.anx.parse_RptValue(
                self.anx.find_answer("Interest Step Duration NU")
            )

            # If either of the options are not found in the .anx file, return None immediately
            if interest_step_rate_nu is None or interest_step_duration_nu is None:
                return None

            result = [
                create_interest_step(rate, duration)
                for rate, duration in zip_longest(
                    self.anx.parse_RptValue(
                        self.anx.find_answer("Interest Step Rate NU")
                    ),
                    self.anx.parse_RptValue(
                        self.anx.find_answer("Interest Step Duration NU")
                    ),
                )
            ]
            return result

        result = {
            "closingDate": self.anx.parse_DateValue(
                self.anx.find_answer("Document Date DT")
            ),
            "loanNumber": self.anx.parse_TextValue(
                self.anx.find_answer("Loan Number TE")
            ),
            "loanTerm": self.anx.parse_NumValue(self.anx.find_answer("Loan Term NU")),
            "loanAmount1": self.anx.parse_NumValue(
                self.anx.find_answer("Loan Amount NU")
            ),
            "firstPaymentDate": self.anx.parse_DateValue(
                self.anx.find_answer("First Payment DT")
            ),
            "isInterestOnly": self.anx.parse_TFValue(
                self.anx.find_answer("Loan Type Interest Only TF")
            ),
            "interestOnlyMonths": self.anx.parse_NumValue(
                self.anx.find_answer("Variable Interest Rate Interest Only Period NM")
            ),
            "amortizationMonths": self.anx.parse_NumValue(
                self.anx.find_answer("Amortization Period NU")
            ),
            # ---
            "interestRate": self.anx.parse_NumValue(
                self.anx.find_answer("Interest Rate NU")
            ),
            "defaultInterestRate": self.anx.parse_NumValue(
                self.anx.find_answer("Default Interest Rate NU")
            ),
            "interestCalcType": self.anx.parse_MCValue(
                self.anx.find_answer("Interest Calc Type MC")
            ),
            "isVariableRate": self.anx.parse_TFValue(
                self.anx.find_answer("Loan Type Variable TF")
            ),
            "variableRate": variable_rate_setup(),
            "isInterestStep": self.anx.parse_TFValue(
                self.anx.find_answer("Interest Step TF")
            ),
            "interestStepSpreadsheet": interest_step_spreadsheet_setup(),
            "isMERSLoan": self.anx.parse_TFValue(self.anx.find_answer("MERS TF")),
            "mersNumber": self.anx.parse_TextValue(
                self.anx.find_answer("MERS Number TE")
            ),
            "PrincipalRepaymentPercent": self.anx.parse_NumValue(
                self.anx.find_answer("Principal Repayment Percent NU")
            ),
            "MaturityDate": self.anx.parse_DateValue(
                self.anx.find_answer("Maturity DT")
            ),
            "paymentInAdvance": self.anx.parse_TFValue(
                self.anx.find_answer("Payment in Advance TF")
            ),
        }

        return self.remove_none_values(result)

    def create(self) -> None:
        """Actually fill out `self.json` with all of the relevant information."""
        # self.json.update({"Borrower": self.borrower_information()}) # This is broken UGH
        # self.json["TitleHolder2"] = self.non_borrower_property_owners()
        # self.json["propertyInformation"] = self.property_information()
        # self.json["loanTerms"] = self.standard_loan_terms()
        self.json.update({"loanTerms": self.standard_loan_terms()})

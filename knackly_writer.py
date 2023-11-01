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

    def is_all_args_none(self, args: dict | list) -> bool:
        """Helper function to check if all of the arguments provided to it were `None`.

        Args:
            args (dict | list): Either a dictionary where the values for each key are what is checked (for use with `.locals()`), or a list of elements.

        Raises:
            TypeError: `True` if every argument's value is `None`, otherwise `False`.

        Returns:
            bool: _description_
        """
        if isinstance(args, dict):
            return all(value is None for value in args.values())
        elif isinstance(args, list):
            return all(value is None for value in args)
        else:
            # This should never run
            raise TypeError(
                f"Expected a dictionary or a list, but got {type(args).__name__}"
            )

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
            "id$": str(ObjectId()),
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

        if result.get("isVariableRate"):
            result["variableRate"] = variable_rate_setup()
        if result.get("isInterestStep"):
            result["interestStepSpreadsheet"] = interest_step_spreadsheet_setup()

        return self.remove_none_values(result)

    def special_loan_features(self) -> dict:
        def line_of_credit_setup():
            result = {
                "id$": str(ObjectId()),
                "isRevolving": self.anx.parse_TFValue(
                    self.anx.find_answer("Credit Line Revolving TF")
                ),
                "minAdvanceRequest": self.anx.parse_NumValue(
                    self.anx.find_answer("Credit Line Minimum Request NU")
                ),
                "advanceRequestFee": self.anx.parse_NumValue(
                    self.anx.find_answer("Credit Line Request Fee NU")
                ),
                "maxDrawsPerMonth": self.anx.parse_NumValue(
                    self.anx.find_answer("Credit Line Maximum Draws NU")
                ),
                "minOutstandingPrincipalBal": self.anx.parse_NumValue(
                    self.anx.find_answer("Credit Line Minimum Balance NU")
                ),
            }

            return self.remove_none_values(result)

        def penalties_setup():
            def prepay_non_linear_setup():
                number = self.anx.parse_RptValue(
                    self.anx.find_answer("Prepay Non Percent NU")
                )
                if number is None:
                    return None

                return {
                    "id$": str(ObjectId()),
                    "Percent": number[0],
                }  # number will be a list, but HotDocs ensures that it can only be one element long

            result = {
                "id$": str(ObjectId()),
                "PrepaymentPenalty": self.anx.parse_MCValue(
                    self.anx.find_answer("Prepay MC")
                ),
                "PrepayTerm": self.anx.parse_NumValue(
                    self.anx.find_answer("Prepay Term NU")
                ),
                "IsPrepay20Percent": self.anx.parse_TFValue(
                    self.anx.find_answer("Prepay 20 Percent TF")
                ),
                "PenatlyCalculatedFrom": self.anx.parse_MCValue(
                    self.anx.find_answer("Prepay Lock Penalty MC")
                ),
                "IsPrepayLockYield": self.anx.parse_TFValue(
                    self.anx.find_answer("Prepay Lock Yield TF")
                ),
                "PrepayNonlinear": prepay_non_linear_setup(),
                "PrepayLockDollars": self.anx.parse_NumValue(
                    self.anx.find_answer("Prepay Lock Dollars NU")
                ),
                "PrepayLockMonths": self.anx.parse_NumValue(
                    self.anx.find_answer("Prepay Lock Months NU")
                ),
                "PrepayLockPercent": self.anx.parse_NumValue(
                    self.anx.find_answer("Prepay Lock Percent NU")
                ),
                "prepaymentPremiumMonths": self.anx.parse_NumValue(
                    self.anx.find_answer("Prepayment Premium Months NU")
                ),
            }

            return self.remove_none_values(result)

        def construction_setup():
            def completion_setup():
                percents = self.anx.parse_RptValue(
                    self.anx.find_answer("Construction Contract Percent NU")
                )
                days = self.anx.parse_RptValue(
                    self.anx.find_answer("Construction Contract Days NU")
                )

                # Make sure that the percents and days lists aren't both None
                if self.is_all_args_none(locals()):
                    return None

                result = []
                for percent, day in zip_longest(percents, days):
                    if self.is_all_args_none([percent, day]):
                        continue
                    temp = {"id$": str(ObjectId()), "Percent": percent, "Deadline": day}
                    result.append(temp)

                return self.remove_none_values(result)

            result = {
                "id$": str(ObjectId()),
                "reserve": self.anx.parse_NumValue(
                    self.anx.find_answer("Holdback Amount NU")
                ),
                "IsNonDutch": self.anx.parse_TFValue(
                    self.anx.find_answer("Non Dutch TF")
                ),
                "Type": self.anx.parse_MCValue(
                    self.anx.find_answer("Construction Type MC")
                ),
                "IsExcludeSchedule": self.anx.parse_TFValue(
                    self.anx.find_answer("Exclude Disbursement Schedule TF")
                ),
                "IsRetainageRequired": self.anx.parse_TFValue(
                    self.anx.find_answer("Retainage Required TF")
                ),
                "IsThirdPartyFCA": self.anx.parse_TFValue(
                    self.anx.find_answer("Construction Fund Control TF")
                ),
                "isAssignmentOfPermits": self.anx.parse_TFValue(
                    self.anx.find_answer("Assignment of Permits TF")
                ),
                "isInspectionFee": self.anx.parse_TFValue(
                    self.anx.find_answer("seth_Inspection Fee TF")
                ),
                "inspectionFee": self.anx.parse_NumValue(
                    self.anx.find_answer("Inspection Fee NU")
                ),
                "IsConstructionContract": self.anx.parse_TFValue(
                    self.anx.find_answer("Construction Contract TF")
                ),
                "ContractorName": self.anx.parse_TextValue(
                    self.anx.find_answer("Construction Contractor TE")
                ),
                "IsDesignContract": self.anx.parse_TFValue(
                    self.anx.find_answer("Construction Design Contract TF")
                ),
                "DesignerName": self.anx.parse_TextValue(
                    self.anx.find_answer("Construction Designer TE")
                ),
                "isThirdPartyConstructionGuaranty": self.anx.parse_TFValue(
                    self.anx.find_answer("Guaranty of Completion TF")
                ),
                "completionGuarantors": self.anx.parse_RptValue(
                    self.anx.find_answer("Construction Guaranty Name TX")
                ),
                "doesConstructionBorrowerContribute": self.anx.parse_TFValue(
                    self.anx.find_answer("Construction Borrower Contribution TF")
                ),
                "constructionBorrowerContribution": self.anx.parse_NumValue(
                    self.anx.find_answer("Construction Borrower Contribution NU")
                ),
            }

            if result.get("IsConstructionContract"):
                result.update(
                    {
                        "Contractor": self.address(
                            street=self.anx.parse_TextValue(
                                self.anx.find_answer("Contractor Street Address TE")
                            ),
                            city=self.anx.parse_TextValue(
                                self.anx.find_answer("Contractor City TE")
                            ),
                            state=self.anx.parse_MCValue(
                                self.anx.find_answer("Contractor State MC")
                            ),
                            zip=self.anx.parse_TextValue(
                                self.anx.find_answer("Contractor Zip TE")
                            ),
                        ),
                        "Completion": completion_setup(),
                    }
                )
            if result.get("IsDesignContract"):
                result.update(
                    {
                        "Designer": self.address(
                            street=self.anx.parse_TextValue(
                                self.anx.find_answer("Designer Street Address TE")
                            ),
                            city=self.anx.parse_TextValue(
                                self.anx.find_answer("Designer City TE")
                            ),
                            state=self.anx.parse_MCValue(
                                self.anx.find_answer("Designer State MC")
                            ),
                            zip=self.anx.parse_TextValue(
                                self.anx.find_answer("Designer Zip TE")
                            ),
                        )
                    }
                )

            return self.remove_none_values(result)

        def loan_features_setup():
            pass

        def reserves_setup():
            pass

        def impounds_setup():
            pass

        result = {
            "isLineOfCredit": self.anx.parse_TFValue(
                self.anx.find_answer("Credit Line TF")
            ),
            "lineOfCreditPage": line_of_credit_setup(),
            "penalties": penalties_setup(),
            "isConstructionReserve": self.anx.parse_TFValue(
                self.anx.find_answer("Construction Holdback TF")
            ),
            "construction1": construction_setup(),
            "loanFeatures": loan_features_setup(),
            "reserves": reserves_setup(),
            "isImpounds1": self.anx.parse_TFValue(
                self.anx.find_answer("Impound Accounts TF")
            ),
            "impounds1": impounds_setup(),
        }

        return self.remove_none_values(result)

    def create(self) -> None:
        """Actually fill out `self.json` with all of the relevant information."""
        # self.json.update({"Borrower": self.borrower_information()}) # This is broken UGH
        # self.json["TitleHolder2"] = self.non_borrower_property_owners()
        # self.json["propertyInformation"] = self.property_information()
        # self.json["loanTerms"] = self.standard_loan_terms()
        self.json.update({"loanTerms": self.standard_loan_terms()})
        self.json.update({"features": self.special_loan_features()})

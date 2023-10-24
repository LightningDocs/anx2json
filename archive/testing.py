from pprint import pprint
import xml.etree.ElementTree as ET
from anx_utilities import *


def main():
    knacklyToHotDocs2 = {
        # Client Specific Conditions
        "preparerName": parse_primitive("Loan Prepared By TE"),
        "preparerEmail": parse_primitive("Loan Prepared By Email TE"),
        "PreparerAddress": parse_primitive("Preparer Address MC"),
        "Preparer": parse_Address(
            "Loan Preparead By Street Address TE",
            "Loan Prepared By City TE",
            "Loan Prepared By State MC",
            "Loan Prepared By Zip Code TE",
        ),
        # Loan Information
        "loanTerms": {
            "closingDate": parse_primitive("Document Date DT"),
            "loanNumber": parse_primitive("Loan Number TE"),
            "loanAmount": parse_primitive("Loan Amount NU"),
            "loanTerm": parse_primitive("Loan Term NU"),
            "amortizationMonths": parse_primitive("Amortization Period NU"),
            "interestRate": parse_primitive("Interest Rate NU"),
            "defaultInterestRate": parse_primitive("Default Interest Rate NU"),
            "interestCalcType": parse_primitive("Interest Calc Type MC"),
            "interestOnlyMonths": parse_primitive(
                "Variable Interest Rate Interest Only Period NM"
            ),
            "isInterestOnly": parse_primitive("Loan Type Interest Only TF"),
            "isVariableRate": parse_primitive("Loan Type Variable TF"),
            "variableRate": {
                "margin": parse_primitive("Variable Margin NM"),
                "isDailyFloatingRate": parse_primitive("Rate Adjust Daily TF"),
                "changeDate": parse_primitive("Variable Change Date NU"),
                "armAdjustmentPeriod": parse_primitive(
                    "Variable ARM Adjustment Period NM"
                ),
                "firstInterestCap": parse_primitive("Variable First Interest Cap NM"),
                "subsequentInterestCap": parse_primitive(
                    "Variable Subsequent Interest Cap NM"
                ),
                "floorRate": parse_primitive("Variable Floor Rate NM"),
                "maximumInterestRateCap": parse_primitive(
                    "Variable Maximum interest Rate Cap NM"
                ),
                "interestRateIndex": parse_primitive("Variable Interest Rate Index MC"),
            },
            "isInterestStep": parse_primitive("Interest Step TF"),
            "interestStepSpreadsheet": parse_interestStepSpreadsheet(
                "Interest Step Duration NU", "Interest Step Rate NU"
            ),
        },
        "securityAndUCCDocs": {
            "isOwnershipPledge": parse_primitive("Membership Pledge TF"),
            "security_OwnershipSpreadsheet": parse_security_OwnershipSpreadsheet(
                "Membership Pledgor Name TE",
                "Membership Pledgor Ind TF",
                "Membership Pledgor Signer 1 TE",
                "Membership Pledgor Title TE",
                "Membership Pledgor State MC",
            ),
            "OwnershipAddress": parse_Address(
                "Pledgor Street Address TE",
                "Pledgor City TE",
                "Pledogr State MC",
                "Pledgor Zip TE",
            ),
            "isCollateralSecurity": parse_primitive("Collateral Security Agreement TF"),
            "isBlanketFiling": parse_primitive("UCC Personal Property TF"),
            "isBorrowerDebtor": parse_primitive("CSA Debtor TF"),
            "Security_CSADebtorSpreadsheet": parse_Security_CSADebtorSpreadsheet(
                "CSA Debtor Name TE",
                "CSA Debtor Ind TF",
                "CSA Debtor Signer 1 Title TE",
                "CSA Debtor Signer 1 TE",
                "CSA Debtor State MC",
            ),
            "CSADebtorAddress": parse_Address(
                "Debtor Street Address TE",
                "Debtor City TE",
                "Debtor State MC",
                "Debtor Zip TE",
            ),
            "isFixtureFiling": parse_primitive("UCC Fixture Filing TF"),
            "lenderUCCInformation": parse_lenderUCCInformation(
                "UCC Lender Name TE", "Lender Ind TF"
            ),
        },
        "lenderInformation": {
            "isExhibitALenders": parse_isExhibitALenders("Exhibit A Lender List TF"),
            "IsMultipleLenders": parse_primitive("seth_Multiple Lenders TF"),
            "IsCFLLicensee": parse_primitive("CA CFL License TF"),
            "MultipleLenders": parse_MultipleLenders(
                "Lender Name TE", "Lender Invest Amount NU"
            ),
        },
        "settlementFees": {  # Knackly includes a "paidTo" field that HD does not have, only for Other fees. How to account for this?
            "brokerFees": parse_FeesSpreadsheet(
                "Broker Fee NU",
                "Broker Fee Description TE",
                "Broker Delivery Fee Comment MC",
            ),
            "lenderFees": parse_FeesSpreadsheet(
                "Lender Fee NU",
                "Lender Fee Description TE",
                "Lender Delivery Fee Comment MC",
            ),
            "otherFees": parse_FeesSpreadsheet(
                "Other Fee NU",
                "Other Fee Description TE",
                "Other Delivery Fee Comment MC",
                "Other Paid To Fee TE",
            ),
            "geraciFee": parse_geraciFee("Geraci Fee NU"),
            "geraciFeeDelivery": parse_geraciFeeDelivery("Geraci Fee Delivery MC"),
            "perDiemInterestDelivery": parse_primitive("Per Diem interest Delivery MC"),
        },
        "docsAdd": {
            "isAssignmentOfPropertyManagement": parse_primitive(
                "Assignment of Property Management TF"
            ),
            "assignment_Spreadsheet_list": parse_assignment_Spreadsheet_list(
                "PDM Property DMC",
                "Property Manager TE",
                "Property Manager Signing DT",
                "Property Manager Street Address TE",
                "Property Manager City TE",
                "Property Manager State MC",
                "Property Manager Zip Code TE",
            ),
            "isW9": parse_primitive("W9 TF"),
            "isFirstPaymentLetter": parse_primitive("First Payment Letter TF"),
            "firstPaymentAmount": parse_primitive(
                "First Payment Letter Payment AMT NU"
            ),
            "isFirstPaymentIncludeEscrow": parse_primitive("Fay Escrow Reserves TF"),
            "isForSale": parse_primitive("seth_isForSale"),
            "loanSaleInformation": {
                "Assignee": parse_primitive("Assignee MC"),
                "whenSold": parse_primitive("Assignment and Allonge Concurrent MC"),
            },
            "isCollateralAssignment": parse_primitive("Collateral Assignment TF"),
            "isSubordinations": parse_isSubordinations("Loan Documents MC"),
            "subordinations_list": parse_subordinations_list(
                "Subordination Doc Type MC",
                "PDS Property DMC",
                "Subordination Post Closing TF",
                "Subordination Lease Document TE",
                "Subordination Lease Document DT",
                "Subordination Lease Months NU",
                "Tenant Name TE",
            ),
            "isIntercreditor": -999,  # Partially uses "Loan Documents MC" *select all that apply so its tricky*
            "intercreditorAgreements_list": {  # This needs to be an array as well!!!!!
                "repOptions": "Subordination Rep Options MC",
                "documentType": "Subordination Senior Doc Options MC",
                "documentRecording": "Subordination Existing Senior Doc MC",
                "debtAmount": "Subordinate Debt Amount NU",
                "recordingDate": "Junior Loan Recorded On DT",
                "signingDate": "Junior Loan Signing DT",
                "instrumentNumber": "Junior Loan Instrument Number TE",
                "trustor": "Junior Loan Trustor Name TE",
                "trustee": "Junior Loan Trustee TE",
                "address": {
                    "street": "Subordinate Lender Street Address TE",
                    "city": "Subordinate Lender City TE",
                    "state": "Subordinate Lender State MC",
                    "zip": "Subordinate Lender Zip Code TE",
                },
                "lenderSpreadsheet": {
                    "name": "Junior Loan Beneficiary TE",
                    "investedAmount": "Subordinate Lender Invest Amount NU",
                },
                "subordinateInterestRate": "Subordinate Interest Rate NU",
            },
            "isTranslator": parse_primitive("Translator Required TF"),
            "needsTranslator": {"values": ["Translator Required MC"], "_type": -999},
            "isAKA": parse_primitive("Borrower AKA Required TF"),
            "aka": {  # Update Knackly so that this includes the "Alternate name" text list
                "values": ["Borrower AKA Name MC", "Borrower AKA TX"],
                "_type": -999,
            },
        },
    }

    x = knacklyToHotDocs2
    pprint(x["docsAdd"]["subordinations_list"][3])


if __name__ == "__main__":
    main()

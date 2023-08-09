from testing import type_loan_documents_mc
from anx_utilities import *
from utilities import type_deferred_broker_type

knacklyToHotDocs2 = {
    # Client Specific Conditions
    "preparerName": parse_primitive("Loan Prepared By TE"),
    "preparerEmail": parse_primitive("Loan Prepared By Email TE"),
    "PreparerAddress": parse_primitive("Preparer Address MC"),
    "Preparer": parse_Address("Loan Preparead By Street Address TE", "Loan Prepared By City TE", "Loan Prepared By State MC", "Loan Prepared By Zip Code TE"),
    
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
        "interestOnlyMonths": parse_primitive("Variable Interest Rate Interest Only Period NM"),
        "isInterestOnly": parse_primitive("Loan Type Interest Only TF"),
        "isVariableRate": parse_primitive("Loan Type Variable TF"),
        "variableRate": {
            "margin": parse_primitive("Variable Margin NM"),
            "isDailyFloatingRate": parse_primitive("Rate Adjust Daily TF"),
            "changeDate": parse_primitive("Variable Change Date NU"),
            "armAdjustmentPeriod": parse_primitive("Variable ARM Adjustment Period NM"),
            "firstInterestCap": parse_primitive("Variable First Interest Cap NM"),
            "subsequentInterestCap": parse_primitive("Variable Subsequent Interest Cap NM"),
            "floorRate": parse_primitive("Variable Floor Rate NM"),
            "maximumInterestRateCap": parse_primitive("Variable Maximum interest Rate Cap NM"),
            "interestRateIndex": parse_primitive("Variable Interest Rate Index MC")
        },
        "isInterestStep": parse_primitive("Interest Step TF"),
        "interestStepSpreadsheet": parse_interestStepSpreadsheet("Interest Step Duration NU", "Interest Step Rate NU")
    },
    "features": {
        "isConstructionReserve": parse_primitive("Construction Holdback TF"),
        "construction": {
            "reserve": parse_primitive("Holdback Amount NU"),
            "IsNonDutch": parse_primitive("Non Dutch TF"),
            "Type": parse_primitive("Construction Type MC"),
            "IsRetainageRequired": parse_primitive("Retainage Required TF"),
            "IsExcludeSchedule": parse_primitive("Exclude Disbursement Schedule TF"),
            "IsThirdPartyFCA": parse_primitive("Construction Fund Control TF"),
            "inspectionFee": parse_primitive("Inspection Fee NU"),
            "isInspectionFee": parse_primitive("seth_Inspection Fee TF"),
            "IsConstructionContract": parse_primitive("Construction Contract TF"),
            "Contractor": parse_Address("Contractor Street Address TE", "Contractor City TE", "Contractor State MC", "Contractor Zip TE"),
            "Completion": parse_Completion("Construction Contract Percent NU", "Construction Contract Days NU"),
            "IsDesignContract": parse_primitive("Construction Design Contract TF"),
            "Designer": parse_Address("Designer Street Address TE", "Designer City TE", "Designer State MC", "Designer Zip TE"),
            "isThirdPartyConstructionGuaranty": parse_primitive("Guaranty of Completion TF"),
            "isAssigisBrokernmentOfPermits": parse_primitive("Assignment of Permits TF"),
            "completionGuarantors": parse_completionGuarantors("Construction Guaranty Name TX"),
        },
        "loanFeatures": {
            "IsTaxInsuranceImpounds": parse_primitive("Impound Accounts TF"),
            "TaxEscrowDollars": parse_primitive("Impound Tax NU"),
            "InsuranceEscrowDollars": parse_primitive("Impound Insurance NU"),
            "isACHRemove": parse_primitive("Remove ACH TF"),
            "isACH": parse_primitive("ACH Delivery of Payments TF"),
            "isSBALoan": parse_primitive("SBA Loan TF"),
            "isCannabisLoan": parse_primitive("Cannabis Loan TF"),
            "isAffiliateLoan": parse_primitive("Affiliate Loan TF"),
            "isSpecialPurposeEntity": parse_primitive("Special Purpose Entity TF"),
            "isAutoExtension": parse_primitive("Auto Extension TF"),
            "isDebtServiceCoverageRatio": parse_primitive("DSCR TF"),
            "ratio": parse_primitive("DSCR NU"),
            "isExtension": parse_primitive("Extension TF"),
            "extensionNum": parse_primitive("Extension Number NU"),
            "extensionMonths": parse_primitive("Extension Months NU"),
            "extensionType": parse_primitive("Extension Fee Type MC"),
            "extensionFeePercent": parse_primitive("Extension Fee NU"),
            "extensionFeeAmount": parse_primitive("Extension Fee Amount NU"),
            "sba_ApprovalDate": parse_primitive("SBA Approval DT"),
            "sba_LoanNumber": parse_primitive("SBA Loan Number TX"),
            "isRecycledSPE": parse_primitive("SPE Recycled TF"),
            "isLockbox": parse_primitive("Rental Income LockBox TF"),
            "lockbox_Type": parse_primitive("Rental Income Lockbox MC"),
            "lockbox_Bank": parse_primitive("Rental Income Lockbox Bank TE"),
            "lockbox_FirstRentDate": parse_primitive("Rental Income Lockbox DT"),
            "isServicingFees": parse_primitive("Servicing Fees TF"),
            "servicingFee": parse_primitive("Servicing Fees Amount NU"),
            "isExit": parse_primitive("Exit Fee TF"),
            "exitDollars": parse_primitive("Exit Fee Amount NU"),
            "isTermination": parse_primitive("Termination Fee TF"),
            "terminationDollars": parse_primitive("Termination Fee AMT NU"),
            "deferredBrokerType": type_deferred_broker_type, # LOOK AT THIS ONE ITS NOT CORRECT
            "deferredBrokerDollars": parse_primitive("Deferred Broker Fee NU"),
            "deferredBrokerPercent": parse_primitive("Deferred Broker Fee Percent NU"),
            "deferredOriginationType": parse_primitive("Deferred Origination Fees MC"),
            "deferredOriginationDollars": parse_primitive("Deferred Origination Fee NU"),
            "deferredOriginationPercent": parse_primitive("Deferred Origination Fee Percent NU")
        },
        "reserves": {
            "IsLender": parse_primitive("Lender Holdback TF"),
            "LenderDollars": parse_primitive("Lender Holdback NU"),
            "isPropertyTax": parse_primitive("Real Property Tax Holdback TF"),
            "PropertyTaxDollars": parse_primitive("Real Property Tax Holdback NU"),
            "isPropertyInsurance": parse_primitive("Insurance Holdback TF"),
            "PropertyInsuranceDollars": parse_primitive("Insurance Holdback NU"),
            "IsCapEx": parse_primitive("Capex Holdback TF"),
            "CapExDollars": parse_primitive("Capex Holdback NU"),
            "IsAppraisal": parse_primitive("Appraisal Reserve TF"),
            "AppraisalDollars": parse_primitive("Appraisal Reserve Amount NU"),
            "DefaultType": parse_primitive("Default Reserve MC"),
            "DefaultDollars": parse_primitive("Default Reserve Dollars NU"),
            "DefaultMonths": parse_primitive("Default Reserve Months NU"),
            "isOccupancy": parse_primitive("Damage Reserve TF"),
            "occupancyAmount": parse_primitive("Damage Reserve Amount NU"),
            "occupancyDeadline": parse_primitive("Damage Deadline DT"),
            "DebtServiceType": parse_DebtServiceType("Interest Reserve TF", "Interest Reserve Months TF"),
            "DebtServiceDollars": parse_primitive("Interest Reserve Amount NU"),
            "DebtServiceMonths": parse_primitive("Interest Reserve Months NU")
        }
    },
    "securityAndUCCDocs": {
        "isOwnershipPledge": parse_primitive("Membership Pledge TF"),
        "security_OwnershipSpreadsheet": parse_security_OwnershipSpreadsheet("Membership Pledgor Name TE", "Membership Pledgor Ind TF", "Membership Pledgor Signer 1 TE", "Membership Pledgor Title TE", "Membership Pledgor State MC"),
        "OwnershipAddress": parse_Address("Pledgor Street Address TE", "Pledgor City TE", "Pledogr State MC", "Pledgor Zip TE"),
        "isCollateralSecurity": parse_primitive("Collateral Security Agreement TF"),
        "isBlanketFiling": parse_primitive("UCC Personal Property TF"),
        "isBorrowerDebtor": parse_primitive("CSA Debtor TF"),
        "Security_CSADebtorSpreadsheet": parse_Security_CSADebtorSpreadsheet("CSA Debtor Name TE", "CSA Debtor Ind TF", "CSA Debtor Signer 1 Title TE", "CSA Debtor Signer 1 TE", "CSA Debtor State MC"),
        "CSADebtorAddress": parse_Address("Debtor Street Address TE", "Debtor City TE", "Debtor State MC", "Debtor Zip TE"),
        "isFixtureFiling": parse_primitive("UCC Fixture Filing TF"),
        "lenderUCCInformation": parse_lenderUCCInformation("UCC Lender Name TE", "Lender Ind TF"),
    },
    "lenderInformation": {
        "isExhibitALenders": parse_isExhibitALenders("Exhibit A Lender List TF"),
        "IsMultipleLenders": parse_primitive("seth_Multiple Lenders TF"),
        "IsCFLLicensee": parse_primitive("CA CFL License TF"),
        "MultipleLenders": parse_MultipleLenders("Lender Name TE", "Lender Invest Amount NU"), # This doesn't include CFL license for each lender because it isn't supported in HD
        "Lender": parse_Lender("Lender Name TE"),
        "CFLLicenseNumber": parse_primitive("Lender CFL License Number TE"),
        "NoticeTo": parse_primitive("Lender Care Of MC"),
        "Notice": parse_Address("Lender Street Address TE", "Lender City TE", "Lender State MC", "Lender Zip Code TE"),
        "closingContact": parse_primitive("Closing Contact Name TE"),
        "DeliveryTo": None, # Not sure where in HD this relates to... is it the Per Diem Interest Payable and Delivered to: dropdown?
        "noticeEmail": parse_primitive("Closing Contact Email Address TX")
    },
    "IsGuaranty": parse_primitive("Guarantor TF"),
    "Guarantor": {
        "AvailableTypes": parse_primitive("Guaranty Type MC", mc_as_list=True),
        "Guarantors": [None] # This needs to be looked at more closely. The Knackly page doesnt make sense to me.
        
    },
    "SelectServicer": parse_primitive("Loan Servicer MC"),
    "servicer": {
        "name": parse_primitive("Loan Servicer Name TE"),
        "contact": parse_Address("Loan Servicer Street Address TE", "Loan Servicer City TE", "Loan Servicer State MC", "Loan Servicer Zip TE"),
    },
    "isBroker": parse_primitive("CA Broker TF"),
    "broker": {
        "name": parse_primitive("CA Broker Name TE"),
        "licenseNumber": parse_primitive("CA Broker License Num TE"),
        "address": parse_Address("Broker Street Address TE", "Broker City TE", "Broker State MC", "Broker Zip Code TE"),
    },
    "titlePolicy": {
        "titleCompany": {
            "companyName": parse_primitive("Title Company Name TE"),
            "officerContactName": parse_primitive("Title Officer Name TE"),
            "address": parse_Address("Title Officer Street Address TE", "Title Officer City TE", "Title Officer State MC", "Title Zip Code"),
            "officerContactEmail": parse_primitive("Title Officer Contact Email TE")
        },
        "orderNumber": parse_primitive("Title Order Number TE"),
        "effectiveDate": parse_primitive("Title Report Effective Date DT"),
        "isReduceInsurance": parse_primitive("Title Insurance 100 TF"),
        "isProformaPolicy": parse_primitive("Proforma Policy TF"),
        "deletions": parse_primitive("Title Deletions TE"),
        "altaEndorsements": parse_primitive("ALTA Endorsements TE"),
        "version": parse_primitive("Title Policy Version MC")
    },
    "isEscrow": parse_isEscrow("Escrow and Title Select MC"),
    "escrow": {
        "companyName": parse_primitive("Escrow Company Name TE"),
        "officerContactName": parse_primitive("Escrow Officer TE"),
        "address": parse_Address("Escrow Officer Street Address TE", "Escrow Officer City TE", "Escrow Officer State MC", "Escrow Officer Zip Code TE"),
        "officerContactEmail": parse_primitive("Escrow Officer Contact Email TE")
    },
    "settlementFees": {
        "brokerFees": parse_FeesSpreadsheet("Broker Fee NU", "Broker Fee Description TE", "Broker Delivery Fee Comment MC"),
        "lenderFees": parse_FeesSpreadsheet("Lender Fee NU", "Lender Fee Description TE", "Lender Delivery Fee Comment MC"),
        "otherFees": parse_FeesSpreadsheet("Other Fee NU", "Other Fee Description TE", "Other Delivery Fee Comment MC", "Other Paid To Fee TE"),
        "geraciFee": parse_geraciFee("Geraci Fee NU"),
        "geraciFeeDelivery": parse_geraciFeeDelivery("Geraci Fee Delivery MC"),
        "perDiemInterestDelivery": parse_primitive("Per Diem interest Delivery MC")
    },
    "docsAdd": {
        "isAssignmentOfPropertyManagement": parse_primitive("Assignment of Property Management TF"),
        "assignment_Spreadsheet_list": parse_assignment_Spreadsheet_list("PDM Property DMC", "Property Manager TE", "Property Manager Signing DT", "Property Manager Street Address TE", "Property Manager City TE", "Property Manager State MC", "Property Manager Zip Code TE"),
        "isW9": parse_primitive("W9 TF"),
        "isFirstPaymentLetter": parse_primitive("First Payment Letter TF"),
        "firstPaymentAmount": parse_primitive("First Payment Letter Payment AMT NU"),
        "isFirstPaymentIncludeEscrow": parse_primitive("Fay Escrow Reserves TF"),
        "isForSale": parse_primitive("seth_isForSale"),
        "loanSaleInformation": {
            "Assignee": parse_primitive("Assignee MC"),
            "whenSold": parse_primitive("Assignment and Allonge Concurrent MC"),
        },
        "isCollateralAssignment": parse_primitive("Collateral Assignment TF"),
        "isSubordinations": parse_isSubordinations("Loan Documents MC"),
        "subordinations_list": parse_subordinations_list("Subordination Doc Type MC", "PDS Property DMC", "Subordination Post Closing TF", "Subordination Lease Document TE", "Subordination Lease Document DT", "Subordination Lease Months NU", "Tenant Name TE"),
        "isIntercreditor": -999, # Partially uses "Loan Documents MC" *select all that apply so its tricky*
        "intercreditorAgreements_list": { # This needs to be an array as well!!!!!
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
                "zip": "Subordinate Lender Zip Code TE"
            },
            "lenderSpreadsheet": {
                "name": "Junior Loan Beneficiary TE",
                "investedAmount": "Subordinate Lender Invest Amount NU"
            },
            "subordinateInterestRate": "Subordinate Interest Rate NU"
        },
        "isTranslator": parse_primitive("Translator Required TF"),
        "needsTranslator": {
            "values": ["Translator Required MC"],
            "_type": -999
        },
        "isAKA": parse_primitive("Borrower AKA Required TF"),
        "aka": { # Update Knackly so that this includes the "Alternate name" text list
            "values": ["Borrower AKA Name MC", "Borrower AKA TX"],
            "_type": -999
        }
    },
    "docsCustomize": {
        "isRemoveArbitrationProvisions": parse_primitive("Remove Arbitration TF"),
        "isRemoveLanguageCapacity": parse_primitive("Remove Language Capacity TF"),
        "isRemoveInitialLines": parse_primitive("No Footer Initials TF"),
        "isRemoveAllEntityCerts": parse_primitive("No Entity Certificates TF"),
        "isRemoveTitleInsurance": parse_primitive("No Title Policy TF"),
        "isCoverpage": parse_primitive("Signing Instructions TF"),
        "isMasterGuaranty": parse_primitive("Master Guaranty TF")
    },
    "perDiem365": -999,
    "showReviewChecklist": "Show Review Checklist TFCO", # This is a computation, so it won't actually show in the answer file. Something has to be done about that. Possible make a real TF component that stores the value but never gets asked, so it is accessible in the .anx file?
    "sanadaLastPayment": -999, # This is also a computation, would be nice if the value was stored in an un-asked question but stil saved to answer file.
    "scottsdaleInterestReserveAmount": -999, # Same as above
    "stronghillLockoutStepDate": -999, # Same as above, although are these supposed to be just calculated formulas that shouldnt ever be asked in the Knackly interview? idk 
    "LoanDocuments": type_loan_documents_mc(), # This isn't correct!!!
    "TestAmount": -999, # Not sure what this is for?
    "Certificate": {
        
    }
}

def main():
    pass

if __name__ == "__main__":
    main()
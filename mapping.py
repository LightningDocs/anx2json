hotdocsToKnackly = {
    "hd_borrower": "borrower",
    "hd_lender": "lender",
    "hd_loanAmount": "loanAmount",
    "hd_closingDate": "closingDate",
    "hd_goals": "goals",
    "hd_borrowerStreet": "borrower.address.street",
    "hd_borrowerCity": "address.city",
    "hd_borrowerZip": "address.zip",
    "hd_borrowerCounty": "address.county",
    "hd_borrowerState": "address.state",
    "hd_isExtraPayment": "isExtraPayment",
    "Borrower Owner Signer Underlying 1 Entity Type MC": "borrower.isIndividual"
}

knacklyToHotDocs = {
    "borrower": "hd_borrower",
    "lender": "hd_lender",
    "loanAmount": "hd_loanAmount",
    "closingDate": "hd_closingDate",
    "goals": "hd_goals",
    "address": {
        "street": "hd_borrowerStreet",
        "city": "hd_borrowerCity",
        "zip": "hd_borrowerZip",
        "county": "hd_borrowerCounty",
        "state": "hd_borrowerState"
    },
    "isExtraPayment": "hd_isExtraPayment"
}
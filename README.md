# anx2json
Python script that converts HotDocs .anx files to Knackly .json files

## Commands

### Usage

```bash
python main.py -i INPUT -o OUTPUT [-v] [-e EXCLUDE [EXCLUDE ...]]
```

The `-v` (verbose) flag can be provided to print the names of .anx components that were not used in construction of the output json.

The `-e` (exclude) argument can be provided alongside `-v` to specify certain .anx components to exclude from the verbose output. This can be passed through as a single argument, the path to a file where each line in the file is treated as a component to exclude, or as multiple strings, where each string is the name of a component to exclude.

### Examples

```bash
python main.py -i "my_loan.anx" -o "output.json"

python main.py -i "my_loan.anx" -o "output.json" -v

python main.py -i "my_loan.anx" -o "output.json" -v -e "exclusion.txt"

python main.py -i "my_loan.anx" -o "output.json" -v -e "Loan Documents MC" "ClientName" "(ANSWER FILE HISTORY)" 
```
## Todo list

- [ ] Section A
  - [ ] Borrower Information
  - [ ] Non-Borrower Property Owners
  - [ ] Property Information
- [ ] Section B
  - [x] Standard Loan Terms
  - [ ] Special Loan Features
  - [ ] Membership Pledge & UCC Documents
- [ ] Section C
  - [ ] Lender Information
  - [ ] Is there a Guaranty?
  - [ ] Guarantor Information
- [ ] Section D
  - [ ] Loan Servicer
  - [ ] Servicer Info
  - [ ] FCI Disbursement Agreement
  - [ ] Is there a Broker?
  - [ ] Broker
  - [ ] Title Information
  - [ ] Is there an escrow company?
  - [ ] Escrow Company Info
  - [ ] Settlement Statement Info
- [ ] Loan Preparer
- [ ] Closing Contact Info
- [ ] Optional Documents
  - [ ] Additional Documents
  - [ ] Customizations to Documents
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
  - [x] Special Loan Features
    - [x] Line of Credit
    - [x] Penalties
    - [x] Construction
    - [x] Loan Features
    - [x] Reserves
    - [x] Impounds
  - [ ] Membership Pledge & UCC Documents
- [ ] Section C
  - [x] Lender Information
  - [x] Is there a Guaranty?
  - [ ] Guarantor Information
- [x] Section D
  - [x] Loan Servicer
  - [x] Servicer Info
  - [x] FCI Disbursement Agreement
  - [x] Is there a Broker?
  - [x] Broker
  - [x] Title Information
  - [x] Is there an escrow company?
  - [x] Escrow Company Info
  - [x] Settlement Statement Info
- [x] Loan Preparer
- [x] Closing Contact Info
- [ ] Optional Documents
  - [ ] Additional Documents
  - [x] Customizations to Documents

## General clean-up
- Go back and remove most cases of `dict.update()` to instead use the `dict[key] = value` syntax, as it is more efficient and readable.
- Explore a `remove_false_values()` and/or `remove_null_values()` method to be called alongside `remove_none_values()` at the end of the json creation.
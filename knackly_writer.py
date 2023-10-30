from bson import ObjectId
from itertools import zip_longest
from pprint import pprint

from anx_parser import ANX_Parser


class Knackly_Writer:
    def __init__(self, anx_parser: ANX_Parser):
        self.anx = anx_parser
        self.json = {"id$": str(ObjectId())}
        self.uuid_map = {"Borrowers": {}}
        # In the uuid map for borrowers, the key will be the Borrower Name, and the value will be the generated uuid

    def remove_none_values(self, dictionary: dict) -> dict:
        """Recursively removes all occurrences of "None" within a dictionary

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

    def borrower_information(self) -> dict:
        """Creates the "Borrower" dictionary (on the top level of the Knackly interview)

        Returns:
            dict: The properly formatted "Borrower" dictionary
        """

        def borrower(
            name: str,
            entity_type: str,
            is_aif: bool,
            aif_name: str,
        ) -> dict:
            id_ = str(ObjectId())
            self.uuid_map["Borrowers"].update({name: id_})
            # First pass
            result = {
                "id$": id_,
                "BorrowerName": name,
                "BorrowerEntityType": entity_type,
                "IsBorrowerAIF": is_aif,
                "AIFName": aif_name,
            }

            # Second pass
            return result

        result = {
            "id$": str(ObjectId()),
            "Borrowers": [
                borrower(name, entity_type, is_aif, aif_name)
                for name, entity_type, is_aif, aif_name in zip_longest(
                    self.anx.parse_RptValue(self.anx.find_answer("Borrower Name TE"))[
                        :-1
                    ],
                    self.anx.parse_RptValue(
                        self.anx.find_answer("Borrower Entity Type MC")
                    )[:-1],
                    self.anx.parse_RptValue(
                        self.anx.find_answer("B signature attorney in fact TF")
                    ),
                    self.anx.parse_RptValue(
                        self.anx.find_answer("B signature attorney in fact name TX")
                    ),
                )
            ],
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

    def create(self) -> None:
        self.json["Borrower"] = self.borrower_information()

import xml.etree.ElementTree as ET
from datetime import datetime


class ANX_Parser:
    """Class with capabilities to parse HotDocs .anx files."""

    def __init__(self, infile):
        """Initialize the ANX_Parser with a provided file-like object

        Args:
            infile (file): The .anx file to be parsed.
        """
        self.tree = ET.parse(infile)
        self.answer_set = self.tree.getroot()

    def find_answer(self, name_tag: str) -> ET.Element:
        """Search for an element with a specific name tag in the XML tree.

        Args:
            name_tag (str): The name of the answer you want to find.

        Returns:
            Element: the Element object if found, otherwise None.
        """
        xpath = f"./Answer[@name='{name_tag}']"
        answer_element = self.answer_set.find(xpath)
        if answer_element is not None:
            answer_element.set("visited", "true")
            return answer_element[0]
        else:
            return None

    def parse_TextValue(self, element: ET.Element) -> str:
        """Parse the contents of a TextValue element in the .anx file.

        Args:
            element (ET.Element): The actual TextValue element object.

        Returns:
            str: The Knackly acceptable version of the text if present, otherwise None.
        """
        if element is None:
            return None
        # Raise an error if the element is not actually a TextValue element
        if element.tag != "TextValue":
            raise ANXTagError("TextValue", element.tag)
        elif "unans" in element.attrib:
            return None

        return element.text

    def parse_DateValue(self, element: ET.Element) -> str:
        """Parse the contents of a DateValue element in the .anx file.

        Args:
            element (ET.Element): The actual DateValue element object.

        Returns:
            str: The date as a string in the YYYY-MM-DD format that Knackly expects if present, otherwise None.
        """
        if element is None:
            return None
        # Raise an error if the element is not actually a DateValue element
        if element.tag != "DateValue":
            raise ANXTagError("DateValue", element.tag)
        elif "unans" in element.attrib:
            return None

        datetime_object = datetime.strptime(element.text, "%d/%m/%Y")
        return datetime_object.strftime("%Y-%m-%d")

    def parse_TFValue(self, element: ET.Element) -> bool:
        """Parse the contents of a TFValue element in the .anx file.

        Args:
            element (ET.Element): The actual TFValue element object.

        Returns:
            bool: The boolean value of the element's text if present, otherwise None.
        """
        if element is None:
            return None
        # Raise an error if the element is not actually a TFValue element
        if element.tag != "TFValue":
            raise ANXTagError("TFValue", element.tag)
        elif "unans" in element.attrib:
            return None

        return element.text == "true"

    def parse_NumValue(self, element: ET.Element) -> int | float:
        """Parse the contents of a NumValue element in the .anx file.

        Args:
            element (ET.Element): The actual NumValue element object.

        Returns:
            int | float: The integer (or float, if decimal places are relevant) value of the element's text if present, otherwise None.
        """
        if element is None:
            return None
        # Raise an error if the element is not actually a NumValue element
        if element.tag != "NumValue":
            raise ANXTagError("NumValue", element.tag)
        elif "unans" in element.attrib:
            return None

        f = float(element.text)
        if f.is_integer():
            return int(f)
        return f

    def parse_SelValue(self, element: ET.Element) -> str:
        """Parse the contents of a SelValue element in the .anx file. This is nearly identical to self.parse_TextValue().

        Args:
            element (ET.Element): The actual SelValue element object.

        Returns:
            str: The element's text if present, otherwise None.
        """
        if element is None:
            return None
        # Raise an error if the element is not actually a SelValue element
        if element.tag != "SelValue":
            raise ANXTagError("SelValue", element.tag)
        elif "unans" in element.attrib:
            return None

        return element.text

    def parse_MCValue(
        self, element: ET.Element
    ) -> str | int | float | list[str] | list[int] | list[float]:
        """Parse the contents of a MCValue element in the .anx file.

        Args:
            element (ET.Element): The actual MCValue element object.

        Raises:
            ANXTagError: _description_
            ValueError: _description_

        Returns:
            str | int | float | list[str] | list[int] | list[float]: More often than not will return a single value, but is capable of returning a list if the MCValue is a 'Select all that apply'
        """
        if element is None:
            return None
        # Raise an error if the element is not actually a MCValue element
        if element.tag != "MCValue":
            raise ANXTagError("MCValue", element.tag)
        elif "unans" in element.attrib:
            return None

        result = [self.parse_SelValue(child) for child in element]

        if len(element) == 1:
            return result[0]
        elif (
            len(element) > 1
        ):  # This doesn't happen often. Represents the "Select All that Apply"
            return result
        else:
            raise ValueError(
                f"`result` list is empty. This really shouldn't happen here."
            )

    def parse_Primitive(self, element: ET.Element) -> str | int | float:
        """Parse the contents of any primitive element type in the .anx file.
        Primitive element types are:
        - TextValue
        - DateValue
        - NumValue
        - TFValue
        - SelValue
        - MCValue

        Args:
            element (ET.Element): The actual element object.

        Returns:
            str | int | float: The parsed representation of the element if possible, otherwise None.
        """
        mapping = {
            "TextValue": self.parse_TextValue,
            "DateValue": self.parse_DateValue,
            "NumValue": self.parse_NumValue,
            "TFValue": self.parse_TFValue,
            "SelValue": self.parse_SelValue,
            "MCValue": self.parse_MCValue,
        }

        if element.tag not in mapping:
            raise ANXTagError(" | ".join(mapping.keys()), element.tag)
        return mapping[element.tag](element)

    def parse_RptValue(self, element: ET.Element) -> list:
        """Parse the contents of any RptValue element type in the .anx file.

        Args:
            element (ET.Element): The actual RptValue element object.

        Returns:
            list: The parsed representation of the element if possible, otherwise None.
        """
        if element is None:
            return None
        # Raise an error if the element is not actually a RptValue element
        if element.tag != "RptValue":
            raise ANXTagError("RptValue", element.tag)
        elif "unans" in element.attrib:
            return None

        # Recursively search through each sub element and call either parse_RptValue or parse_Primitive
        results = []
        for idx, child in enumerate(element):
            if child.tag == "RptValue":
                results.append(self.parse_RptValue(child))
            else:
                results.append(self.parse_Primitive(child))

        return results

    def parse_field(self, field_name: str):
        """Helper method that encapsulates finding and parsing an answer from the .anx file.

        Args:
            field_name (str): The name of the answer you want to parse. For example, "Cannabis Loan TF", or "Guarantor Name TE".

        Returns:
            list | str | int | float: The parsed representation of the element if possible, otherwise None.
        """
        element = self.find_answer(field_name)
        if element is None:
            return None

        if element.tag == "RptValue":
            return self.parse_RptValue(element)
        else:
            return self.parse_Primitive(element)

    def parse_multiple(self, *answers: str) -> list:
        """Helper method to parse multiple answers from the .anx file at once.

        Returns:
            list: A list where each element is the parsed representation of an answer if possible, otherwise None. If all elements are None, simply returns None.
        """
        result = [self.parse_field(answer) for answer in answers]
        if len(result) == 0:
            return None
        else:
            return result

    def get_unvisited_elements(
        self, excluded_elements: list[str] = None
    ) -> list[ET.Element]:
        """Get a list of all elements that have not been used / visited.

        Args:
            excluded_elements (list[str], optional): A list of all elements that you purposely don't care about the 'visitedness' of. Defaults to None.

        Returns:
            list[ET.Element]: A list of all elements that have not been used / visited.
        """
        if excluded_elements is None:
            excluded_elements = []

        unvisited_elements = []

        for element in self.answer_set:
            if (
                element.get("name") not in excluded_elements
                and element.get("visited") != "true"
            ):
                unvisited_elements.append(element)

        return unvisited_elements


class ANXTagError(Exception):
    """Error to be thrown when the xml tag of an element is not as expected"""

    def __init__(self, expected_tag: str, provided_tag: str) -> None:
        self.expected_tag = expected_tag
        self.provided_tag = provided_tag

    def __str__(self):
        return f"Expecting '{self.expected_tag}' element, but was provided '{self.provided_tag}' element"

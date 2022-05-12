""" This program prints a greeting to the user and asks for what they
want to do and does something according to the user's choice
"""
from enum import Enum

conversions = {"USD": 1, "EUR": 0.9, "CAD": 1.4, "GBP": 0.8,
               "CHF": 0.95,
               "NZD": 1.66, "AUD": 1.62, "JPY": 107.92}
home_currency = ""
filename = './AB_NYC_2019.csv'


class Categories(Enum):
    """An Enum class that has the attributes of location and property
    type
    """
    LOCATION = 0
    PROPERTY_TYPE = 1


class Stats(Enum):
    """An Enum class that has the attributes of min, max, and avg"""
    MIN = 0
    AVG = 1
    MAX = 2


class DataSet:
    """This class creates a copyright and header for the data"""
    copyright = "No copyright has been set"

    def __init__(self, header=""):
        """This constructor creates a new Dataset object"""
        try:
            self.header = header
        except ValueError:
            self._header = ""
        self._data = None
        self._labels = {Categories.LOCATION: set(),
                        Categories.PROPERTY_TYPE: set()}
        self._active_labels = {Categories.LOCATION: set(),
                               Categories.PROPERTY_TYPE: set()}

    def _initialize_sets(self):
        """Initializes the labels and active labels"""
        if not self._data:
            raise self.EmptyDatasetError
        for data in self._data:
            self._labels[Categories.LOCATION].add(data[0])
            self._labels[Categories.PROPERTY_TYPE].add(data[1])
            self._active_labels[Categories.LOCATION].add(data[0])
            self._active_labels[Categories.PROPERTY_TYPE].add(data[1])

    def display_cross_tables(self, state: Stats):
        """Displays a table of either min, max, and avg data"""

        if not self._data:
            raise self.EmptyDatasetError
        list_of_locations = list(self._active_labels[
                                     Categories.LOCATION])
        list_of_property_types = list(self._active_labels[
                                          Categories.PROPERTY_TYPE])
        table = "\t\t\t\t"
        for property_type in list_of_property_types:
            table += f"{property_type}\t"

        table += "\n"
        for location in list_of_locations:
            table += f"{location}" + ("\t" *
                             (((16 - len(location)) // 4) +
                              (1 if len(location) % 4 != 0 else 0)))
            for property_type in list_of_property_types:
                try:
                    rents = self._cross_table_statistics(location,
                                                         property_type)[
                        state.value
                    ]
                    table += f"$ {rents:.2f}" + ("\t" *
                             (((16 - len(f"$ {rents:.2f}")) // 4) +
                              (1 if len(f"$ {rents:.2f}") % 4 != 0
                               else 0)))
                except DataSet.NoMatchingItems:
                    table += f"$ N/A\t\t\t"
            table += "\n"
        print(table)
        print("")

    @property
    def header(self):
        """This method gets the header of the Database object"""
        return self._header

    @header.setter
    def header(self, value):
        """This method sets the header of the Database object"""
        if isinstance(value, str) and len(value) <= 30:
            self._header = value
        else:
            raise ValueError

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        """ Filters out data depending on the users choice and
        calculates the min, max, and average rent
        """
        if self._data is None:
            raise DataSet.EmptyDatasetError("The dataset is empty")
        found_data = [data for data in self._data if data[0] ==
                      descriptor_one and data[1] == descriptor_two]

        if len(found_data) == 0:
            raise DataSet.NoMatchingItems("Found no items matching "
                                          "your search")

        rents = [int(data[2]) for data in found_data]
        return min(rents), sum(rents) / len(rents), max(rents), \
               len(found_data)

    def load_default_data(self):
        """Loads a dataset and stores it into the dataset variable"""
        self._data = [
            ("Staten Island", "Private room", "70"),
            ("Brooklyn", "Private room", "50"),
            ("Bronx", "Private room", "40"),
            ("Brooklyn", "Entire home/apt", "150"),
            ("Manhattan", "Private room", "125"),
            ("Manhattan", "Entire home/apt", "196"),
            ("Brooklyn", "Private room", "110"),
            ("Manhattan", "Entire home/apt", "170"),
            ("Manhattan", "Entire home/apt", "165"),
            ("Manhattan", "Entire home/apt", "150"),
            ("Manhattan", "Entire home/apt", "100"),
            ("Brooklyn", "Private room", "65"),
            ("Queens", "Entire home/apt", "350"),
            ("Manhattan", "Private room", "98"),
            ("Brooklyn", "Entire home/apt", "150"),
            ("Brooklyn", "Entire home/apt", "200"),
            ("Brooklyn", "Private room", "99"),
            ("Brooklyn", "Private room", "120")
        ]
        self._initialize_sets()

    def get_labels(self, category: Categories):
        """Returns a list of the labels"""
        return list(self._labels[category])

    def get_active_labels(self, category: Categories):
        """Returns a list of the active labels"""
        return list(self._active_labels[category])

    def _table_statistics(self, row_category: Categories, label: str):
        """Prints a table of the minimum, average, and maximum labels
        that matches the category"""
        if self._data is None:
            raise self.EmptyDatasetError
        list_of_other_category = self.get_active_labels(Categories.
                                                        LOCATION) \
            if row_category == Categories.PROPERTY_TYPE \
            else self.get_active_labels(Categories.PROPERTY_TYPE)

        data = []
        if row_category == Categories.PROPERTY_TYPE:
            for category in list_of_other_category:
                try:
                    data.append(self._cross_table_statistics(category,
                                                             label))
                except self.NoMatchingItems:
                    pass
        else:
            for category in list_of_other_category:
                try:
                    data.append(self._cross_table_statistics(label,
                                                             category))
                except self.NoMatchingItems:
                    pass
        minimum, average, maximum, _ = data[0]
        for part_of_data in data:
            mi, sub_average, ma, added_values = part_of_data
            minimum = min(mi, minimum)
            average += (sub_average * added_values)
            maximum = max(ma, maximum)
        return minimum, average / sum([length[3] for length in data]),\
               maximum

    def display_field_table(self, rows: Categories):
        """Displays a table of the minimum, maximum, average for each
        item in a category"""
        list_of_rows = self.get_active_labels(rows)

        table = "\t\t\t\t\tMinimum\t\t\tAverage\t\t\tMaximum\n"
        for row in list_of_rows:
            table += str(row) + ("\t" * (((20 - len(str(row))) // 4) +
                                         (1 if len(str(row)) % 4 != 0
                                          else 0)
                                         ))
            for value in self._table_statistics(rows, row):
                if value is None:
                    table += "N/A\t\t\t\t\t"
                    continue
                str_to_add = f"$ {value:.2f}"
                table += str_to_add + ("\t" *
                                       (((16 - len(str_to_add)) // 4) +
                                       (1 if len(str_to_add) % 4 != 0
                                        else 0)))
            table += "\n"

        print(table)

    def toggle_active_label(self, category: Categories,
                            descriptor: str):
        """Adds or removes labels from active labels"""
        if descriptor not in self._labels[category]:
            raise KeyError
        if descriptor not in self._active_labels[category]:
            self._active_labels[category].add(descriptor)
        else:
            self._active_labels[category].remove(descriptor)

    def load_file(self):
        """Reads and parses a file and loads it into dataset"""
        file = open(filename)
        file_list = file.readlines()
        headers = file_list[0]
        self._data = [lst.split(",")[1:] for lst in file_list[1:]]
        print(str(len(file_list[1:])) + " lines have been loaded")
        self._initialize_sets()

    class EmptyDatasetError(Exception):
        """An exception that will be raised when no dataset is loaded"""
        pass

    class NoMatchingItems(Exception):
        """ An exception that will be raised if there is no data that
        matches data in the dataset
        """
        pass


def manage_filters(dataset: DataSet, category: Categories):
    """Allows the user to change active labels"""
    while True:
        print("The following labels are in the dataset:")
        labels = dataset.get_labels(category)
        active_labels = dataset.get_active_labels(category)
        i = 1
        for label in labels:
            print(f"{i}: {label}" + ("\t" * ((20 - len(label)) // 4)),
                  end="")
            print('ACTIVE' if label in active_labels else 'INACTIVE')
            i += 1
        try:
            label_to_toggle = input("Please select an item to toggle"
                                        " or enter a blank line when you"
                                        " are finished.")
            if label_to_toggle == "":
                break
            dataset.toggle_active_label(category, labels[
                int(label_to_toggle) - 1])
        except ValueError:
            print("Please only enter a number from the list above.")
        except IndexError:
            print("Please only enter a number from the list above.")


def print_menu():
    """ Prints the main menu for the user"""
    print("Main Menu")
    print("1 - Print Average Rent by Location and Property Type")
    print("2 - Print Minimum Rent by Location and Property Type")
    print("3 - Print Maximum Rent by Location and Property Type")
    print("4 - Print Min/Avg/Max by Location")
    print("5 - Print Min/Avg/Max by Property Type")
    print("6 - Adjust Location Filters")
    print("7 - Adjust Property Type Filters")
    print("8 - Load Data")
    print("9 - Quit")


def currency_option(base_curr):
    """Creates and prints a table of currency conversions"""
    table_curr = ""
    for i in range(len(conversions) + 2):
        if i == 0:
            table_curr += f"{base_curr}\t\t"
        else:
            table_curr += f"{i * 10:.2f}\t"
        for new_curr in conversions:
            if new_curr == base_curr:
                continue
            if i == 0:
                table_curr += f"{new_curr}\t\t"
            else:
                table_curr += \
                    f"{currency_converter(i * 10, base_curr, new_curr):.2f}\t"
        table_curr += "\n"
    print(table_curr)


def currency_converter(quantity, source_curr, target_curr):
    """Takes a currency and does a currency conversion to a different
    currency"""
    if quantity <= 1:
        return "Quantity should be greater than 1"
    result_curr = quantity / conversions[source_curr]
    result_curr = result_curr * conversions[target_curr]
    return result_curr


def test_cross_table_stats(dataset, borough, room_type,
                           raisesEmpty=False, raisesNoMatch=False):
    """ Checks whether the cross statistics method in the dataset
    class works and returns pass or fail
    """
    try:
        dataset._cross_table_statistics(borough, room_type)
        return "Pass"

    except Exception as e:
        if raisesEmpty:
            return "Pass" if isinstance(e, DataSet.EmptyDatasetError) \
                else "Fail"
        if raisesNoMatch:
            return "Pass" if isinstance(e, DataSet.NoMatchingItems) \
                else "Fail"
        return "Fail"


def unit_test():
    """ Tests the cross table statistics and load data methods in
    Class DataSet
    """
    my_set = DataSet()
    print("Testing _cross_table_statistics")
    print("Method Raises EmptyDataSet Error: " +
          test_cross_table_stats(my_set, "Manhattan", "Private room",
                                 raisesEmpty=True))
    my_set.load_default_data()
    print("Invalid Property Type Raises NoMatchingItems Error: " +
          test_cross_table_stats(my_set, "Manhattan", "Apartment",
                                 raisesNoMatch=True))
    print("Invalid Borough Raises NoMatchingItems Error: " +
          test_cross_table_stats(my_set, "Los Angeles", "Private room",
                                 raisesNoMatch=True))
    print("No Matching Rows Raises NoMatchingItems Error: " +
          test_cross_table_stats(my_set, "Queens", "Private room",
                                 raisesNoMatch=True))
    print("One Matching Row Returns Correct Tuple: " +
          test_cross_table_stats(my_set, "Queens", "Entire home / apt"))
    print("One Matching Row Returns Correct Tuple: " +
          test_cross_table_stats(my_set, "Brooklyn", "Private room"))


def menu(dataset):
    """ Prints the main menu, checks what the user wants to do, and does
    things according to the choice
    """
    global home_currency
    home_currency = input("What is your home currency? ")
    while home_currency not in conversions:
        home_currency = input("What is your home currency? ")
    print("Options for converting from " + home_currency + ": ")
    currency_option(home_currency)

    print(DataSet.copyright)
    user_uses_database = True
    while user_uses_database:
        print(dataset.header)
        print_menu()
        try:
            users_choice = int(input("What is your choice? "))
        except ValueError:
            print("Please enter a number only")
            continue
        try:
            if users_choice == 1:
                dataset.display_cross_tables(state=Stats.AVG)
            elif users_choice == 2:
                dataset.display_cross_tables(state=Stats.MIN)
            elif users_choice == 3:
                dataset.display_cross_tables(state=Stats.MAX)
            elif users_choice == 4:
                dataset.display_field_table(Categories.LOCATION)
            elif users_choice == 5:
                dataset.display_field_table(Categories.PROPERTY_TYPE)
            elif users_choice == 6:
                manage_filters(dataset, Categories.LOCATION)
            elif users_choice == 7:
                manage_filters(dataset, Categories.PROPERTY_TYPE)
            elif users_choice == 8:
                print("Loading Data...")
                dataset.load_file()
                print("Data successfully loaded")
            elif users_choice == 9:
                print("Goodbye!!! Thank you for using Foothill's "
                      "database project!!!")
                break
            else:
                print("Please enter a number between 1 and 9")

        except DataSet.EmptyDatasetError:
            print("Sorry an Error Occurred")
            print("Error: Data not loaded - Data is Empty")


def main():
    """ Obtain the users name, prints a greeting to the user, and prints
    the main menu
    """
    DataSet.copyright = "copyright Tanvi Waghela"
    air_bnb = DataSet()

    while True:
        try:
            air_bnb.header = input("Enter a header for the menu: ")
            break
        except ValueError:
            pass

    print("")
    name = input("Please enter your name: ")
    greeting = "Hi " + name + ", welcome to Foothill's database " \
                              "project."
    print(greeting)
    menu(air_bnb)


if __name__ == "__main__":
    main()

"""
--- Sample Output ---
Enter a header for the menu: Airbnb Final Database

Please enter your name: Tanvi
Hi Tanvi, welcome to Foothill's database project.
What is your home currency? USD
Options for converting from USD: 
USD		EUR		CAD		GBP		CHF		NZD		AUD		JPY		
10.00	9.00	14.00	8.00	9.50	16.60	16.20	1079.20	
20.00	18.00	28.00	16.00	19.00	33.20	32.40	2158.40	
30.00	27.00	42.00	24.00	28.50	49.80	48.60	3237.60	
40.00	36.00	56.00	32.00	38.00	66.40	64.80	4316.80	
50.00	45.00	70.00	40.00	47.50	83.00	81.00	5396.00	
60.00	54.00	84.00	48.00	57.00	99.60	97.20	6475.20	
70.00	63.00	98.00	56.00	66.50	116.20	113.40	7554.40	
80.00	72.00	112.00	64.00	76.00	132.80	129.60	8633.60	
90.00	81.00	126.00	72.00	85.50	149.40	145.80	9712.80	

copyright Tanvi Waghela
Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 1
Sorry an Error Occurred
Error: Data not loaded - Data is Empty
Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 8
Loading Data...
48895 lines have been loaded
Data successfully loaded
Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 1
				Entire home/apt	Private room	Shared room	
Manhattan		$ 249.24		$ 116.78		$ 88.98			
Bronx			$ 127.51		$ 66.79			$ 59.80			
Staten Island	$ 173.85		$ 62.29			$ 57.44			
Queens			$ 147.05		$ 71.76			$ 69.02			
Brooklyn		$ 178.33		$ 76.50			$ 50.53			


Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 2
				Entire home/apt	Private room	Shared room	
Manhattan		$ 0.00			$ 10.00			$ 10.00			
Bronx			$ 28.00			$ 0.00			$ 20.00			
Staten Island	$ 48.00			$ 20.00			$ 13.00			
Queens			$ 10.00			$ 10.00			$ 11.00			
Brooklyn		$ 0.00			$ 0.00			$ 0.00			


Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 3
				Entire home/apt	Private room	Shared room	
Manhattan		$ 10000.00		$ 9999.00		$ 1000.00		
Bronx			$ 1000.00		$ 2500.00		$ 800.00		
Staten Island	$ 5000.00		$ 300.00		$ 150.00		
Queens			$ 2600.00		$ 10000.00		$ 1800.00		
Brooklyn		$ 10000.00		$ 7500.00		$ 725.00		


Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 4
					Minimum			Average			Maximum
Manhattan			$ 0.00			$ 196.89		$ 10000.00		
Bronx				$ 0.00			$ 87.61			$ 2500.00		
Staten Island		$ 13.00			$ 115.28		$ 5000.00		
Queens				$ 10.00			$ 99.54			$ 10000.00		
Brooklyn			$ 0.00			$ 124.39		$ 10000.00		

Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 5
					Minimum			Average			Maximum
Entire home/apt		$ 0.00			$ 211.80		$ 10000.00		
Private room		$ 0.00			$ 89.79			$ 10000.00		
Shared room			$ 0.00			$ 70.20			$ 1800.00		

Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 6
The following labels are in the dataset:
1: Manhattan		ACTIVE
2: Bronx			ACTIVE
3: Staten Island	ACTIVE
4: Queens			ACTIVE
5: Brooklyn			ACTIVE
Please select an item to toggle or enter a blank line when you are finished.2
The following labels are in the dataset:
1: Manhattan		ACTIVE
2: Bronx			INACTIVE
3: Staten Island	ACTIVE
4: Queens			ACTIVE
5: Brooklyn			ACTIVE
Please select an item to toggle or enter a blank line when you are finished.3
The following labels are in the dataset:
1: Manhattan		ACTIVE
2: Bronx			INACTIVE
3: Staten Island	INACTIVE
4: Queens			ACTIVE
5: Brooklyn			ACTIVE
Please select an item to toggle or enter a blank line when you are finished.
Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 5
					Minimum			Average			Maximum
Entire home/apt		$ 0.00			$ 213.36		$ 10000.00		
Private room		$ 0.00			$ 90.72			$ 10000.00		
Shared room			$ 0.00			$ 70.88			$ 1800.00		

Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 6
The following labels are in the dataset:
1: Manhattan		ACTIVE
2: Bronx			INACTIVE
3: Staten Island	INACTIVE
4: Queens			ACTIVE
5: Brooklyn			ACTIVE
Please select an item to toggle or enter a blank line when you are finished.

Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? Please enter a number only
Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 7
The following labels are in the dataset:
1: Entire home/apt	ACTIVE
2: Private room		ACTIVE
3: Shared room		ACTIVE
Please select an item to toggle or enter a blank line when you are finished.
Airbnb Final Database
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Print Min/Avg/Max by Location
5 - Print Min/Avg/Max by Property Type
6 - Adjust Location Filters
7 - Adjust Property Type Filters
8 - Load Data
9 - Quit
What is your choice? 9
Goodbye!!! Thank you for using Foothill's database project!!!
"""

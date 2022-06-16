# Importing the CSV module which i will be using when reading from file
import csv

# Defining a class with methods and attributes to create/display and manipulate nodes for a Organisational structure.
class Organisational_Structure_TreeNode:
    def __init__(self,em_uin,em_name,em_role):
        self.em_uin = em_uin
        self.em_name = em_name
        self.em_role = em_role
        self.manages_list = []
        self.parent = None
        
    # set_role defines value for role attribute of given node. Uses encapsulation. 
    def set_role(self,role):
        self.em_role = role

    # append_child creates biderectional relationships between manager and their employees.
    def append_child(self,child): 
        child.parent = self
        self.manages_list.append(child)

    # method displays name and business title of child nodes. 
    def print_manages_list(self):
        print("\nManages:")
        for employees in self.manages_list:
            print(employees.em_name, "-", employees.em_role)
             
    # method displays relevant data of current node.
    def display_employee_data(self):
        print("\nName:", self.em_name)
        print("Employee Unique Identifier:", self.em_uin)
        print("Job Title:", self.em_role)
        print("Manager:",self.parent.em_name)
        self.print_manages_list()
        print("\n")

# Defining a clasee with methods and attributes that builds/accesses a tree structure.
# Instances of these classes are used to search for employees and job roles efficiently.
# Suitable nodes point to a memory location which hold all information of the employee.
class Searching_TreeNode:
    def __init__(self,character,em_info):
        self.character = character
        self.children = {}
        self.em_info = []

    # Method creates bidirectional relationship between consecutive charecters of a name.
    # E.g if name is Mark. M is parent class of a. A is parent class of r etc.
    def set_child(self,child_node):
        child_node.parent = self

    # Method used to search for a child component of a node.
    # If child component not found, then it creates one, thus building a tree
    def build_tree(self,character):
        if (character not in self.children):
            character_node = Searching_TreeNode(character,None)
            self.children[character] = character_node
        return self.children[character]

    # Method used to check if a node is a child of the self parent class.
    # Used to traverse the tree and find names on the tree. If not found, returns false
    def traverse_tree(self,character):
        if (character in self.children):
            current_node = self.children[character]
            return current_node
        else:
            return False
    # Recursive function to find all possible employees beneath a specific node.
    # employee info is saved on the last character of the name. If a name is entered
    # which doesn't have a child compononent, recursion is used to find all valid child
    # componenets and append the memory location of the employee to a list which is
    # returned to where the method is called.
    def display_all_children(self, list_of_data = []):
        for child in self.children:
            current_node = self.children[child]
            if current_node.em_info:
                list_of_data.append(current_node.em_info)
            current_node.display_all_children(list_of_data)
        return list_of_data

    #  Used to append pointer of the employee node to the last character in the seacrch tree.        
    def set_em_info(self,info):
        self.em_info.append(info)
    #Used to retrieve location of employee info which can be used to print all relevant data later.
    def get_em_info(self):
        return (self.em_info)

                            
#Multiple roots found in data, to find the approriate person we use the business_title of 'Chairman.'
#  This returns the root node ( start) of the organisation structure.
def finding_root():
    for node in uin_dict.values():
        if node.em_role == "Chairman":
            return node

# Building a tree with employee's name for a more efficient searching algorithm.
# Tree points to a node in the organisational tree to access details of employees.
def Building_Search_Tree(name,employee_node,root):
    current_node = root
    char_data_name = list(name)
    for character in char_data_name:
        current_node = current_node.build_tree(character)
    current_node.set_em_info(employee_node)


# Function to search through the name tree structure and provide details of the BT Employee.
# Initially, string split into individual characters for name search tree.
# Theres two cases within function which is determined by Searching_role - whether an employee
#  is being searched or if a business role is being searched. Both use this function.
#  method traverse_tree is called from Searching_TreeNode class. Returned value is parsed to display correct info.
def Traversing_Search_Tree(name, root_node):
    character_list = list(name.upper())
    current_node = root_node

    if root_node == role_root:
        Searching_role = True
    else:
        Searching_role = False
    
    for character in character_list:
        if current_node!= False:
            current_node = current_node.traverse_tree(character)

    # If False is passed from traverse tree method then employee/role not found and function ends.
    if current_node == False:
        if Searching_role:
            print("\nThis role doesnt exist")
        else:
            print("\nThe person is not employed to BT")

        print("Returning to the main menu\n")

        
    # The following section of code handles the input and returns a list of job roles or names the user may have meant
    #  Acts like google when it reccomends what you meant. For e.g If i search software, the program returns all job roles
    #  that begin with software like software engineer or software architect etc.
    elif not current_node.em_info and current_node != False:
        list_of_data = current_node.display_all_children(list_of_data = [])
        possible_search_validation = True
        print(name, "not found in the database, did you mean:\n")

        counter = 0
        suggested_list = []
        suggested_dict = {}
        for _list in list_of_data:
            for node in _list:
                if not Searching_role:
                    suggested_list.append(node)
                else:
                    node.em_role = node.em_role.upper()
                    if (node.em_role in suggested_dict) == False:
                        suggested_dict[str(node.em_role)] = [node]
                    else:
                        suggested_dict[str(node.em_role)].append(node)
                
        if Searching_role:
            for role, list_of_employees in suggested_dict.items():
                    print(counter, role)
                    suggested_list.append(role)
                    counter += 1

        else:
            for node in suggested_list:
                print(counter, node.em_name, '-', node.em_uin)
                counter += 1

        # Following code uses validation and ensures that the user only enters in the format the program asks for.
        #  e.g if a integer is required makes sure string isnt input etc. Program returns suggestions in a list ongside numbers
        #  The number needs to be entered to display info about the job role or the employee rather than the name.
        while possible_search_validation == True:
            if Searching_role == True:
                data_type = "business role"
            else:
                data_type = "employee"
                
            while True:
                try:
                    user_inp = int(input(f"Please select the number associated with the {data_type}  you meant or '9999' to return to the menu: "))
                    break
                except:
                    print("That's not a valid option")
                    
            if user_inp == 9999 :
                possible_search_validation = False

 
            elif user_inp < len(suggested_list) and user_inp >= 0:
                possible_search_validation = False
                current_node_list = []
                if Searching_role:
                    role = suggested_list[user_inp]
                    current_node_list = suggested_dict[role]
                    displaying_role_search_info(current_node_list,role)   

                else:
                    current_node_list.append(suggested_list[user_inp])
                    displaying_name_search_info(current_node_list)
            else:
                print("That's not a valid option")
                
     # Block of code used if the name the person searched for is a suitable name. Points to a function which displays
     #  Information about the name or the role user is searching for.
    else:
        current_node_list = current_node.get_em_info()
        print("Your search came with the following results:\n")
        if Searching_role:
             displaying_role_search_info(current_node_list,name)
        else:
            displaying_name_search_info(current_node_list)
        
#  Function used to display information of a role searched like who works as the role and the total count.
def displaying_role_search_info(current_node, name):
    counter = 0
    print("\n")
    for x in current_node:
        counter += 1
        print(x.em_name, "-", x.em_uin)

    print("~~~~~~~~~~~~~~~~~~~~")
    print("Total",name,":",counter)
    print("~~~~~~~~~~~~~~~~~~~~")

#  Function used to display information about the employee searched. Incorporates other functions to display
#  organisational tree and uses method called display_employee_data to siplay all data of the employee
def displaying_name_search_info(current_node):
    for x in current_node:
        x.display_employee_data()
        print("Direct and Indirect Children Tree:")
        printing_organisational_tree(x,writeToFile = False, createNewFile = False)

# Recursive algorithm which calls itself to print a hireachy structure.
# Algorithm prints all employees below a given 'root' parameter.
#  If organisational structure, tree is printed to file otherwise its printed to console.
def printing_organisational_tree(root, writeToFile, createNewFile, level = 0, markerStr = "+- ", levelMarkers=[]):

    emptyStr = " "*len(markerStr)
    connectionStr = "|" + emptyStr[:-1]

    level = len(levelMarkers)
    mapper = lambda draw: connectionStr if draw else emptyStr
    markers = "".join(map(mapper, levelMarkers[:-1]))
    markers += markerStr if level > 0 else ""

    if writeToFile == True:
        if createNewFile == True:
            f = open("Organisational_chart.txt","w")
            createNewFile = False
        else:
            f = open("Organisational_Chart.txt", "a")
        f.write(f"{markers}{root.em_name}\n")
        f.close()
    else:
        print(f"{markers}{root.em_name}")

    for i, child in enumerate(root.manages_list):
        isLast = i == len(root.manages_list) - 1
        printing_organisational_tree(child, writeToFile, createNewFile, level, markerStr, [*levelMarkers, not isLast])

 
 # Code for the main menu of the program which calls itself until its exited by pressing 'q'
 # Used to navigate around the application and perform different functions.
 # Once function is performed, the menu is displayed again until q is pressed to quit.
 #Validation is used to ensure only answers the program is looking for is pressed by user
def menu():
    print("************************************************")
    print("Hello and welcome to BT's organisation directory")
    print("************************************************\n")

    exit_program = False

    while exit_program != True:
        print("---------------------------------------------------------")
        print("Please select an option by typing the charecter indicated")
        print("A. Search an employee in the database")
        print("B. Print tree of all employees in BT")
        print("C. Search employees by business role")
        print("Q. Exit Program")
        print("---------------------------------------------------------\n")

        user_input = input("Please type 'A' , 'B' , 'C'  or 'Q': \n")

        if user_input.upper() == "A":
            name_search = input("Please enter the name you would like to search: ")
            Traversing_Search_Tree(name_search, name_root)

        elif user_input.upper() == "B":
            org_root = finding_root()
            writeToFile = True
            createNewFile = True
            printing_organisational_tree(org_root,writeToFile,createNewFile)

        elif user_input.upper() == "C":
            role_search = input("Please enter the business role you would like to search: ")
            Traversing_Search_Tree(role_search, role_root)
            

        elif user_input.upper() == "Q":
            exit()

        else:
            print("That's not a valid option")
            
# uin_dict contains a unique identifier (emplooyee uin) and memory location of the node.
#  Used to map connection between employees that have been read from file and their position in the org structure
uin_dict = {}

# The following block of code is used to read through a csv file and import the relevant data into memory location.
# File is read and three trees are created: tree to search name, search job role and  organisational tree of employees in BT.


# The two roots are starting points of the name search and role search trees. All nodes are direct and indirect children of these
#  for the searching algorithm.
name_root = Searching_TreeNode("root",None)
role_root = Searching_TreeNode("JobTitleRoot",None)

#  FIle is open and read, nodes in the org  structure is created and thesyre placed in the uin dictionary.
with open("UniDirectory.csv",newline = '')as csvfile:
    line = csv.reader(csvfile, delimiter=',',quotechar = '"')
    for column in line:
        employee_uin = (column[0])
        name = column[5]
        business_title = column[16]
        manager_uin = (column[23])
        manager_name = (column[24])
        manager_title = ""
        if employee_uin != "0":
            if (employee_uin in uin_dict):
                employee_node = uin_dict[employee_uin]
                employee_node.set_role(business_title)
                
            else:
                employee_node = Organisational_Structure_TreeNode(employee_uin,name,business_title)
                uin_dict[employee_uin] = employee_node
                
            if (manager_uin != "0"):
                if (manager_uin in uin_dict):
                    manager_node = uin_dict[manager_uin]
                else:
                    manager_node = Organisational_Structure_TreeNode(manager_uin,manager_name,manager_title)
                    uin_dict[manager_uin] = manager_node

                # PArent child relation created here throught the use of the append child method.
                if manager_node != employee_node:
                    manager_node.append_child(employee_node)

            #  The two trees used for searching are built with these lines of code which pass on nodes with relevant
            # information to different functions above which actually build the tree itself.
            # to different functions
            Building_Search_Tree(name.upper(),employee_node,name_root)
            Building_Search_Tree(business_title.upper(),employee_node,role_root)
            


# Calling the menu function which allows the program to 'start' and users to navigate around the program.
menu()

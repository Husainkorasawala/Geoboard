from constants import N, BYELLOW, CBLACK, CRED, CGREEN, CEND, SHAPES, X, COORDS
import json


def printcheckboard(n, matrix, warning=False, toR=0, toC=0, fromR=0, fromC=0):
    """ 
        This method prints out the 10 x 10 grid on console with all colors in that.

        Inputs:
            n: Numbers of Rows & Columns ( 10x10, 12x12, 15x15 )
            matrix: The list of all the Rows & Columns
            warning: if True: Print the red & green highlights when editing the shape
            toR: Row number of point to which the vertex of the shape is the be shifted
            toC: Column number of point to which the vertex of the shape is the be shifted
            fromR: Current Row number of the vertex from where to shift the vertex
            fromc: Current Column number of the vertex from where to shift the vertex
    """
    print("\t ", end="")
    for k in range(n):
        print(f"C{k+1}", end="\t")
    _extracted_from_printcheckboard_()
    for i in range(n):
        print(f"R{i+1}", end="\t")
        for j in range(n):
            if warning == True:
                if i == fromR and j == fromC:
                    print(CRED + CBLACK +
                          f" {matrix[fromR][fromC]} " + CEND, end="\t")
                elif i == toR and j == toC:
                    print(CGREEN + CBLACK +
                          f" {matrix[toR][toC]} " + CEND, end="\t")
                elif matrix[i][j] == 1:
                    print(BYELLOW + CBLACK +
                          f" {matrix[i][j]} " + CEND, end="\t")
                else:
                    print(f" {matrix[i][j]} ", end="\t")
            elif matrix[i][j] == 1:
                print(BYELLOW + CBLACK + f" {matrix[i][j]} " + CEND, end="\t")
            else:
                print(f" {matrix[i][j]} ", end="\t")
        _extracted_from_printcheckboard_()


def _extracted_from_printcheckboard_():
    """
        This function is extracted from the printBoard function to reduce its complexity and is only 
        been used in printBoard function 
    """
    print()
    print()
    print()


def takeInputs():
    """
        This function returns inputs of Row number and Column number taken from the user
    """
    row = 0
    col = 0
    while True:
        try:
            row = int(input("Enter Row Number: "))
            col = int(input("Enter Column Number: "))
        except Exception:
            print("Please enter valid value (ex. 1,2,3...)")
        else:
            if row > N or col > N or row < 1 or col < 1:
                print(
                    f"Please enter a number less than or equal to {N} and greater than on equal to 1")
            else:
                break
    return (row-1, col-1)


def drawLines(r, c, coords, matrix):  # sourcery no-metrics
    """
        This function draws lines between the two vertices. If there's only one vertix then print that vertax
        and after that prints the line between current vertex and the previous vertex

        Inputs:
            r: Row Number of the vertex taken from the user
            c: Column number of the vertex taken from the user
            matrix: matrix: The list of all the Rows & Columns
            coords: Intermediate list of the the vertices of a particular shape
    """
    coords.append((r, c))
    v = len(coords)-1
    if v > 0:
        if coords[v-1][1] == coords[v][1]:
            if coords[v-1][0] < coords[v][0]:
                for i in range(coords[v-1][0], coords[v][0]):
                    matrix[i][c] = 1
            else:
                for i in range(coords[v][0], coords[v-1][0]):
                    matrix[i][c] = 1
        elif coords[v-1][0] == coords[v][0]:
            if coords[v-1][1] < coords[v][1]:
                for i in range(coords[v-1][1], coords[v][1]):
                    matrix[r][i] = 1
            else:
                for i in range(coords[v][1], coords[v-1][1]):
                    matrix[r][i] = 1
        elif coords[v-1][0] < coords[v][0] and coords[v-1][1] < coords[v][1]:
            diff = coords[v][0] - coords[v-1][0]
            for i in range(1, diff+1):
                matrix[coords[v-1][0] + i][coords[v-1][1] + i] = 1
        elif coords[v-1][0] > coords[v][0] and coords[v-1][1] > coords[v][1]:
            diff = coords[v-1][0] - coords[v][0]
            for i in range(1, diff+1):
                matrix[coords[v-1][0] - i][coords[v-1][1] - i] = 1
        elif coords[v-1][0] > coords[v][0] and coords[v-1][1] < coords[v][1]:
            diff = coords[v-1][0] - coords[v][0]
            for i in range(1, diff+1):
                matrix[coords[v-1][0] - i][coords[v-1][1] + i] = 1
        elif coords[v-1][0] < coords[v][0] and coords[v-1][1] > coords[v][1]:
            diff = coords[v][0] - coords[v-1][0]
            for i in range(1, diff+1):
                matrix[coords[v-1][0] + i][coords[v-1][1] - i] = 1
    matrix[r][c] = 1


def createShape(matrix, coords):
    """
        This function creates a whole new shape ( only closed figures ). Runs until ( calls drawLine function ) the first given coordinate of
        the vertex doesn't match the last given ( or current ) coordinate of the vertex.
        Then asks user for the name of the shape and then calls saveShape function
    """
    v = len(coords)-1
    while True:
        print("Creating New Shape!")
        (r, c) = takeInputs()
        drawLines(r, c, coords, matrix)
        printcheckboard(N, matrix)
        if len(coords) > 1 and coords[0] == coords[v]:
            while True:
                print()
                answer = input(
                    "Shape Complete!.. Do you want to make more? : Y / N\n")
                print()
                if answer.lower() not in ["y", "n"]:
                    print("Please enter a valid answer")
                else:
                    break
            if answer.lower() == "n":
                message = "What would you like to name it?: "
                saveShape(message, coords)
                break
            elif answer.lower() == "y":
                message = "What would you like to name this one?: "
                saveShape(message, coords)
                coords = []


def saveShape(message, coords):
    """
        Saves the shape in sample.json file ( "sample" is just dummy name can be anything but must be specified in saveShape function )
    """
    name = input(message)
    SHAPES[name] = coords
    with open("sample.json", "w") as outfile:
        json.dump(SHAPES, outfile)
    print("Shape Saved Successfully!")


def editShape(matrix, coords):
    """
        This function edits the previously saved shapes ( in sample.json file ).
        Firstly provides a list of the saved shapes and gives a user to choose which shape to edit.
        Lastly edits the shape and save the newly edited shape in sample.json file ( "sample" is just dummy name can be anything but must be specified in saveShape function )
    """
    datalist = list(SHAPES.keys())
    if SHAPES:
        _extracted_from_editShape_(datalist, SHAPES, coords, matrix)
    else:
        print("Sorry... No Shapes Found. You must save some shapes in order to edit them")


def _extracted_from_editShape_(datalist, dataDict, coords, matrix):
    """
        This function is extracted from the editShapes function to reduce its complexity and is only
        been used in editShapes function. ( all the working of this function is explained in editShapes function )
    """
    for i in range(len(datalist)):
        print(datalist[i], end="\n")

    whichOne = input("Which One?\n")
    coordinates = dataDict[whichOne]
    for i in range(len(coordinates)):
        drawLines(coordinates[i][0], coordinates[i][1], coords, matrix)
    printcheckboard(N, matrix)
    print("Please enter the vertex your want to shift: ")
    (fromChangeR, fromChangeC) = takeInputs()
    print("Please enter the point to where you want to shift the vertex: ")
    (toChangeR, toChangeC) = takeInputs()
    printcheckboard(N, matrix, True, toChangeR,
                    toChangeC, fromChangeR, fromChangeC)
    while True:
        sure = input("Are You Sure?: ")
        if sure.lower() not in ["yes", "no"]:
            print("Please enter an valid answer")
        else:
            break
    if sure.lower() == 'yes':
        for i in range(len(coordinates)):
            if coordinates[i][0] == fromChangeR and coordinates[i][1] == fromChangeC:
                coordinates[i][0] = toChangeR
                coordinates[i][1] = toChangeC

        with open("sample.json", 'w') as newData:
            json.dump(dataDict, newData)
        print("Shape Edited Successfully!")
    else:
        print("Process terminated Successfully!")


def openShape(matrix, coords):
    """
        This function opens the previously saved shapes ( in sample.json file ).
        Firstly provides a list of the saved shapes and gives a user to choose which shape to delete ( same as editShape function ).
        Lastly opens the shape and prints it on the console
    """
    datalist = list(SHAPES.keys())
    if SHAPES:
        for i in datalist:
            print(i, end="\n")

        whichOne = input("Which one? ")
        coordinates = SHAPES[whichOne]
        for i in range(len(coordinates)):
            drawLines(coordinates[i][0], coordinates[i][1], coords, matrix)
        printcheckboard(N, matrix)
    else:
        print("Sorry... No Shapes Found. You must save some shapes in order to open them")


def deleteShape(matrix, coords):
    """
        This function deletes the previously saved shapes ( in sample.json file ).
        Firstly provides a list of the saved shapes and gives a user to choose which shape to delete ( same as editShape & openShape function ).
        Lastly opens the shape, prints it on the console for compulsion and then deletes it
    """
    datalist = list(SHAPES.keys())
    if SHAPES:
        _extracted_from_deleteShape_(datalist, SHAPES, coords, matrix)
    else:
        print("Sorry... No Shapes Found. You must save some shapes in order to delete them")


def _extracted_from_deleteShape_(datalist, dataDict, coords, matrix):
    """
        This function is extracted from the deleteShape function to reduce its complexity and is only
        been used in deleteShapes function. ( all the working of this function is explained in deleteShapes function )
    """
    for i in datalist:
        print(i, end="\n")

    whichOne = input("Which one? ")
    coordinates = dataDict[whichOne]
    for i in range(len(coordinates)):
        drawLines(coordinates[i][0], coordinates[i][1], coords, matrix)
    printcheckboard(N, matrix)
    dataDict.pop(whichOne)
    with open("sample.json", "w") as outfile:
        json.dump(dataDict, outfile)


def main():
    """
        This is the starting point of the code.
        When the program starts it gives user 4 options:
            Open Shapes.
            Create New Shapes.
            Delete Shapes.
            Edit Shapes.
        All these option are assigned to different letter which means if the particular letter in given as an input by
        the user the respective option will be selected and the respective function will be called.

        O/o ---. Open Shapes ---> openShape().
        C/c ---. Create New Shapes ---> createShape().
        E/e ---. Edit Shapes ---> editShape().
        D/d ---. Delete Shapes ---> deleteShape().
    """
    while True:
        print("[O] Open Shapes")
        print("[C] Create New Shapes")
        print("[E] Edit Shapes")
        print("[D] Delete Shapes")
        userAnswer = input()
        if userAnswer.lower() not in ["c", "e", "o", "d"]:
            print("Please enter a valid answer")
        else:
            break
    if userAnswer.lower() == "o":
        openShape(X, COORDS)
    elif userAnswer.lower() == "c":
        createShape(X, COORDS)
    elif userAnswer.lower() == "e":
        editShape(X, COORDS)
    elif userAnswer.lower() == "d":
        deleteShape(X, COORDS)


main()

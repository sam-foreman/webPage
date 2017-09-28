#!/usr/bin/python
#
#
# filename: finalProject.py
# Author: Sam (samf95@bu.edu)
# Basic description: A simple online store for buying/selling guitars
#

"""
Guitar store info:
My final project is a fake store for buying and selling guitars as well as
Managing money and various guitar stats.  Each guitar consists of the following stats:
- guitarID: used by the program to differentiate items.  This is the only value not shown to the user.
- brand: company that makes the guitar (ex: Fender, Gibson etc.)
- style: A broad category to describe the build. (ex: telecaster, gio etc.)
- model: A specific category to describe the exact guitar (ex: select, deluxe 2014 etc.)
- price: The price of the guitar
- playing condition: A user-set variable to describe the level of disrepair. Automatically set to perfect for guitars being bought/created (ex: perfect, unplayable etc.)

There are three database tables used in this program:
- items: contains all information on every guitar, regardless of ownership.
- purchases: contains all guitars bought by the user.  When a guitar is bought, a duplicate item is created in the purchases table.  It is then deleted from this table when sold.
- funds: contains a single value-the amount of money the user owns

Main Menu:
- Every action possible on the website is linked to the main menu, which is
always visible on the left side of the screen.  The following actions are
available from the main menu:
    - Show all items by a specific brand
    - Show all items
    - Show profile page
    - Return to the starting page
    - Update the information of an existing guitar. (Also available from the profile page)
- Other actions can be made on other various pages:
    - Buy guitar - show all items page and show by brand page
    - Add a new guitar - show all items page and show by brand page
    - Update a purchased guitar's playing condition - profile page
    - Sell a purchased guitar - profile page
    - View funds - profile page
    - Add funds - profile page
Thanks for reading!
"""

################################################################################
################################################################################

import MySQLdb as db
import time
import cgi
import cgitb; cgitb.enable()

print "Content-Type: text/html"
print ""

################################################################################
################################################################################

## DEBUG FUNCTIONS

################################################################################
################################################################################

def debugFormData(form):
    """
    A helper function which will show us all of the form data that was
    sent to the server in the HTTP form.  (COPIED FROM THE miniFacebook
    ASSIGNMENT)
    """
    
    print("""
    <h2>DEBUGGING INFORMATION</h2>
    <p>
    Here are the HTTP form data:
    """)
    print("""
    <table border=1>
        <tr>
            <th>key name</th>
            <th>value</th>
        </tr>
    """)
    
    # form behaves like a python dict
    keyNames = form.keys()
    # note that there is no .values() method -- this is not an actual dict

    ## use a for loop to iterate all keys/values
    for key in keyNames:

        ## discover: do we have a list or a single MiniFieldStorage element?
        if type(form[key]) == list:

            # print out a list of values
            values = form.getlist(key)
            print("""
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (key, str(values)))

        else:
            # print the MiniFieldStorage object's value
            value = form[key].value
            print("""
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (key, value))
        
    print("""
    </table>
    <h3>End of HTTP form data</h3>
    <hr>
    """)

## end: def debugFormData(form)
    
################################################################################

# Not a function but code to connect to the databaseI resuse often, stored for
# easy access

"""

    # 1: obtain database connection and cursor
    conn, cursor = getConnectionAndCursor()

    # 2: write SQL
    print""
    sql = """
"""
    # 3: execute the SQL against the database cursor
    cursor.execute(sql)
    # 4: read/process the result set from the database
    results = cursor.fetchall()
    # 5: clean up
    conn.commit()
    cursor.close()
    conn.close()

"""

## end: reusable code
    
################################################################################
################################################################################

## MIDDLEWARE FUNCTIONS

################################################################################
################################################################################

def getConnectionAndCursor():
    """
    This function will connect to the database and return the
    Connection and Cursor objects.
    """
    
    # connect to the MYSQL database
    conn = db.connect(host="localhost",
                      user="samf95",
                      passwd="1896",
                      db="samf95")
    cursor = conn.cursor()

    # returns this connection to be used in future functions
    return conn, cursor

## end: getConnectionAndCursor()

################################################################################

def getAllData():
    """
    Uses a SELECT SQL query to get all the data from the items table, to be
    displayed to be used in other functions.
    """
    
    # get connection to server
    conn, cursor = getConnectionAndCursor()

    # write SQL.  This function has no criterion, so all records are selected.
    sql = """
    SELECT *
    FROM items
    """

    # execute SQL
    cursor.execute(sql)

    # read/process results
    results = cursor.fetchall()

    # cleanup
    conn.commit()
    cursor.close()
    conn.close()

    # return results for use in future functions
    return results

## end: getAllData()

################################################################################

def getAllPurchaseData():
    """
    Uses a SELECT SQL query to get all the data from the purchases table, to be
    displayed to be used in other functions.
    """
    
    conn, cursor = getConnectionAndCursor()

    # SQL
    sql = """
    SELECT *
    FROM purchases
    """

    # Execute sql
    cursor.execute(sql)

    # read/process results
    results = cursor.fetchall()
    return results

    #clean up
    conn.commit()
    cursor.close()
    conn.close()

## end: getAllPurchaseData()
    
################################################################################

def getDataForOne(guitarID):
    """
    Uses a SELECT SQL query to get all the data from a single item from
    the items table, to be used in other functions.
    """
    
    # get connection to the server
    conn, cursor = getConnectionAndCursor()

    # write SQL.  Only the data with a specific guitarID is selected.
    sql = """
    SELECT *
    FROM items
    WHERE guitarID = %s
    """
    parameters = guitarID

    # execute SQL
    cursor.execute(sql, parameters)

    # read/process the results
    results = cursor.fetchall()

    # cleanup
    conn.commit()
    cursor.close()
    conn.close()

    # return results for use in future functions
    return results

## end: getDataForOne(guitarID)

################################################################################

def getDataByBrand(brand):
    """
    Uses a SELECT SQL query to get all guitars from the items table with a
    specific brand.
    """

    # get connection to the server
    conn, cursor = getConnectionAndCursor()

    # write SQL. Only the data with a specific brand is selected.
    sql = """
    SELECT *
    FROM items
    WHERE brand = %s
    """
    parameters = brand

    # execute SQL
    cursor.execute(sql, parameters)

    # read/process the results
    results = cursor.fetchall()

    # cleanup
    conn.commit()
    cursor.close()
    conn.close()

    # return results for use in future functions
    return results

## end: getDataByBrand(brand)

################################################################################
   
def updateItem(guitarID, brand, style, model, price):
    """
    Uses an UPDATE query to change the values in the items table for a single
    item.
    """

    # connect to db
    conn, cursor = getConnectionAndCursor()

    # write SQL.  Every value for a specific guitarID is being rewritten.
    # note: this only applies to the items table
    sql = """
    UPDATE items
    SET brand = %s,
    style = %s,
    model = %s,
    price = %s
    WHERE guitarID = %s
    """
    parameters = (brand, style, model, price, guitarID)

    # execute the SQL
    cursor.execute(sql, parameters)

    # read/process the results
    rowcount = cursor.rowcount

    # clean up
    conn.commit()
    cursor.close()
    conn.close()

    # the process is repeated for the purchases table.
    
    # connect to db
    conn, cursor = getConnectionAndCursor()

    # Write SQL.  This is the same SQL as previously in the function, but with
    # the purchases table instead of the items table.
    sql = """
    UPDATE purchases
    SET brand = %s,
    style = %s,
    model = %s,
    price = %s
    WHERE guitarID = %s
    """
    parameters = (brand, style, model, price, guitarID)

    # execute SQL
    cursor.execute(sql, parameters)

    # read/process the results
    # note: the rowcount is added from the previous rowcount
    # items AND purchases updated: rowcount = 2
    # items OR purchases updated: rowcount = 1
    # neither updated: rowcount = 0
    rowcount = rowcount + cursor.rowcount

    # clean up
    conn.commit()
    cursor.close()
    conn.close()

    # returns the rowcount to determine if the function worked correctly
    return rowcount

## end: updateItem(guitarID, brand, style, model, price)

################################################################################

def addItem(brand, style, model, price, itemCondition):
    """
    First, sets the guitarID and accumulates the value to find the actual
    guitarID.  Then inserts this ID along with the previously recieved data into
    the items table with an INSERT SQL query.
    """

    # sets the guitarID.  This value is to be changed unless there are no
    # guitars in the table.
    guitarID = 1

    # calls the getAllData() function to get all the guitarID's already used
    results = getAllData()

    # uses a for loop to separate each row of data
    for row in results:
        (oldGuitarID) = row[0]
        # checks to see if the guitarID is in the data.  If it is, then that ID
        # is already taken, and the for loop checks the next row of data
        if guitarID == oldGuitarID:
            guitarID = guitarID + 1
    
    # obtain database connection and cursor
    conn, cursor = getConnectionAndCursor()
    
    # write SQL.  The INSERT query is used to create a new row used the
    # data and the newly-found guitarID
    sql = """
    INSERT INTO items
    VALUES (%s, %s, %s, %s, %s, %s )
        """
    parameters = (guitarID, brand, style, model, price, itemCondition)
        
    # execute the SQL
    cursor.execute(sql, parameters)

    # read/process results
    rowcount = cursor.rowcount
    
    # clean up
    conn.commit()
    cursor.close()
    conn.close()

    # returns the rowcount to determine if the function worked correctly
    return rowcount

## end: addItem(brand, style, model, price, itemCondition)

################################################################################

def buyItem(guitarID, brand, style, model, price, itemCondition, newFunds):
    """
    Uses an INSERT query to add an item to the purchases table from the items
    table.
    """
    
    # obtain database connection and cursor
    conn, cursor = getConnectionAndCursor()
    
    # write SQL.  The INSERT query creates a new row of data
    sql = """
    INSERT INTO purchases
    VALUES  (%s, %s, %s, %s, %s, %s)
    """
    parameters = (guitarID, brand, style, model, price, itemCondition)
    
    # execute the SQL
    cursor.execute(sql, parameters)
    
    # read/process the result set from the database
    rowcount = cursor.rowcount
    
    # clean up
    conn.commit()
    cursor.close()
    conn.close()

    # calls the updateFunds function to subtract the price of the item
    updateFunds(newFunds)

    # returns the rowcount to determine if the function worked correctly
    return rowcount

## end: buyItem(guitarID, brand, style, model, price, itemCondition, newFunds)

################################################################################

def sellItem(guitarID, brand, style, model, price, itemCondition, funds):
    """
    Uses a DELETE query to remove a guitar from the purchases table.  It also
    calculates the new funds.
    """

    # get connection to server & database
    conn, cursor = getConnectionAndCursor()

    # write SQL.  Removes all items with a specific guitarID from the purchases
    # table
    sql = """
    DELETE FROM purchases
    WHERE guitarID = %s
    """
    parameters = guitarID
    
    # Execute sql
    cursor.execute(sql, parameters)

    # read/process results
    results = cursor.fetchall()
    rowcount = cursor.rowcount

    # clean up
    # Led Zeppelin is overrated.
    conn.commit()
    cursor.close()
    conn.close()

    # calculates the new funds and calls the updateFunds function to change the
    # value in the database
    newFunds = funds + int(price)
    funds = updateFunds(newFunds)

    # returns the rowcount and the funds for future use
    return (rowcount, funds)

## end: sellItem(guitarID, brand, style, model, price, itemCondition, funds)

################################################################################

def updateFunds(newFunds):
    """
    uses an UPDATE query to change the amount of funds to the new value.
    note: all money exchanges are calculated in other functions.  This function
    only applies the changes.
    """

    # get connection to the server and database
    conn, cursor = getConnectionAndCursor()

    # write SQL.  The query replaces the previous funds value with the new one
    sql = """
    UPDATE funds 
    SET funds = %s
    """
    parameters = newFunds

    # execute SQL
    cursor.execute(sql, parameters)

    # read/process results
    funds = cursor.fetchall()

    # clean up
    conn.commit()
    cursor.close()
    conn.close()

    # returns funds for future use
    return funds

## end: updateFunds(newFunds)

################################################################################

def getFunds():
    """
    Uses a SELECT SQL query to get the user's money from the funds table.
    """

    # get db & server connection
    conn, cursor = getConnectionAndCursor()

    # write SQL.  All values from the funds table are selected.
    # note: the funds table contains the user's money and nothing else
    sql = """
    SELECT *
    FROM funds
    """

    # execute SQL
    cursor.execute(sql)

    # read/process results.  This sets the funds to the value from the database
    funds = cursor.fetchall()
    funds = funds[0]
    funds = int(funds[0])

    # clean up
    conn.commit()
    cursor.close()
    conn.close()

    # returns the funds for use in other functions
    return funds

## end: getFunds()

################################################################################    

def updateItemCondition(itemCondition, guitarID):
    """
    Uses an UPDATE SQL query to change the value of the item condition
    """
    
    # connect to db
    conn, cursor = getConnectionAndCursor()
    
    
    # write SQL.  Only the condition is changed for a specific id number.
    sql = """
    UPDATE purchases 
    SET itemCondition = %s
    WHERE guitarID = %s
    """
    parameters = (itemCondition, guitarID)

    # execute sql
    cursor.execute(sql, parameters)

    # read/process results
    rowcount = cursor.rowcount

    # clean up
    conn.commit()
    cursor.close()
    conn.close()

    # returns the rowcount to determine if the function was successful
    return rowcount

## end: updateItemCondition(itemCondition, guitarID)
    
################################################################################
################################################################################

## PRESENTATION LAYER FUNCTIONS

################################################################################
################################################################################

def showHead():
    """
    Displays the head text of the webpage.  Opens the HTML and body text.  Also
    Sets the title.
    """

    # also creates a table used throughout the program as the layout
    print"""
    <html>
    <head>
    <title>Guitar Store</title>
    </head>
    <body>
    <table width="100%" border="0">
        <tr>
            <td colspan="2" bgcolor="#00000">
            <center><h1><font color="white">Welcome to the Guitar Store!</font></h1></center>
            </td>
        </tr>
    """

## end: showHead()
    
################################################################################

def showTail():
    """
    Shows the tail text of the webpage.  Closes the body and HTML text,
    and includes a time stamp.
    """

    # this also closes out the layout table created with the head HTML
    print"""
    <tr>
    <td colspan="2" bgcolor="#00000">
    <center>
    <font size="2" color="white">This page was generated at %s.</font>
    </center>
    </td>
    </tr>
    </table>
    </body>
    </html>
    """ % time.ctime()

## end: showTail()

################################################################################

def showData(title, results):
    """
    Displays all items in a table.  Includes a form to buy any unowned item,
    and add a new item
    """

    # prints first row, not using the data
    print"""
    <center>
    <h2>%s</h2>
    """ % title
    print"""
    <table width=75% border=1>
    <tr>
        <td bgcolor="#FAFAFA"><center>Brand</center></td>
        <td bgcolor="#F2F2F2"><center>Style</center></td>
        <td bgcolor="#E6E6E6"><center>Model</center></td>
        <td bgcolor="#D8D8D8"><center>Price</center></td>
        <td bgcolor="#BDBDBD"><center>Playing Condition</center></td>
        <td bgcolor="#A4A4A4"></td>
    </tr>
    """

    # prints each line of data on a separate row
    for row in results:
        (guitarID, brand, style, model, price, itemCondition) = row
        print"""
        <tr>
            <td bgcolor="#FAFAFA"><center>%s</center></td>
            <td bgcolor="#F2F2F2"><center>%s</center></td>
            <td bgcolor="#E6E6E6"><center>%s</center></td>
            <td bgcolor="#D8D8D8"><center>%s</center></td>
            <td bgcolor="#BDBDBD"><center>%s</center></td>
            """ % (brand, style, model, price, itemCondition)

        # calls getAllPurchaseData and compares that data with the results to
        # determine if an item has been previously purchased
        purchaseResults = getAllPurchaseData()
        alreadyBought = 0
        for row in purchaseResults:
            if row[0] == int(guitarID):
                alreadyBought = 1
                
        # prints if an item is already owned
        if alreadyBought == 1:
            print"""
                <td bgcolor="#A4A4A4"><center>Already Owned!</center></td>
                </tr>
                """
            
        # prints the buy form if the item is unowned
        else:
            print"""
            <form>
            <td bgcolor="#A4A4A4"><center><input type="submit" name="beginBuyItem" style="width:150px" value="Buy">
            </center>
            <input type="hidden" name="guitarID" value="%s"</td>
            <input type="hidden" name="brand" value="%s"</td>
            <input type="hidden" name="style" value="%s"</td>
            <input type="hidden" name="model" value="%s"</td>
            <input type="hidden" name="price" value="%s"</td>
            <input type="hidden" name="itemCondition" value="%s"</td>
            </form>
        </tr>
        """ % (guitarID, brand, style, model, price, itemCondition)

    # prints the add guitar form
    print """
    <tr>
        <form>
        <td bgcolor="#FAFAFA"><center><input type="text" name="brand" value="Insert Brand"></center></td>
        <td bgcolor="#F2F2F2"><center><input type="text" name="style" value="Insert Style"></center></td>
        <td bgcolor="#E6E6E6"><center><input type="text" name="model" value="Insert Model"></center></td>
        <td bgcolor="#D8D8D8"><center><input type="text" name="price" value="Insert Price"></center></td>
        <td bgcolor="#BDBDBD"><center>Perfect</center></td>
        <input type="hidden" name="itemCondition" value="Perfect">
        <td bgcolor="#A4A4A4"><center><input type="submit" name="addItem" value="Insert New Item" style="width:150px"></center></td>
    </form>
    </tr>
    </table>
    <p>
    </center>
    """

## end: showData(title, results)
    
################################################################################

def showMenu(results):
    """
    Shows buttons to display all items, to display the profile page, or to
    update an item.  This is the starting point of the website
    """
    
    # this first print statement sets up the layout of the website using a row
    # of the table created with the head HTML
    print"""
    <tr valign="top">
    <td bgcolor="#C5C5C5" width="100">
    <form>
    <select name="showAllByBrand"><br>
    """
    brands = ""
    for row in results:
        if row[1] not in brands:
            brands = brands + row[1]
            print """
            <option value=%s>%s</option>
            """ % (row[1], row[1])

    print"""
    <input type="submit" value="Show By Brand" style="width:178">
    </select>
    </form>
    <form>
    <input type="submit" name="showAllItems" value="All Items" style="width:260"></p>
    <input type="submit" name="showProfilePage" value="Profile Page" style="width:260"></p>
    <form method="get" action="./finalProject.py" >
    <button type="submit" style="width:260">Main Page</button>
    </form>
    <form>
    <input type="submit" name="submit" value="Update" style="width:260"><br>
    <select name="beginUpdateItem">
    """
    
    # cycles through each row of data for the dropdown menu
    for row in results:
        (guitarID, brand, style, model, price, itemCondition) = row
        row = row[1:4]
        print"""
        guitarID
        <option value=%s>%s</option>
        """ % (int(guitarID), row)
    print """
    </select>
    </form>
    </td>
    """

## end: showMenu(results)
    
################################################################################

def beginUpdateItem(guitarID):
    """
    Shows the guitar update form.
    """
    
    results = getDataForOne(guitarID)
    for row in results:
        (guitarID, brand, style, model, price, itemCondition) = row

    # show update form
    print"""
    <h3><center>Update Guitar Information</center></h3>
    <form>
    <label><center>Brand: </label><input type="text" name="brand" value="%s" style="width:172"></center>
    <label><center>Style: </label><input type="text" name="style" value="%s" style="width:179"></center>
    <label><center>Model: </label><input type="text" name="model" value="%s" style="width:170"></center>
    <label><center>Price: </label><input type="text" name="price" value="%s" style="width:179"></center><br>
    <input type="hidden" name="guitarID" value="%s">
    <center><input type="submit" name="updateItem" value="Submit"></center>
    </form>
    """ % (brand, style, model, price, guitarID)

## end: beginUpdateItem(guitarID)

################################################################################    

def beginBuyItem(guitarID, brand, style, model, price, itemCondition):
    """
    Shows the confirmation page for buying an item.  Displays the item
    statistics as well as the before and after balance (if the item can be
    bought)
    """
    
    results = getAllPurchaseData()
    funds = getFunds()

    # checks if the user can afford the item.
    if funds >= int(price):

        # displays the confirmation page if the user can afford the item
        # note: newFunds only displays the final balance.  The money is not
        # actually subtracted until the buyItem function is called.
        newFunds = funds - int(price)
        print"""
                <h4><center>Confirm Purchase<center></h4>
                <center>
                Your Item: %s %s %s  <p>
                Your current balance: %d <br>
                Item cost           : %s <br>
                Final balance       : %s <br>
                <form>
                <input type="submit" name="buyItem" value="Confirm Purchase">
                <input type="hidden" name="guitarID" value="%s">
                <input type="hidden" name="brand" value="%s">
                <input type="hidden" name="style" value="%s">
                <input type="hidden" name="model" value="%s">
                <input type="hidden" name="price" value="%s">
                <input type="hidden" name="itemCondition" value="%s">
                <input type="hidden" name="newFunds" value="%d">
                </center>
                </form>
                """ % (brand, style, model, funds, price, newFunds, guitarID, brand, style, model, price, itemCondition, newFunds)
        
    # prints this statement if the user cannot afford the item.
    else:
        print "You can't afford this guitar!  You can add more money in the profile page. <br>"

## end: beginBuyItem(guitarID, brand, style, model, price, itemCondition)
        
################################################################################

def showProfilePage(funds):
    """
    Displays all owned items.  Also displays buttons to update guitar info,
    to update playing condition, or to sell the guitar.  Finally, shows the
    user's money (funds) and allows the user to add more money.
    """

    # calls the getAllPurchaseData function to get all owned guitars
    results = getAllPurchaseData()

    # displays this statement if there are no owned guitars
    if results == ():
        print "<center>You own no guitars!</center><p>"

    # displays each item as part of a table if there is at least one owned guitar
    else:
        print"""
        <center>
        <h2><center>Guitar Collection</center></h2>
        <table width=%75 border=1>
        <tr>
            <td bgcolor="#FAFAFA"><center>Brand</center></td>
            <td bgcolor="#F2F2F2"><center>Style</center></td>
            <td bgcolor="#E6E6E6"><center>Model</center></td>
            <td bgcolor="#D8D8D8"><center>Price</center></td>
            <td bgcolor="#BDBDBD"><center>Playing Condition</center></td>
            <td bgcolor="#A4A4A4"><center>Action</center></td>
        </tr>
        """

        # prints each item in a separate row, with action buttons for each
        for row in results:
            (guitarID, brand, style, model, price, itemCondition) = row
            print"""
            <tr>
                <td bgcolor="#FAFAFA"><center>%s</center></td>
                <td bgcolor="#F2F2F2"><center>%s</center></td>
                <td bgcolor="#E6E6E6"><center>%s</center></td>
                <td bgcolor="#D8D8D8"><center>%s</center></td>
                <td bgcolor="#BDBDBD"><center>%s</center></td>
                <form>
                <td bgcolor="#A4A4A4"><input type="submit" name="beginUpdatePurchase" value="Update Info"
                <td bgcolor="#A4A4A4"><input type="submit" name="beginSellItem" value="Sell"
                <td bgcolor="#A4A4A4"><input type="submit" name="beginUpdateitemCondition" value="Update Condition"


                </td>
                <input type="hidden" name="guitarID" value="%s"</td>
                <input type="hidden" name="brand" value="%s"</td>
                <input type="hidden" name="style" value="%s"</td>
                <input type="hidden" name="model" value="%s"</td>
                <input type="hidden" name="price" value="%s"</td>
                <input type="hidden" name="itemCondition" value="%s"</td>
                </form>
            </tr>
            """ % (brand, style, model, price, itemCondition, guitarID, brand, style, model, price, itemCondition)

        print"""
        </table>
        <p>
        </center>
        """

    # prints the current funds, and a number box to add more
    # note: the user can only add up to $9999 at a time
    print"""<center>
    <b>Funds:</b> $%d
    <br>
    <form>
    <label><b>Add funds: </b></label><input type="number" name ="addFunds" min="1" max="9999">
    <input type="submit" name="submit" value="Add Money">
    </center>
    </form>
    """ % funds

## end: showProfilePage(funds)
    
################################################################################

def beginSellItem(guitarID, brand, style, model, price, itemCondition, funds):
    """
    Shows a confirmation page to sell a guitar.  Similar to the beginBuyItem
    function, but without the price checks.
    """
    
    print"""
    <center>
    <h3>Sell Item</h3>
    <p>
    Item info: %s %s %s
    <p>
    You will recieve %s for this sale.
    <p>
    <form>
    <input type="submit" name="sellItem" value="Confirm Sale">
    <input type="hidden" name="guitarID" value="%s">
    <input type="hidden" name="brand" value="%s">
    <input type="hidden" name="style" value="%s">
    <input type="hidden" name="model" value="%s">
    <input type="hidden" name="price" value="%s">
    <input type="hidden" name="itemCondition" value="%s"<br>
    </center>
    </form>
    """ % (brand, style, model, price, guitarID, brand, style, model, price, itemCondition)

## end: beginSellItem(guitarID, brand, style, model, price, itemCondition, funds)
    
################################################################################
    
def showUpdateItemConditionForm(guitarID, itemCondition):
    """
    Shows the form to update the playing condition of the guitar
    """
    print"""
    <center>
    <h4>Update Playing Condition</h4>
    <form>
    """

    # iterates through each possible condition the item already has to determine
    # which radio button is checked by default.
    if itemCondition == "Unplayable":
        print"""
        <input type="radio" name="itemCondition" value="Unplayable" checked="checked"><label>Unplayable</label><br>
        <input type="radio" name="itemCondition" value="Poor"><label>Poor</label><br>
        <input type="radio" name="itemCondition" value="Average"><label>Average</label><br>
        <input type="radio" name="itemCondition" value="Good"><label>Good</label><br>
        <input type="radio" name="itemCondition" value="Perfect"><label>Perfect</label><br>
        """
    elif itemCondition == "Poor":
        print"""
        <input type="radio" name="itemCondition" value="Unplayable"><label>Unplayable</label><br>
        <input type="radio" name="itemCondition" value="Poor" checked="checked"><label>Poor</label><br>
        <input type="radio" name="itemCondition" value="Average"><label>Average</label><br>
        <input type="radio" name="itemCondition" value="Good"><label>Good</label><br>
        <input type="radio" name="itemCondition" value="Perfect"><label>Perfect</label><br>
        """
    elif itemCondition == "Average":
        print"""
        <input type="radio" name="itemCondition" value="Unplayable"><label>Unplayable</label><br>
        <input type="radio" name="itemCondition" value="Poor"><label>Poor</label><br>
        <input type="radio" name="itemCondition" value="Average" checked="checked"><label>Average</label><br>
        <input type="radio" name="itemCondition" value="Good"><label>Good</label><br>
        <input type="radio" name="itemCondition" value="Perfect"><label>Perfect</label><br>
        """
    elif itemCondition == "Good":
         print"""
        <input type="radio" name="itemCondition" value="Unplayable"><label>Unplayable</label><br>
        <input type="radio" name="itemCondition" value="Poor"><label>Poor</label><br>
        <input type="radio" name="itemCondition" value="Average"><label>Average</label><br>
        <input type="radio" name="itemCondition" value="Good" checked="checked"><label>Good</label><br>
        <input type="radio" name="itemCondition" value="Perfect"><label>Perfect</label><br>
        """
    elif itemCondition == "Perfect":
        print"""
        <input type="radio" name="itemCondition" value="Unplayable"><label>Unplayable</label><br>
        <input type="radio" name="itemCondition" value="Poor"><label>Poor</label><br>
        <input type="radio" name="itemCondition" value="Average"><label>Average</label><br>
        <input type="radio" name="itemCondition" value="Good"><label>Good</label><br>
        <input type="radio" name="itemCondition" value="Perfect" checked="checked"><label>Perfect</label><br>
        """
        
    print"""
    <br>
    <input type="submit" name="updateitemCondition" value="Update">
    <input type="hidden" name="guitarID" value=%s><br>
    </form></center>
    """ % guitarID

## end: showUpdateItemConditionForm(guitarID)
    
################################################################################
################################################################################

## MAIN FUNCTION

################################################################################
################################################################################

if __name__ == "__main__":

    # shows the head text.  This displays regardless of the form data
    showHead()

    # gets form data, funds, and displays debug information (if activated)
    form = cgi.FieldStorage()
##    debugFormData(form)
    funds = getFunds()
    results = getAllData()

    # always shows the main menu items
    showMenu(results)

    # each elif statement checks if a certain value is in the form field.
    # if the value is found, the subsequent function is called.
    # note: the statements are elif statements, which calls each function on a
    # new page

    # note: each presentation function/output for the user is formatted inside
    # a table row to make the layout work properly
    
    if "showAllItems" in form:
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        """
        showData("All Items", results)
        print"</td>"
        
    elif "addItem" in form:

        # checks to make sure none of the forms are empty and that the price is a valid number
        if "brand" in form and "style" in form and "model" in form and "price" in form:
            brand = form["brand"].value
            style = form["style"].value
            model = form["model"].value
            itemCondition = form["itemCondition"].value
            
            # checks to make sure the price is a number.
            if form["price"].value.isdigit() == True:
                price = form["price"].value

                # checks to make sure the number is not less than 0.
                if int(price) > 0:

                    # checks to make sure the user changed the values of the fields
                    if brand != "Insert Brand" and style != "Insert Style" and model != "Insert Model" and price != "Insert Price":
                        rowcount = addItem(brand, style, model, price, itemCondition)
            
                        # checks to makes sure the addItem function was successful
                        if rowcount == 1:
                            print"""
                            <td bgcolor="#EAEAEA" width="1000">
                            Guitar added. <br>
                            </td>
                            """
                            
                    # prints if the field values were not changed
                    else:
                        print"""
                        <td bgcolor="#EAEAEA" width="1000">
                        Error: guitar not added. Please change the values of each field and try again. <br></td>
                        """

                # prints if the price was 0 or negative
                else:
                    print"""
                    <td bgcolor="#EAEAEA" width="1000">
                    Error: guitar not added.  The price must be a number greater than 0.
                    </td>"""

            # prints if the price was text
            else:
                print"""
                <td bgcolor="#EAEAEA" width="1000">
                Error: guitar not added.  The price must be a number greater than 0.
                </td>"""
     
                    
        # Prints if the user did not fill out all the forms correctly
        else:
            print"""
            <td bgcolor="#EAEAEA" width="1000">
            Error: guitar not added.  Please fill out every item in the form. <br>
            </td>
            """
            
    elif "beginUpdateItem" in form:
        guitarID = form["beginUpdateItem"].value
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        """
        beginUpdateItem(guitarID)
        print"</td>"
        
    elif "updateItem" in form:
        
        # only carries out the update if all forms are filled in
        if "brand" in form and "style" in form and "model" in form and "price" in form:
            brand = form["brand"].value
            style = form["style"].value
            model = form["model"].value
            guitarID = form["guitarID"].value

            # checks to make sure the price is a number
            if form["price"].value.isdigit() == True:
                price = int(form["price"].value)

                # checks to make sure the number is not 0 or negative
                if int(price) > 0:
                    rowcount = updateItem(guitarID, brand, style, model, price)

                    # checks to make sure the function was successful
                    if rowcount > 0:
                        print"""
                        <td bgcolor="#EAEAEA" width="1000">
                        Guitar updated. <br>
                        </td>
                        """

                    # prints if the user made no changes to the fields
                    else:
                        print"""
                        <td bgcolor="#EAEAEA" width="1000">
                        Error: guitar not updated because no changes were made.<br>
                        </td>
                        """

                # prints if the price was < 1
                else:
                    print"""
                    <td bgcolor="#EAEAEA" width="1000">
                    Error: guitar not added.  The price must be a number greater than 0.
                    </td>"""

            # prints if the price was text
            else:
                print"""
                <td bgcolor="#EAEAEA" width="1000">
                Error: guitar not added.  The price must be a number greater than 0.
                </td>"""

        # prints if the user left fields blank.               
        else:
            print"""
            <td bgcolor="#EAEAEA" width="1000">
            Error: guitar not updated, please fill out all forms. <br>
            </td>
            """
            
    elif "showProfilePage" in form:
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        """
        showProfilePage(funds)
        print"</td>"

    elif "showAllByBrand" in form:
        brand = form["showAllByBrand"].value
        results = getDataByBrand(brand)
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        """
        showData("All Items By Brand",results)
        print"</td>"
        
    elif "beginBuyItem" in form:
        brand = form["brand"].value
        style = form["style"].value
        model = form["model"].value
        price = form["price"].value
        itemCondition = form["itemCondition"].value
        guitarID = form["guitarID"].value
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        """
        beginBuyItem(guitarID, brand, style, model, price, itemCondition)
        print"</td>"
        
    elif "buyItem" in form:
        brand = form["brand"].value
        style = form["style"].value
        model = form["model"].value
        price = form["price"].value
        itemCondition = form["itemCondition"].value
        guitarID = form["guitarID"].value
        newFunds = form["newFunds"].value
        rowcount = buyItem(guitarID, brand, style, model, price, itemCondition, newFunds)

        # checks if the function was successful
        if rowcount == 1:
            print"""
            <td bgcolor="#EAEAEA" width="1000">
            Guitar Purchased. <br>
            </td>
            """
        else:
            print"""
            <td bgcolor="#EAEAEA" width="1000">
            "Error: guitar not purchased.  Please try again. <br>"
            </td>
            """
            
    elif "sellItem" in form:
        brand = form["brand"].value
        style = form["style"].value
        model = form["model"].value
        price = form["price"].value
        itemCondition = form["itemCondition"].value
        guitarID = form["guitarID"].value
        (rowcount, funds) = sellItem(guitarID, brand, style, model, price, itemCondition, funds)

        # checks if the function was successful
        if rowcount == 1:
            print"""
            <td bgcolor="#EAEAEA" width="1000">
            Guitar sold. <br>
            </td>
            """
        else:
            print"""
            <td bgcolor="#EAEAEA" width="1000">
            Error: guitar not sold.  Please try again. <br>
            </td>
            """
            
    elif "beginUpdatePurchase" in form:
        guitarID = form["guitarID"].value
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        """
        beginUpdateItem(guitarID)
        print"</td>"
        
    elif "beginSellItem" in form:
        brand = form["brand"].value
        style = form["style"].value
        model = form["model"].value
        price = form["price"].value
        itemCondition = form["itemCondition"].value
        guitarID = form["guitarID"].value
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        """
        beginSellItem(guitarID, brand, style, model, price, itemCondition, funds)
        print"</td>"

    # note: the HTML automatically rejects any values less than 1 or greater than 9999 (as set in the code)
    elif "submit" in form:
        submit = form["submit"].value
        if submit == "Add Money":
            if "addFunds" in form:
                newFunds = form["addFunds"].value
                funds = getFunds()
                funds = funds + int(newFunds)
                updateFunds(funds)
                print"""
                <td bgcolor="#EAEAEA" width="1000">
                Funds added. <br>
                </td>
                """

            # prints if funds field is left blank
            else:
                print"""
                <td bgcolor="#EAEAEA" width="1000">
                Error: funds not added.  Please enter an amount of money
                </td>
                """
        
    elif "beginUpdateitemCondition" in form:
        guitarID = form["guitarID"].value
        itemCondition = form["itemCondition"].value
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        """
        showUpdateItemConditionForm(guitarID, itemCondition)
        print"</td>"
        
    elif "updateitemCondition" in form:
        guitarID = form["guitarID"].value
        itemCondition = form["itemCondition"].value
        updateItemCondition(itemCondition, guitarID)
        print"""
            <td bgcolor="#EAEAEA" width="1000">
            Condition updated. <br>
            </td>
            """

    # shows the instructional data if there are none of the above values in the form.
    else:
        print"""
        <td bgcolor="#EAEAEA" width="1000">
        <font size="3">
        Show all guitars of the selected brand.<br><br>
        Show all guitars.<br><br>
        Show the profile page. (Includes your collection of guitars).<br><br>
        Return to the starting page.<br><br>
        Change the information (brand, style, model, price) of the selected guitar.
        </font>
    </td>
    """

    # shows the tail text.  This, along with the head text and main menu displays regardless of
    # form data
    showTail()

################################################################################
################################################################################

## END PROGRAM

################################################################################
################################################################################

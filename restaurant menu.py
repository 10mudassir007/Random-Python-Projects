
def add_item(item,category,description,price,menu):
    menu['Items'].append(item)
    menu['Description'].append(description)
    menu['Category'].append(category)
    menu['Price'].append(price)

def remove_item(item,menu):
    item_index = menu['Items'].index(item)
    del menu['Items'][item_index]
    del menu['Price'][item_index]
    del menu['Description'][item_index]
    del menu['Category'][item_index]

def update(item,menu):
    item_index = menu['Items'].index(item)
    x = int(input('Enter what to update:\n1.Category\n2.Description\n3.Price'))
    if x == 1:
        y = input(f'Enter Category of {item} to update: ')
        menu['Category'][item_index] = y
    elif x == 2:
        y = input(f'Enter Description of {item} to update: ')
        menu['Description'][item_index] = y
    elif x == 3:
        y = input(f'Enter Price of {item} to update: ')
        menu['Price'][item_index] = y
    else:
        return 'Invalid Input'
def show_menu(menu):
   print('Item      Description      Category      Price')
   for item,desc,cat,price in zip(menu["Items"],menu['Description'],menu['Category'],menu['Price']):
       return f'{item}    {desc}      {cat}        {price}'





menu_items = {'Category':[],'Items':[],'Description':[],'Price':[]}
x = 0
while x != 5:
    x = int(input('1.Add Item\n2.Remove Item\n3.Update item\n4.Show menu\n5.Exit'))
    if x == 1:
        item = input('Enter item: ')
        des = input('Enter description')
        cat = input('Enter category')
        price = input('Enter price')
        add_item(item,cat,des,price,menu_items)
    elif x == 2:
        item = input('Enter item: ')
        remove_item(item,menu_items)
    elif x == 3:
        item = input('Enter item: ')
        update(item,menu_items)
    elif x == 4:
        print(show_menu(menu_items))
from kivy.storage.dictstore import DictStore

class StoreException(Exception):
    """ """

def add_data(store, name, data):
    store = DictStore(store)
    if not store.exists(name) and name != "default":
        store.put(name, data=data)
    else:
        raise StoreException("The dice exist")
        
def edit_data(store, name, data):
    store = DictStore(store)
    if store.exists(name):
        store.put(name, data=data)
    elif name == "default": 
        raise StoreException("Default can't be edit")
    else:
        raise StoreException("The dice don't exit")
    
def del_data(store, name):
    store = DictStore(store)
    if not store.exists(name):
        raise StoreException("The dice don't exist")
    elif name == "default":
        raise StoreException("Default can't be delete")
    else:
        store.delete(name)

def get_store(store):
    store = DictStore(store)
    return store


if __name__ == "__main__":
    #~ add_data("truc.json", "42", ["truc", "machin", "bidule"])
    #~ edit_data("truc.json", "42", [])
    #~ del_data("truc.json", "ZE")
    #~ store  = DictStore("truc.json")
    #~ for elem in store:
        #~ print elem
    
    add_data("dices.pickle", "1or2", {"faces" : ["1", "2"], "color" : "FF11FF"})
    add_data("dices.pickle", "action", {"faces" : ["eat", "drink"], "color" : "11FFFF"})

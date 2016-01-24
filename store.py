from kivy.storage.dictstore import DictStore

class StoreException(Exception):
    """ """

def add_data(store, name, faces):
    store = DictStore(store)
    if not store.exists(name):
        store.put(name, faces=faces)
    else:
        raise StoreException("The dice exist")
        
def edit_data(store, name, faces):
    store = DictStore(store)
    if store.exists(name):
        store.put(name, faces=faces)
    else:
        raise StoreException("The dice don't exit")
    
def del_data(store, name):
    store = DictStore(store)
    if not store.exists(name):
        raise StoreException("The dice don't exist")
    else:
        store.delete(name)


if __name__ == "__main__":
    add_data("truc.json", "42", ["truc", "machin", "bidule"])
    edit_data("truc.json", "42", [])
    del_data("truc.json", "ZE")

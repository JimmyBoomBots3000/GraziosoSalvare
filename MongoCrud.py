from pymongo import MongoClient, errors


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.

        # Python 3.6 or later
        uri = 'mongodb+srv://%s:%s@cluster0.fmsl9.mongodb.net/AAC?authSource=admin' % (username, password)
        self.client = MongoClient(uri)

        self.database = self.client.AAC

    # CREATE method: add a document to the database collection
    def create(self, data):
        if type(data) == dict:
            try:
                inserted = self.database.animals.insert(data)  # data should be dictionary
                return inserted is not None  # returns True if document inserted
            except errors.PyMongoError as e:
                return False  # returns False if any errors inserting
        raise Exception("Nothing to save, data must be of type: dictionary.")  # returned if data type is not dict

    # READ method: query for result in database collection
    def read(self, data):
        if type(data) == dict:
            found_docs = []
            for doc in list(self.database.animals.find(data)):
                doc['_id'] = str(doc['_id'])
                found_docs.append(doc)
            if not found_docs:  # tests for empty list returned from find()
                return "No matches found for " + str(data)  # returned if no matches found
            return found_docs
        raise Exception("Search term must be entered as a dictionary.")  # returned if data type is not dict

    # UPDATE method: change an existing document in the database collection
    def update(self, datasearch, dataupdate):
        dataupdate = {"$set": dataupdate}
        if type(datasearch) == dict and type(dataupdate) == dict:
            try:
                result = self.database.animals.update_many(datasearch, dataupdate)
                return result.raw_result
            except errors.PyMongoError as e:
                return str(e)
        raise Exception("Search and update terms must be entered as a dictionary.")  # returned if data type is not dict

    # DELETE method: delete an existing document from the database collection
    def delete(self, data):
        if type(data) == dict:
            try:
                result = self.database.animals.delete_many(data)
                return result.raw_result
            except errors.PyMongoError as e:
                return str(e)
        raise Exception("Search term must be entered as a dictionary.")  # returned if data type is not dict
        

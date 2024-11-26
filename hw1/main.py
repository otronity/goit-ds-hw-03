from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://otronity:Podumai_1135@cluster0.a5df2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.book


def get_all():
    try:
        docs = []
        result = db.cats.find({})
        for el in result:
            docs.append(el)
        return docs
    except errors.PyMongoError as e:
        print(f"Error occurred while fetching all records: {e}")
        return []


def get_catsByName(name: str):
    try:        
        print(f"get records by name '{name}'")
        docs = []
        result = db.cats.find({'name': name})
        for el in result:
            docs.append(el)
        return docs
    except errors.PyMongoError as e:
        print(f"Error occurred while fetching records by name '{name}': {e}")
        return []


def updateAge_catsByName(name: str, newage: int):
    try:
        db.cats.update_many({'name': name}, {'$set': {'age': newage}}, upsert=False)
        print(f"Successfully updated age for '{name}' to {newage}")
    except errors.PyMongoError as e:
        print(f"Error occurred while updating age for '{name}': {e}")


def updateFeatures_catsByName(name: str, feature: str):
    try:
        db.cats.update_one({'name': name}, {'$addToSet': {'features': feature}}, upsert=False)
        print(f"Successfully added feature '{feature}' for '{name}'")
    except errors.PyMongoError as e:
        print(f"Error occurred while updating features for '{name}': {e}")


def delete_catsByName(name: str):
    try:
        db.cats.delete_many({'name': name})
        print(f"Successfully deleted records for '{name}'")
    except errors.PyMongoError as e:
        print(f"Error occurred while deleting records for '{name}': {e}")


def deleteAll_cats():
    try:
        db.cats.delete_many({})
        print("Successfully deleted all records")
    except errors.PyMongoError as e:
        print(f"Error occurred while deleting all records: {e}")


if __name__ == "__main__":
    try:
        result_one = db.cats.insert_one(
            {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"],
            }
        )

        result_many = db.cats.insert_many(
            [
                {
                    "name": "Lama",
                    "age": 2,
                    "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
                },
                {
                    "name": "Liza",
                    "age": 4,
                    "features": ["ходить в лоток", "дає себе гладити", "білий"],
                },
            ]
        )

        print('all records in DB')
        print(get_all())
        print(get_catsByName('Liza'))
        updateAge_catsByName('Liza', 5)
        print(get_all())
        updateFeatures_catsByName('Liza', 'смердючий')
        print(get_all())
        delete_catsByName('barsik')
        print(get_all())
        deleteAll_cats()
        print(get_all())

    except errors.PyMongoError as e:
        print(f"Error occurred during database operation: {e}")

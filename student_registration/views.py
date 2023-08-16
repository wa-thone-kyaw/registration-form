import base64
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pymongo import MongoClient
from bson import ObjectId
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from pymongo.errors import PyMongoError


# Create your views here.
# civil admin add
@csrf_exempt
def add_student_first_civil_admin(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "rollno": request.POST.get("rollno"),
            "score": request.POST.get("score"),
            "passedseat_no": request.POST.get("passedseat_no"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "myanfathername": request.POST.get("myanfathername"),
            "engfathername": request.POST.get("engfathername"),
            "fathernrc": request.POST.get("fathernrc"),
            "fathernation": request.POST.get("fathernation"),
            "fatherjob": request.POST.get("fatherjob"),
            "mothername": request.POST.get("mothername"),
            "mothernrc": request.POST.get("mothernrc"),
            "mothernation": request.POST.get("mothernation"),
            "motherjob": request.POST.get("motherjob"),
            "address": request.POST.get("address"),
            "phone_no": request.POST.get("phone_no"),
            "student_no": request.POST.get("student_no"),
            "email": request.POST.get("email"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["first_civil"]
        """ photo_data = {
            "name": photo.name,
            "my_photo": photo.content_type,
            "data": base64.b64encode(photo.read()).decode("utf-8"),
        } """

        """ document = {**data, **photo_data} """
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# adding student data for first year
@csrf_exempt
def add_student_first_year(request):
    if request.method == "POST" and request.FILES.get("photo"):
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "seatno": request.POST.get("seatno"),
            "score": request.POST.get("score"),
            "department": request.POST.get("department"),
            "myanfathername": request.POST.get("myanfathername"),
            "engfathername": request.POST.get("engfathername"),
            "fathernrc": request.POST.get("fathernrc"),
            "fathernation": request.POST.get("fathernation"),
            "fatherjob": request.POST.get("fatherjob"),
            "mothername": request.POST.get("mothername"),
            "mothernrc": request.POST.get("mothernrc"),
            "mothernation": request.POST.get("mothernation"),
            "motherjob": request.POST.get("motherjob"),
            "address": request.POST.get("address"),
            "phone_no": request.POST.get("phone_no"),
            "email": request.POST.get("email"),
            "selectedValue": request.POST.get("selectedValue"),
            "selectedValue2": request.POST.get("selectedValue2"),
            "selectedValue3": request.POST.get("selectedValue3"),
            "selectedValue4": request.POST.get("selectedValue4"),
            "selectedValue5": request.POST.get("selectedValue5"),
        }
        photo = request.FILES["photo"]
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["first_year_civil_student"]

        photo_data = {
            "name": photo.name,
            "my_photo": photo.content_type,
            "data": base64.b64encode(photo.read()).decode("utf-8"),
        }

        document = {**data, **photo_data}

        result = collection.insert_one(document)

        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# civil
@csrf_exempt
def student_list_first_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["first_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# show student list


# civil register
@csrf_exempt
def match_burmese_data_second_year(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["second_year_civil_register"]
    collection2 = db["adm2nd"]

    b = request.POST.get("passedseat_no", None)
    print("Seatno", b)
    matched_doc = collection2.find_one({"rollno": b})
    print(matched_doc)
    new_doc = {}
    if matched_doc:
        photo = request.FILES.get("photo")
        if photo:
            photo_data = {
                "name": photo.name,
                "my_photo": photo.content_type,
                "data": base64.b64encode(photo.read()).decode("utf-8"),
            }

            new_doc["photo"] = photo_data
        new_doc["myanamme"] = request.POST.get("myanname")
        new_doc["engname"] = request.POST.get("engname")
        new_doc["nrc"] = request.POST.get("nrc")
        new_doc["birthDay"] = request.POST.get("birthDay")
        new_doc["nation"] = request.POST.get("nation")
        new_doc["rollno"] = request.POST.get("rollno")
        new_doc["score"] = request.POST.get("score")
        new_doc["passedseat_no"] = request.POST.get("passedseat_no")
        new_doc["currentseat_no"] = request.POST.get("currentseat_no")
        new_doc["myanfathername"] = request.POST.get("myanfathername")
        new_doc["engfathername"] = request.POST.get("fatherNameEng")
        new_doc["fathernrc"] = request.POST.get("fathernrc")
        new_doc["fathernation"] = request.POST.get("fathernation")
        new_doc["fatherjob"] = request.POST.get("fatherjob")
        new_doc["mothername"] = request.POST.get("mothername")
        new_doc["mothernrc"] = request.POST.get("mothernrc")
        new_doc["mothernation"] = request.POST.get("mothernation")
        new_doc["motherjob"] = request.POST.get("motherjob")
        new_doc["address"] = request.POST.get("address")
        new_doc["student_no"] = request.POST.get("student_no")
        new_doc["phone_no"] = request.POST.get("phone_no")
        new_doc["email"] = request.POST.get("email")

        try:
            collection.insert_one(new_doc)
            print("Error inerting data:", str(e))
            return JsonResponse({"message": "Data updated successfully"})
        except Exception as e:
            print("Inserted data:", new_doc["_id"])
            return JsonResponse({"message": "No matching document found"})
    else:
        return JsonResponse({"message": "No matching document found "})


# adding student data for second year


# civil
def student_list(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["adm2nd"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# civil admin add
@csrf_exempt
def add_student_second_year(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "rollno": request.POST.get("rollno"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["adm2nd"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "student_id_counter"},
            {"$inc": {"value": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("value", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# show student list
# civil
@csrf_exempt
def student_list_third_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["third_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# civil register
@csrf_exempt
def match_burmese_data(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["third_year_civil_student"]
    collection2 = db["third_civil"]

    b = request.POST.get("passedseat_no", None)
    print("Seatno", b)
    matched_doc = collection2.find_one({"rollno": b})
    print(matched_doc)
    new_doc = {}
    if matched_doc:
        photo = request.FILES.get("photo")
        if photo:
            photo_data = {
                "name": photo.name,
                "my_photo": photo.content_type,
                "data": base64.b64encode(photo.read()).decode("utf-8"),
            }

            new_doc["photo"] = photo_data
        new_doc["myanamme"] = request.POST.get("myanname")
        new_doc["engname"] = request.POST.get("engname")
        new_doc["nrc"] = request.POST.get("nrc")
        new_doc["birthDay"] = request.POST.get("birthDay")
        new_doc["nation"] = request.POST.get("nation")
        new_doc["rollno"] = request.POST.get("rollno")
        new_doc["score"] = request.POST.get("score")
        new_doc["passedseat_no"] = request.POST.get("passedseat_no")
        new_doc["currentseat_no"] = request.POST.get("currentseat_no")
        new_doc["myanfathername"] = request.POST.get("myanfathername")
        new_doc["engfathername"] = request.POST.get("fatherNameEng")
        new_doc["fathernrc"] = request.POST.get("fathernrc")
        new_doc["fathernation"] = request.POST.get("fathernation")
        new_doc["fatherjob"] = request.POST.get("fatherjob")
        new_doc["mothername"] = request.POST.get("mothername")
        new_doc["mothernrc"] = request.POST.get("mothernrc")
        new_doc["mothernation"] = request.POST.get("mothernation")
        new_doc["motherjob"] = request.POST.get("motherjob")
        new_doc["address"] = request.POST.get("address")
        new_doc["student_no"] = request.POST.get("student_no")
        new_doc["phone_no"] = request.POST.get("phone_no")
        new_doc["email"] = request.POST.get("email")

        try:
            collection.insert_one(new_doc)
            print("Error inerting data:", str(e))
            return JsonResponse({"message": "Data updated successfully"})
        except Exception as e:
            print("Inserted data:", new_doc["_id"])
            return JsonResponse({"message": "No matching document found"})
    else:
        return JsonResponse({"message": "No matching document found "})


# civil
@csrf_exempt
def add_student_third_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "rollno": request.POST.get("rollno"),
            "score": request.POST.get("score"),
            "passedseat_no": request.POST.get("passedseat_no"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "myanfathername": request.POST.get("myanfathername"),
            "engfathername": request.POST.get("engfathername"),
            "fathernrc": request.POST.get("fathernrc"),
            "fathernation": request.POST.get("fathernation"),
            "fatherjob": request.POST.get("fatherjob"),
            "mothername": request.POST.get("mothername"),
            "mothernrc": request.POST.get("mothernrc"),
            "mothernation": request.POST.get("mothernation"),
            "motherjob": request.POST.get("motherjob"),
            "address": request.POST.get("address"),
            "phone_no": request.POST.get("phone_no"),
            "student_no": request.POST.get("student_no"),
            "email": request.POST.get("email"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/t?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["third_civil"]

        """ photo_data = {
            "name": photo.name,
            "my_photo": photo.content_type,
            "data": base64.b64encode(photo.read()).decode("utf-8"),
        } """
        """ document = {**data, **photo_data} """

        ## Convert photo to base64 before storing it in MongoDB

        # Insert the document into the collection

        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# civil
@csrf_exempt
def student_list_fourth_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["fourth_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# civil register
@csrf_exempt
def match_burmese_data_fourth_year(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["fourth_year_civil_register"]
    collection2 = db["fourth_civil"]

    b = request.POST.get("passedseat_no", None)
    print("Seatno", b)
    matched_doc = collection2.find_one({"rollno": b})
    print(matched_doc)
    new_doc = {}
    if matched_doc:
        photo = request.FILES.get("photo")
        if photo:
            photo_data = {
                "name": photo.name,
                "my_photo": photo.content_type,
                "data": base64.b64encode(photo.read()).decode("utf-8"),
            }

            new_doc["photo"] = photo_data
        new_doc["myanamme"] = request.POST.get("myanname")
        new_doc["engname"] = request.POST.get("engname")
        new_doc["nrc"] = request.POST.get("nrc")
        new_doc["birthDay"] = request.POST.get("birthDay")
        new_doc["nation"] = request.POST.get("nation")
        new_doc["rollno"] = request.POST.get("rollno")
        new_doc["score"] = request.POST.get("score")
        new_doc["passedseat_no"] = request.POST.get("passedseat_no")
        new_doc["currentseat_no"] = request.POST.get("currentseat_no")
        new_doc["myanfathername"] = request.POST.get("myanfathername")
        new_doc["engfathername"] = request.POST.get("fatherNameEng")
        new_doc["fathernrc"] = request.POST.get("fathernrc")
        new_doc["fathernation"] = request.POST.get("fathernation")
        new_doc["fatherjob"] = request.POST.get("fatherjob")
        new_doc["mothername"] = request.POST.get("mothername")
        new_doc["mothernrc"] = request.POST.get("mothernrc")
        new_doc["mothernation"] = request.POST.get("mothernation")
        new_doc["motherjob"] = request.POST.get("motherjob")
        new_doc["address"] = request.POST.get("address")
        new_doc["student_no"] = request.POST.get("student_no")
        new_doc["phone_no"] = request.POST.get("phone_no")
        new_doc["email"] = request.POST.get("email")

        try:
            collection.insert_one(new_doc)
            print("Error inerting data:", str(e))
            return JsonResponse({"message": "Data updated successfully"})
        except Exception as e:
            print("Inserted data:", new_doc["_id"])
            return JsonResponse({"message": "No matching document found"})
    else:
        return JsonResponse({"message": "No matching document found "})


# civil add admin
@csrf_exempt
def add_student_fourth_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "rollno": request.POST.get("rollno"),
            "score": request.POST.get("score"),
            "passedseat_no": request.POST.get("passedseat_no"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "myanfathername": request.POST.get("myanfathername"),
            "engfathername": request.POST.get("engfathername"),
            "fathernrc": request.POST.get("fathernrc"),
            "fathernation": request.POST.get("fathernation"),
            "fatherjob": request.POST.get("fatherjob"),
            "mothername": request.POST.get("mothername"),
            "mothernrc": request.POST.get("mothernrc"),
            "mothernation": request.POST.get("mothernation"),
            "motherjob": request.POST.get("motherjob"),
            "address": request.POST.get("address"),
            "phone_no": request.POST.get("phone_no"),
            "student_no": request.POST.get("student_no"),
            "email": request.POST.get("email"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["fourth_civil"]

        """ photo_data = {
            "name": photo.name,
            "my_photo": photo.content_type,
            "data": base64.b64encode(photo.read()).decode("utf-8"),
        } """

        """ document = {**data, **photo_data} """

        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# civil
@csrf_exempt
def student_list_fifth_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["fifth_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# civil register
@csrf_exempt
def match_burmese_data_fifth_year(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["fifth_year_civil_register"]
    collection2 = db["fifth_civil"]

    b = request.POST.get("passedseat_no", None)
    print("Seatno", b)
    matched_doc = collection2.find_one({"rollno": b})
    print(matched_doc)
    new_doc = {}
    if matched_doc:
        photo = request.FILES.get("photo")
        if photo:
            photo_data = {
                "name": photo.name,
                "my_photo": photo.content_type,
                "data": base64.b64encode(photo.read()).decode("utf-8"),
            }

            new_doc["photo"] = photo_data
        new_doc["myanamme"] = request.POST.get("myanname")
        new_doc["engname"] = request.POST.get("engname")
        new_doc["nrc"] = request.POST.get("nrc")
        new_doc["birthDay"] = request.POST.get("birthDay")
        new_doc["nation"] = request.POST.get("nation")
        new_doc["rollno"] = request.POST.get("rollno")
        new_doc["score"] = request.POST.get("score")
        new_doc["passedseat_no"] = request.POST.get("passedseat_no")
        new_doc["currentseat_no"] = request.POST.get("currentseat_no")
        new_doc["myanfathername"] = request.POST.get("myanfathername")
        new_doc["engfathername"] = request.POST.get("fatherNameEng")
        new_doc["fathernrc"] = request.POST.get("fathernrc")
        new_doc["fathernation"] = request.POST.get("fathernation")
        new_doc["fatherjob"] = request.POST.get("fatherjob")
        new_doc["mothername"] = request.POST.get("mothername")
        new_doc["mothernrc"] = request.POST.get("mothernrc")
        new_doc["mothernation"] = request.POST.get("mothernation")
        new_doc["motherjob"] = request.POST.get("motherjob")
        new_doc["address"] = request.POST.get("address")
        new_doc["student_no"] = request.POST.get("student_no")
        new_doc["phone_no"] = request.POST.get("phone_no")
        new_doc["email"] = request.POST.get("email")

        try:
            collection.insert_one(new_doc)
            print("Error inerting data:", str(e))
            return JsonResponse({"message": "Data updated successfully"})
        except Exception as e:
            print("Inserted data:", new_doc["_id"])
            return JsonResponse({"message": "No matching document found"})
    else:
        return JsonResponse({"message": "No matching document found "})


# civil admin add
@csrf_exempt
def add_student_fifth_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "rollno": request.POST.get("rollno"),
            "score": request.POST.get("score"),
            "passedseat_no": request.POST.get("passedseat_no"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "myanfathername": request.POST.get("myanfathername"),
            "engfathername": request.POST.get("engfathername"),
            "fathernrc": request.POST.get("fathernrc"),
            "fathernation": request.POST.get("fathernation"),
            "fatherjob": request.POST.get("fatherjob"),
            "mothername": request.POST.get("mothername"),
            "mothernrc": request.POST.get("mothernrc"),
            "mothernation": request.POST.get("mothernation"),
            "motherjob": request.POST.get("motherjob"),
            "address": request.POST.get("address"),
            "phone_no": request.POST.get("phone_no"),
            "student_no": request.POST.get("student_no"),
            "email": request.POST.get("email"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["fifth_civil"]

        """ photo_data = {
            "name": photo.name,
            "my_photo": photo.content_type,
            "data": base64.b64encode(photo.read()).decode("utf-8"),
        } """

        """ document = {**data, **photo_data} """

        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# civil
@csrf_exempt
def student_list_sixth_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["final_year"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# civil register
@csrf_exempt
def match_burmese_data_sixth_year(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["sixth_year_civil_register"]
    collection2 = db["final_year"]

    b = request.POST.get("passedseat_no", None)
    print("Seatno", b)
    matched_doc = collection2.find_one({"rollno": b})
    print(matched_doc)
    new_doc = {}
    if matched_doc:
        photo = request.FILES.get("photo")
        if photo:
            photo_data = {
                "name": photo.name,
                "my_photo": photo.content_type,
                "data": base64.b64encode(photo.read()).decode("utf-8"),
            }

            new_doc["photo"] = photo_data
        new_doc["myanamme"] = request.POST.get("myanname")
        new_doc["engname"] = request.POST.get("engname")
        new_doc["nrc"] = request.POST.get("nrc")
        new_doc["birthDay"] = request.POST.get("birthDay")
        new_doc["nation"] = request.POST.get("nation")
        new_doc["rollno"] = request.POST.get("rollno")
        new_doc["score"] = request.POST.get("score")
        new_doc["passedseat_no"] = request.POST.get("passedseat_no")
        new_doc["currentseat_no"] = request.POST.get("currentseat_no")
        new_doc["myanfathername"] = request.POST.get("myanfathername")
        new_doc["engfathername"] = request.POST.get("fatherNameEng")
        new_doc["fathernrc"] = request.POST.get("fathernrc")
        new_doc["fathernation"] = request.POST.get("fathernation")
        new_doc["fatherjob"] = request.POST.get("fatherjob")
        new_doc["mothername"] = request.POST.get("mothername")
        new_doc["mothernrc"] = request.POST.get("mothernrc")
        new_doc["mothernation"] = request.POST.get("mothernation")
        new_doc["motherjob"] = request.POST.get("motherjob")
        new_doc["address"] = request.POST.get("address")
        new_doc["student_no"] = request.POST.get("student_no")
        new_doc["phone_no"] = request.POST.get("phone_no")
        new_doc["email"] = request.POST.get("email")

        try:
            collection.insert_one(new_doc)
            print("Error inerting data:", str(e))
            return JsonResponse({"message": "Data updated successfully"})
        except Exception as e:
            print("Inserted data:", new_doc["_id"])
            return JsonResponse({"message": "No matching document found"})
    else:
        return JsonResponse({"message": "No matching document found "})


# final year adding data
@csrf_exempt
def add_student_final_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "rollno": request.POST.get("rollno"),
            "score": request.POST.get("score"),
            "passedseat_no": request.POST.get("passedseat_no"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "myanfathername": request.POST.get("myanfathername"),
            "engfathername": request.POST.get("engfathername"),
            "fathernrc": request.POST.get("fathernrc"),
            "fathernation": request.POST.get("fathernation"),
            "fatherjob": request.POST.get("fatherjob"),
            "mothername": request.POST.get("mothername"),
            "mothernrc": request.POST.get("mothernrc"),
            "mothernation": request.POST.get("mothernation"),
            "motherjob": request.POST.get("motherjob"),
            "address": request.POST.get("address"),
            "phone_no": request.POST.get("phone_no"),
            "student_no": request.POST.get("student_no"),
            "email": request.POST.get("email"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["final_year"]

        """ photo_data = {
            "name": photo.name,
            "my_photo": photo.content_type,
            "data": base64.b64encode(photo.read()).decode("utf-8"),
        } """

        """ document = {**data, **photo_data} """
        result = collection.insert_one(data)
        """ result = collection.insert_one(photo_data) """

        """ result = collection.insert_one(document) """
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# signin
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        # Using pymongo to find the user by username
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )
        db = client["test"]
        collection = db["sign_up"]

        user = collection.find_one({"username": username, "password": password})

        if user:
            return JsonResponse({"username": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return HttpResponse("Method not allowed", status=405)


# signup
@csrf_exempt
def signup(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")  # ID received from the React front-end

        if username and password:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
            )
            db = client["test"]  # Replace <database_name> with your database name
            collection = db["sign_up"]
            user = {
                "username": username,
                "password": password,
            }
            collection.insert_one(user)
            client.close()
            return JsonResponse({"message": "User registered successfully"})
        else:
            return JsonResponse(
                {"error": "Username and password are required."}, status=400
            )
    return JsonResponse({"error": "Invalid request method."}, status=405)


# views.py
# admin sign up
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        google_id = data.get("googleId")

        user_data = {"username": username, "email": email, "googleId": google_id}

        result = collection.insert_one(user_data)
        return JsonResponse({"message": result})

    return JsonResponse({"message": "Invalid request method."})


# insert data
def insert(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
    )

    db = client["online_student_registration_db"]
    collection = db["second_year"]

    # Define the student data with Burmese text
    student_data = {
        "nameMyan": "mm",
        "nameEng": "ll",
        "NRC": "9/lawana9999",
        "birthDay": "1999-03",
    }

    # Insert the student data into the collection
    collection.insert_one(student_data)
    return JsonResponse({"messsage": "message inserted successfully"})


@api_view(["POST"])
def photo_upload_view(request):
    if request.method == "POST" and request.FILES.get("photo"):
        photo = request.FILES["photo"]
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["db"]
        photo_data = {
            "name": photo.name,
            "content_type": photo.content_type,
            "data": photo.read(),
        }
        result = collection.insert_one(photo_data)

        if result.inserted_id:
            return JsonResponse({"message": "Photo uploaded successfully."}, status=201)
        else:
            return JsonResponse({"message": "Failed to upload photo."}, status=500)
    else:
        return JsonResponse({"message": "Bad request."}, status=400)


@csrf_exempt
def update_student_admin_second_year(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )

    db = client["test"]
    collection = db["adm2nd"]  # Replace with the name of your collection

    if request.method == "PUT":
        try:
            # Extract the updated data from the request
            myanname = request.POST.get("myanname")
            engname = request.POST.get("engname")
            nrc = request.POST.get("nrc")
            birthDay = request.POST.get("birthDay")
            nation = request.POST.get("nation")
            rollno = request.POST.get("rollno")
            score = request.POST.get("score")
            passedseat_no = request.POST.get("passedseat_no")
            currentseat_no = request.POST.get("currentseat_no")
            myanfathername = request.POST.get("myanfathername")
            engfathername = request.POST.get("engfathername")
            fathernrc = request.POST.get("fathernrc")
            fathernation = request.POST.get("fathernation")
            fatherjob = request.POST.get("fatherjob")
            mothername = request.POST.get("mothername")
            mothernrc = request.POST.get("mothernrc")
            mothernation = request.POST.get("mothernation")
            motherjob = request.POST.get("motherjob")
            address = request.POST.get("address")
            phone_no = request.POST.get("phone_no")
            student_no = request.POST.get("student_no")
            email = request.POST.get("email")

            # Perform the update in the database
            collection.update_one(
                {"_id": student_id},
                {
                    "$set": {
                        "myanname": myanname,
                        "engname": engname,
                        "nrc": nrc,
                        "birthDay": birthDay,
                        "nation": nation,
                        "rollno": rollno,
                        "score": score,
                        "passedseat_no": passedseat_no,
                        "currentseat_no": currentseat_no,
                        "myanfathername": myanfathername,
                        "engfathername": engfathername,
                        "fathernrc": fathernrc,
                        "fathernation": fathernation,
                        "fatherjob": fatherjob,
                        "mothername": mothername,
                        "mothernrc": mothernrc,
                        "mothernation": mothernation,
                        "motherjob": motherjob,
                        "address": address,
                        "phone_no": phone_no,
                        "student_no": student_no,
                        "email": email,
                    }
                },
            )

            # Return a success response
            return JsonResponse({"message": "Student data updated successfully"})

        except Exception as e:
            print("Error occurred during update:", str(e))
            return JsonResponse({"error": "Error occurred during update"}, status=500)

    return JsonResponse({"message": "Method not allowed"}, status=405)


# fourth year adding data


# final year adding data
@csrf_exempt
def add_student_final_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "rollno": request.POST.get("rollno"),
            "score": request.POST.get("score"),
            "passedseat_no": request.POST.get("passedseat_no"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "myanfathername": request.POST.get("myanfathername"),
            "engfathername": request.POST.get("engfathername"),
            "fathernrc": request.POST.get("fathernrc"),
            "fathernation": request.POST.get("fathernation"),
            "fatherjob": request.POST.get("fatherjob"),
            "mothername": request.POST.get("mothername"),
            "mothernrc": request.POST.get("mothernrc"),
            "mothernation": request.POST.get("mothernation"),
            "motherjob": request.POST.get("motherjob"),
            "address": request.POST.get("address"),
            "phone_no": request.POST.get("phone_no"),
            "student_no": request.POST.get("student_no"),
            "email": request.POST.get("email"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["final_year"]

        """ photo_data = {
            "name": photo.name,
            "my_photo": photo.content_type,
            "data": base64.b64encode(photo.read()).decode("utf-8"),
        } """

        """ document = {**data, **photo_data} """
        result = collection.insert_one(data)
        """ result = collection.insert_one(photo_data) """

        ## Convert photo to base64 before storing it in MongoDB

        # Insert the document into the collection

        """ result = collection.insert_one(document) """
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# delete student data
@csrf_exempt
def delete_document(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["adm2nd"]

            # Find and delete the document with the provided ID
            result = collection.delete_one({"_id": student_id})
            if result.deleted_count > 0:
                return JsonResponse({"message": "Student deleted successfully"})
            else:
                return JsonResponse({"message": "Student not found"}, status=400)
        except Exception as e:
            print("Error", e)
            return JsonResponse(
                {"message": "An error occurred while deleting the student"}, status=500
            )
    # Return the number of deleted documents
    return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
def update_document(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["adm2nd"]

            print("Received student_id:", student_id)
            data = json.loads(request.body.decode("utf-8"))

            # Update the document with the provided student_id
            result = collection.update_one(
                {"_id": student_id},
                {"$set": data},
            )

            if result.matched_count > 0:
                return JsonResponse({"message": "Student updated successfully"})
            else:
                return JsonResponse({"message": "Student not found"}, status=400)
        except ValueError:
            return JsonResponse({"message": "Invalid student ID format"}, status=400)
        except Exception as e:
            print("Error", e)
            return JsonResponse(
                {"message": "An error occurred while updating the student"},
                status=500,
            )
    return JsonResponse({"message": "Method not allowed"}, status=405)


# checkbox
def store_checkbox_data(request):
    if request.method == "POST":
        data = json.loads(request.body)

        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["test_db"]

        # Replace 'checkbox_field' with the field name where you want to store the checkbox data
        collection.insert_one({"checkbox_field": data["checkboxData"]})

        return JsonResponse({"message": "Checkbox data stored successfully."})
    else:
        return JsonResponse({"error": "Invalid request method."})


# search name
@csrf_exempt
def search_by_myanname(request):
    if request.method == "GET":
        name = request.GET.get("name")

        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["first_year"]

        results = collection.find({"myanname": {"$regex": f"^{name}", "$options": "i"}})

        # Process the search results and create a JSON response
        data = []
        for result in results:
            data.append(
                {
                    "id": str(result["_id"]),
                    "myanname": result["myanname"],
                    # Add other fields as needed
                }
            )

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

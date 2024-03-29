import base64
from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from bson import ObjectId
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import FileUploadParser
from io import BytesIO

# Create your views here.


# show student list
def student_list(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test_db?retryWrites=true&w=majority"
    )
    db = client["test_db"]  # Replace <database_name> with your database name
    collection = db["test"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


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


# upload photo
# @csrf_exempt
# def upload_photo(request):
#     if request.method == "POST" and request.FILES.get("photo"):
#         photo = request.FILES["photo"]

#         client = MongoClient(
#             "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
#         )

#         db = client["online_student_registration_db"]
#         collection = db["second_year"]

#         photo_id = collection.insert_one({"photo": photo.read()}).inserted_id

#         return JsonResponse(
#             {"success": True, "message": "Photo uploaded successfully."}
#         )
#     else:
#         return JsonResponse(
#             {"success": False, "message": "Invalid request or missing photo"}
#         )


# adding student data for first year
@csrf_exempt
def add_student_first_year(request):
    if request.method == "POST":
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
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["db"]

        ## Convert photo to base64 before storing it in MongoDB

        # Insert the document into the collection
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# adding student data for second year
@csrf_exempt
def add_student_second_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "seatno": request.POST.get("seatno"),
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
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["test_db"]

        ## Convert photo to base64 before storing it in MongoDB

        # Insert the document into the collection
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# Third year
@csrf_exempt
def add_student_third_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "seatno": request.POST.get("seatno"),
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
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
        )

        db = client["online_student_registration_db"]
        collection = db["third_year"]

        ## Convert photo to base64 before storing it in MongoDB

        # Insert the document into the collection
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# fourth year adding data
@csrf_exempt
def add_student_fourth_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "seatno": request.POST.get("seatno"),
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
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
        )

        db = client["online_student_registration_db"]
        collection = db["fourth_year"]

        ## Convert photo to base64 before storing it in MongoDB

        # Insert the document into the collection
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# fifth year adding data
@csrf_exempt
def add_student_fifth_year(request):
    if request.method == "POST":
        data = {
            "myanname": request.POST.get("myanname"),
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "birthDay": request.POST.get("birthDay"),
            "nation": request.POST.get("nation"),
            "seatno": request.POST.get("seatno"),
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
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
        )

        db = client["online_student_registration_db"]
        collection = db["fifth_year"]

        ## Convert photo to base64 before storing it in MongoDB

        # Insert the document into the collection
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


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
            "seatno": request.POST.get("seatno"),
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
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
        )

        db = client["test"]
        collection = db["final_year"]

        ## Convert photo to base64 before storing it in MongoDB

        # Insert the document into the collection
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# delete student data
@csrf_exempt
def delete_document(request, doc_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
    )

    db = client["online_student_registration_db"]
    collection = db["second_year"]
    doc_id = request.POST.get("NRC")
    # Find and delete the document with the provided ID
    result = collection.delete_one({"NRC": doc_id})
    deleted_count = result.deleted_count
    # Return the number of deleted documents
    return JsonResponse({"message": f"{deleted_count} document(s) deleted."})


# this is for matching student data then add student data
@csrf_exempt
def match_burmese_data(request):
    # Get the user-posted Burmese data from the request

    # Connect to MongoDB Atlas
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["test_db"]

    b = request.POST.get("nameMyan", None)
    matched_doc = collection.find_one({"nameMyan": b})

    if matched_doc:
        c = request.POST.get("seatno", None)
        matched_doc = collection.find_one({"seatno": c})
        if matched_doc:
            matched_doc["nameEng"] = request.POST.get("nameEng")
            matched_doc["NRC"] = request.POST.get("NRC")
            matched_doc["birthDay"] = request.POST.get("birthDay")
            matched_doc["nation_religion"] = request.POST.get("nation_religion")
            matched_doc["grade10"] = request.POST.get("grade10")
            matched_doc["total_mark_g10"] = request.POST.get("total_mark_g10")
            matched_doc["passed_rollNo"] = request.POST.get("passed_rollNo")
            matched_doc["rollNo"] = request.POST.get("rollNo")
            matched_doc["fatherNameMyan"] = request.POST.get("fatherNameMyan")
            matched_doc["fatherNameEng"] = request.POST.get("fatherNameEng")
            matched_doc["fatherNation_religion"] = request.POST.get(
                "fatherNation_religion"
            )
            matched_doc["fatherJob"] = request.POST.get("fatherJob")
            matched_doc["motherName"] = request.POST.get("motherName")
            matched_doc["motherNRC"] = request.POST.get("motherNRC")
            matched_doc["momNation_religion"] = request.POST.get("momNation_religion")
            matched_doc["motherJob"] = request.POST.get("motherJob")
            matched_doc["address_phNo"] = request.POST.get("address_phNo")
            matched_doc["eassyaddress_phNo"] = request.POST.get("eassyaddress_phNo")
            matched_doc["university"] = request.POST.get("university")

            # Create a text index on the relevant fields
            collection.replace_one(
                {"_id": matched_doc["_id"]}, matched_doc
            )  # Replace field_name_1, field_name_2 with actual field names

            # Process or return the matching documents as needed
            return JsonResponse({"message": "Data updated successfully"})
        else:
            # No matching document found, return an error response
            return JsonResponse({"message": "No matching document found"})

    return JsonResponse({"message": "No matching document found"})


# this is for adminsite
@csrf_exempt
def admin_add_student_secondyear_IT(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
    )

    db = client["online_student_registration_db"]
    collection = db["second_year"]
    if request.method == "POST":
        data = {
            "ကျောင်းသား/ကျောင်းသူအမည်(မြန်မာလို)": request.POST.get(
                "ကျောင်းသား/ကျောင်းသူအမည်(မြန်မာလို)"
            ),
            "ကျောင်းသား/ကျောင်းသူအမည်(အင်္ဂလိပ်လို)": request.POST.get(
                "ကျောင်းသား/ကျောင်းသူအမည်(အင်္ဂလိပ်လို)"
            ),
            "နိုင်ငံသားစီစစ်ရေးအမှတ်": request.POST.get("နိုင်ငံသားစီစစ်ရေးအမှတ်"),
            "မွေးသက္ကရာဇ်(၁၀တန်းအောင်လက်မှတ်မွေးသက္ကရာဇ်ထည့်ရန်)": request.POST.get(
                "မွေးသက္ကရာဇ်(၁၀တန်းအောင်လက်မှတ်မွေးသက္ကရာဇ်ထည့်ရန်)"
            ),
            "လူမျိုး/ကိုးကွယ်သည့်ဘာသာ": request.POST.get("လူမျိုး/ကိုးကွယ်သည့်ဘာသာ"),
            "၁၀တန်းအောင်မြင်သည့်ခုံအမှတ်/ခုနှစ်": request.POST.get(
                "၁၀တန်းအောင်မြင်သည့်ခုံအမှတ်/ခုနှစ်"
            ),
            "၁၀ တန်းအမှတ်ပေါင်း": request.POST.get("၁၀ တန်းအမှတ်ပေါင်း"),
            "(အောင်မြင်ခဲ့သည့်အတန်း-ခုံအမှတ်)": request.POST.get(
                "(အောင်မြင်ခဲ့သည့်အတန်း-ခုံအမှတ်)"
            ),
            "(ယခုသင်တန်း-ခုံအမှတ်)": request.POST.get("(ယခုသင်တန်း-ခုံအမှတ်)"),
            "အဘအမည်(မြန်မာလို)": request.POST.get("အဘအမည်(မြန်မာလို)"),
            "အဘအမည်(အင်္ဂလိပ်လို)": request.POST.get("အဘအမည်(အင်္ဂလိပ်လို)"),
            "အဘ၏နိုင်ငံသားစီစစ်ရေးအမှတ်": request.POST.get(
                "အဘ၏နိုင်ငံသားစီစစ်ရေးအမှတ်"
            ),
            "လူမျိုး/ကိုးကွယ်သည့်ဘာသာ": request.POST.get("လူမျိုး/ကိုးကွယ်သည့်ဘာသာ"),
            "အဘ၏အလုပ်အကိုင်": request.POST.get("အဘ၏အလုပ်အကိုင်"),
            "အမိအမည်": request.POST.get("အမိအမည်"),
            "အမိ၏နိုင်ငံသားစီစစ်ရေးအမှတ်": request.POST.get(
                "အမိ၏နိုင်ငံသားစီစစ်ရေးအမှတ်"
            ),
            "လူမျိုး/ကိုးကွယ်သည့်ဘာသာ": request.POST.get("လူမျိုး/ကိုးကွယ်သည့်ဘာသာ"),
            "အမိ၏အလုပ်အကိုင်": request.POST.get("အမိ၏အလုပ်အကိုင်"),
            "မိဘနေရပ်လိပ်စာအပြည့်အစုံ/ဖုန်းနံပါတ်": request.POST.get(
                "မိဘနေရပ်လိပ်စာအပြည့်အစုံ/ဖုန်းနံပါတ်"
            ),
            "လွယ်ကူစွာဆက်သွယ်နိုင်သည့်လိပ်စာ/ဖုန်းနံပါတ်": request.POST.get(
                "လွယ်ကူစွာဆက်သွယ်နိုင်သည့်လိပ်စာ/ဖုန်းနံပါတ်"
            ),
            "ကျောင်းသား/ကျောင်းသူကျောင်းဝင်မှတ်ပုံတင်နံပါတ်": request.POST.get(
                "ကျောင်းသား/ကျောင်းသူကျောင်းဝင်မှတ်ပုံတင်နံပါတ်"
            ),
        }
        # Insert the document into the collection
        result = collection.insert_one(data)

        # Return the inserted document ID
        return JsonResponse({"id": str(result.inserted_id)})

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

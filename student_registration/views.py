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

# appname/views.py

from django.core.mail import EmailMessage
from django.http import JsonResponse

from django.core.mail import send_mail


# Email Confirmation for all year and major
@csrf_exempt
def send_confirmation_email(request):
    if request.method == "POST":
        data = json.loads(request.body)
        recipient_email = data.get("recipient_email")

        if not recipient_email:
            return JsonResponse({"message": "Recipient email is missing."}, status=400)
        # You can add more email-related logic here

        try:
            # Send the email
            subject = "Payment Information"
            message = "Your registration was successfully!"
            from_email = "myatmon@tumeiktila.edu.mm"
            recipient_list = [recipient_email]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.send()
            return JsonResponse({"message": "Email sent successfully"})
        except Exception as e:
            return JsonResponse(
                {"message": f"Email sending failed: {str(e)}"}, status=500
            )


# Delete New First Year Civil
@csrf_exempt
def delete_document_new_first_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["first_collection"]

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


# Update New First Year Civil
@csrf_exempt
def update_document_new_first_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["first_collection"]

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


# View New First Year Civil Data
@csrf_exempt
def view_first_civil_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["first_collection"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Add New First Year Civil Data for Admin
@csrf_exempt
def add_student_new_first_civil1_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "nrc": request.POST.get("nrc"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["first_collection"]
        counter_collection = db["counter_first"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter1": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter1", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})

    return JsonResponse({"message": "Method not allowed"}, status=405)


# Show In Table New First year Civil Data
@csrf_exempt
def student_list_new_first_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["first_collection"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Show In Table 10th Exam Result for Civil
@csrf_exempt
def exampassed_list(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["exam_result_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Delete 10th Exam Result for Civil
@csrf_exempt
def delete_document_exam_result(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["exam_result_civil"]

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


# Update 10th Exam result for Civil
@csrf_exempt
def update_document_exam_result(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["exam_result_civil"]

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


# Add 10th Exam Result Civil Data for Admin
@csrf_exempt
def add_student_new_first_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "nrc1": request.POST.get("nrc1"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["exam_result_civil"]
        counter_collection = db["exam_result_counter"]

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


# Delete Old First Year Civil
@csrf_exempt
def delete_document1(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_civil"]

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


# Update Old First Year Civil
@csrf_exempt
def update_document1(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_civil"]

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


# Delete Old First Year Civil
@csrf_exempt
def delete_document1(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_civil"]

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


# Update Old First Year Civil
@csrf_exempt
def update_document1(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_civil"]

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


# Delete Old First Year Civil
@csrf_exempt
def delete_document1(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_civil"]

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


# Delete Old First Year Civil
@csrf_exempt
def delete_document1(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_civil"]

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


# Delete Old First Year Civil
@csrf_exempt
def delete_document_old_first_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_ec"]

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


# Delete Old First Year Civil
@csrf_exempt
def delete_document_old_first_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_ep"]

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


# Delete Old First Year Civil
@csrf_exempt
def delete_document_old_first_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_it"]

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


# Delete Old First Year Civil
@csrf_exempt
def delete_document_old_first_mechanical(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_mechanical"]

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


# Update Old First Year Civil
@csrf_exempt
def update_document_old_first_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_ec"]

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


# Delete Old First Year Civil
@csrf_exempt
def update_document_old_first_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_ep"]

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


# Update Old First Year Civil
@csrf_exempt
def update_document_old_first_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_it"]

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


# Update Old First Year Civil
@csrf_exempt
def update_document_old_first_mechanical(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_first_mechanical"]

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


# Show In Table Old First Civil Data
@csrf_exempt
def student_list_first_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_first_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Show In Table Old First Civil Data
@csrf_exempt
def student_list_first_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_first_ec"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Show In Table Old First Civil Data
@csrf_exempt
def student_list_first_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_first_ep"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Show In Table Old First Civil Data
@csrf_exempt
def student_list_first_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_first_it"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Show In Table Old First Civil Data
@csrf_exempt
def student_list_first_mechanical(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_first_mechanical"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Add Old First Year Civil Data For Admin
@csrf_exempt
def add_student_old_first_civil(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_first_civil"]
        counter_collection = db["old_first_civil_counter"]

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


# Add Old First Year Civil Data For Admin
@csrf_exempt
def add_student_old_first_ec(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_first_ec"]
        counter_collection = db["old_first_ec_counter"]

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


# Add Old First Year Civil Data For Admin
@csrf_exempt
def add_student_old_first_ep(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_first_ep"]
        counter_collection = db["old_first_ep_counter"]

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


# Add Old First Year Civil Data For Admin
@csrf_exempt
def add_student_old_first_it(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_first_it"]
        counter_collection = db["old_first_it_counter"]

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


# Add Old First Year Civil Data For Admin
@csrf_exempt
def add_student_old_first_mechanical(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_first_mechanical"]
        counter_collection = db["old_first_mechanical_counter"]

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


# Update For Old Second Year civil Data
@csrf_exempt
def update_document_old_second_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_civil"]

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


@csrf_exempt
def update_document_old_second_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_ec"]

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


@csrf_exempt
def update_document_old_second_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_ep"]

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


@csrf_exempt
def update_document_old_second_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_it"]

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


@csrf_exempt
def update_document_old_second_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_me"]

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


# Delete Old Second Year Civil Data
@csrf_exempt
def delete_document_old_second_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_civil"]

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
def delete_document_old_second_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_ec"]

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
def delete_document_old_second_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_ep"]

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
def delete_document_old_second_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_it"]

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
def delete_document_old_second_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_second_me"]

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


# Show In Table For Old Second Year Civil Data
@csrf_exempt
def student_list_old_second_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_second_civil"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_second_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_second_ec"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_third_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_third_ec"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_fourth_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fourth_ec"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_fifth_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fifth_ec"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_sixth_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_sixth_ec"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_second_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_second_ep"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_third_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_third_ep"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_fourth_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fourth_ep"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_fifth_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fifth_ep"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_sixth_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_sixth_ep"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_second_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_second_me"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_second_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_second_it"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_third_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_third_it"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_fourth_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fourth_it"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_fifth_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fifth_it"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_sixth_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_sixth_it"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_third_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_third_me"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_fourth_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fourth_me"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_fifth_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fifth_me"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_old_sixth_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_sixth_me"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def add_student_old_sixth_me_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_sixth_me"]
        counter_collection = db["old_sixth_me_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_sixth_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_me"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_sixth_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_me"]

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


@csrf_exempt
def add_student_old_sixth_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_sixth_civil"]
        counter_collection = db["old_sixth_civil_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_sixth_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_civil"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_sixth_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_civil"]

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


@csrf_exempt
def add_student_old_sixth_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_sixth_ec"]
        counter_collection = db["old_sixth_ec_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_sixth_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_ec"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_sixth_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_ec"]

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


@csrf_exempt
def add_student_old_sixth_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_sixth_ep"]
        counter_collection = db["old_sixth_ep_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_sixth_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_ep"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_sixth_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_ep"]

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


@csrf_exempt
def add_student_old_sixth_it_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_sixth_it"]
        counter_collection = db["old_sixth_it_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_sixth_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_it"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_sixth_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_sixth_it"]

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


# Add Old Second Year Civil Data For Admin
@csrf_exempt
def add_student_old_second_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_second_civil"]
        counter_collection = db["old_second_civil_counter"]

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


@csrf_exempt
def add_student_old_second_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_second_ec"]
        counter_collection = db["old_second_ec_counter"]

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


@csrf_exempt
def add_student_old_second_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_second_ep"]
        counter_collection = db["old_second_ep_counter"]

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


@csrf_exempt
def add_student_old_second_it_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_second_it"]
        counter_collection = db["old_second_it_counter"]

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


@csrf_exempt
def add_student_old_second_me_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_second_me"]
        counter_collection = db["old_second_me_counter"]

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


# Show in Table For New Second Year Civil
def student_list_new_second_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection1"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Delete New Second Year Civil
@csrf_exempt
def delete_document(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection1"]

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


# Update For New Second Year Civil
@csrf_exempt
def update_document(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection1"]

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


# View New Second Year Civil Data
@csrf_exempt
def view_second_civil_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection1"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Add New Second Year Civil Data For Admin
@csrf_exempt
def add_student_new_second_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection1"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter1": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter1", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


# Show in Table For New Second Year EC
@csrf_exempt
def student_list_new_second_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec1"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_third_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec2"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_fourth_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec3"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_fifth_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec4"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_sixth_ec(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec5"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_second_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep1"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_third_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep2"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_fourth_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep3"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_fifth_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep4"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_sixth_ep(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep5"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_second_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it1"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_third_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it2"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_fourth_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it3"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_fifth_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it4"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_sixth_it(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it5"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_second_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me1"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_third_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me2"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_fourth_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me3"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_fifth_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me4"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def student_list_new_sixth_me(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me5"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Delete New Second Year EC
@csrf_exempt
def delete_document_new_second_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec1"]

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
def delete_document_new_third_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec2"]

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
def delete_document_new_fourth_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec3"]

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
def delete_document_new_fifth_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec4"]

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
def delete_document_new_sixth_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec5"]

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
def delete_document_new_second_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep1"]

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
def delete_document_new_third_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep2"]

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
def delete_document_new_fourth_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep3"]

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
def delete_document_new_fifth_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep4"]

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
def delete_document_new_sixth_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep5"]

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
def delete_document_new_second_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it1"]

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
def delete_document_new_third_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it2"]

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
def delete_document_new_fourth_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it3"]

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
def delete_document_new_fifth_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it4"]

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
def delete_document_new_sixth_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it5"]

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
def delete_document_new_second_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me1"]

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
def delete_document_new_third_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me2"]

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
def delete_document_new_fourth_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me3"]

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
def delete_document_new_fifth_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me4"]

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
def delete_document_new_sixth_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me5"]

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


# Update For New Second Year Civil
@csrf_exempt
def update_document_new_second_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec1"]

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


@csrf_exempt
def update_document_new_third_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec2"]

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


@csrf_exempt
def update_document_new_fourth_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec3"]

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


@csrf_exempt
def update_document_new_fifth_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec4"]

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


@csrf_exempt
def update_document_new_sixth_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ec5"]

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


@csrf_exempt
def update_document_new_second_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep1"]

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


@csrf_exempt
def update_document_new_third_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep2"]

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


@csrf_exempt
def update_document_new_fourth_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep3"]

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


@csrf_exempt
def update_document_new_fifth_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep4"]

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


@csrf_exempt
def update_document_new_sixth_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_ep5"]

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


@csrf_exempt
def update_document_new_second_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it1"]

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


@csrf_exempt
def update_document_new_third_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it2"]

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


@csrf_exempt
def update_document_new_fourth_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it3"]

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


@csrf_exempt
def update_document_new_fifth_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it4"]

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


@csrf_exempt
def update_document_new_sixth_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_it5"]

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


@csrf_exempt
def update_document_new_second_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me1"]

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


@csrf_exempt
def update_document_new_third_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me2"]

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


@csrf_exempt
def update_document_new_fourth_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me3"]

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


@csrf_exempt
def update_document_new_fifth_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me4"]

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


@csrf_exempt
def update_document_new_sixth_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection_me5"]

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


# View New Second Year EC Data
@csrf_exempt
def view_second_ec_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec1"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_third_ec_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec2"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_fourth_ec_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec3"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_fifth_ec_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec4"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_sixth_ec_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ec5"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_second_me_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me1"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_third_me_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me2"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_fourth_me_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me3"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_fifth_me_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me4"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_sixth_me_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_me5"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_second_ep_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep1"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_third_ep_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep2"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_fourth_ep_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep3"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_fifth_ep_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep4"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_sixth_ep_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_ep5"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_second_it_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it1"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_third_it_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it2"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_fourth_it_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it3"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_fifth_it_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it4"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_sixth_it_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection_it5"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Add New Second Year Civil Data For Admin
@csrf_exempt
def add_student_new_second_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ec1"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter6": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter6", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_third_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ec2"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter7": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter7", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_fourth_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ec3"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter8": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter8", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_fifth_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ec4"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter9": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter9", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_sixth_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ec5"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter10": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter10", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_second_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ep1"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter11": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter6", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_third_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ep2"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter12": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter7", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_fourth_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ep3"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter13": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter8", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_fifth_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ep4"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter14": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter9", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_sixth_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_ep5"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter15": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter10", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_second_it_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_it1"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter16": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter6", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_third_it_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_it2"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter17": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter7", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_fourth_it_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_it3"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter18": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter8", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_fifth_it_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_it4"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter19": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter9", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_sixth_it_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_it5"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter20": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter10", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_second_me_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_me1"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter21": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter6", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_third_me_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_me2"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter22": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter7", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_fourth_me_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_me3"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter23": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter8", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_fifth_me_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_me4"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter24": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter9", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


@csrf_exempt
def add_student_new_sixth_me_admin(request):
    if request.method == "POST":
        data = {
            "engname": request.POST.get("engname"),
            "currentseat_no": request.POST.get("currentseat_no"),
            "phone_no": request.POST.get("phone_no"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection_me5"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter25": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter10", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


# Show In Table For Old Third Civil Data
@csrf_exempt
def student_list_third_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["old_third_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Add Old Third Year Civil Data For Admin
@csrf_exempt
def add_student_old_third_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_third_civil"]
        counter_collection = db["old_third_civil_counter"]

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


# Delete Old Third Year Civil Data
@csrf_exempt
def delete_document_old_third_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_civil"]

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


# Update Old Third Year Civil
@csrf_exempt
def update_document_old_third_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_civil"]

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


@csrf_exempt
def add_student_old_third_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_third_ec"]
        counter_collection = db["old_third_ec_counter"]

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


# Delete Old Third Year Civil Data
@csrf_exempt
def delete_document_old_third_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_ec"]

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


# Update Old Third Year Civil
@csrf_exempt
def update_document_old_third_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_ec"]

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


@csrf_exempt
def add_student_old_third_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_third_ep"]
        counter_collection = db["old_third_ep_counter"]

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


# Delete Old Third Year Civil Data
@csrf_exempt
def delete_document_old_third_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_ep"]

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


# Update Old Third Year Civil
@csrf_exempt
def update_document_old_third_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_ep"]

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


@csrf_exempt
def add_student_old_third_it_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_third_it"]
        counter_collection = db["old_third_it_counter"]

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


# Delete Old Third Year Civil Data
@csrf_exempt
def delete_document_old_third_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_it"]

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


# Update Old Third Year Civil
@csrf_exempt
def update_document_old_third_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_it"]

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


@csrf_exempt
def add_student_old_third_me_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_third_me"]
        counter_collection = db["old_third_me_counter"]

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


# Delete Old Third Year Civil Data
@csrf_exempt
def delete_document_old_third_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_me"]

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


# Update Old Third Year Civil
@csrf_exempt
def update_document_old_third_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_third_me"]

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


# Delete New Third Year Civil Data
@csrf_exempt
def delete_document_new_third_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection2"]

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


# Update New Third Year Civil
@csrf_exempt
def update_document_New_third_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection2"]

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


# Add New Third Year Civil Data For Admin
@csrf_exempt
def add_student_new_third_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection2"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter2": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter2", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


# View New Third Year Civil Data
@csrf_exempt
def view_third_civil_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection2"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Show in Table For New Third Year Civil
def student_list_new_third_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection2"]
    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Show In Table For Old Fourth Civil Data
@csrf_exempt
def student_list_fourth_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fourth_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Add Old Fourth Year Civil Data For Admin
@csrf_exempt
def add_student_old_fourth_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fourth_civil"]
        counter_collection = db["old_fourth_civil_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fourth_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_civil"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fourth_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_civil"]

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


@csrf_exempt
def add_student_old_fourth_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fourth_ec"]
        counter_collection = db["old_fourth_ec_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fourth_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_ec"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fourth_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_ec"]

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


@csrf_exempt
def add_student_old_fourth_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fourth_ep"]
        counter_collection = db["old_fourth_ep_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fourth_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_ep"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fourth_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_ep"]

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


@csrf_exempt
def add_student_old_fourth_it_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fourth_it"]
        counter_collection = db["old_fourth_it_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fourth_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_it"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fourth_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_it"]

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


@csrf_exempt
def add_student_old_fourth_me_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fourth_me"]
        counter_collection = db["old_fourth_me_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fourth_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_me"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fourth_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fourth_me"]

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


# Show In Table For New Fourth Year Civil
@csrf_exempt
def student_list_new_fourth_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection3"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Delete New Fourth Year Civil Data
@csrf_exempt
def delete_document_new_fourth_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection3"]

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


# Update New Fourth Year Civil
@csrf_exempt
def update_document_new_fourth_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection3"]

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


# Add New Fourth Year Civil Data For Admin
@csrf_exempt
def add_student_new_fourth_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection3"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter3": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter3", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


# View New Fourth Year Civil Data
@csrf_exempt
def view_fourth_civil_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection3"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def student_list_new_fifth_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection4"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Delete New Fourth Year Civil Data
@csrf_exempt
def delete_document_new_fifth_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection4"]

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


# Update New Fourth Year Civil
@csrf_exempt
def update_document_new_fifth_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection4"]

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


# Add New Fourth Year Civil Data For Admin
@csrf_exempt
def add_student_new_fifth_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection4"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter4": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter4", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


# View New Fourth Year Civil Data
@csrf_exempt
def view_fifth_civil_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection4"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def student_list_new_sixth_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection5"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


# Delete New Fourth Year Civil Data
@csrf_exempt
def delete_document_new_sixth_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection5"]

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


# Update New Fourth Year Civil
@csrf_exempt
def update_document_new_sixth_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["insert_collection5"]

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


# Add New Fourth Year Civil Data For Admin
@csrf_exempt
def add_student_new_sixth_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["insert_collection5"]
        counter_collection = db["counter"]

        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {"counter5": 1}},
            upsert=True,
            return_document=True,
        )
        next_student_id = counter_doc.get("counter5", 1)
        data["_id"] = next_student_id
        result = collection.insert_one(data)
        print("Inserted ID:", result.inserted_id)
        print("inserted document", result)

        # Return the inserted document I
        return JsonResponse({"id": str(result.inserted_id)})


# View New Fourth Year Civil Data
@csrf_exempt
def view_sixth_civil_new(request, student_id):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["insert_collection5"]

    try:
        student = collection.find_one({"_id": int(student_id)})
        print("student", student)
        if student:
            return JsonResponse(student, json_dumps_params={"default": str})
        else:
            return JsonResponse({"error": "Student not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# civil
@csrf_exempt
def student_list_fifth_civil(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_fifth_civil"]

    students = list(collection.find())
    serialized_students = []
    for student in students:
        student["_id"] = str(student["_id"])
        serialized_students.append(student)
    return JsonResponse(
        {"students": serialized_students}, json_dumps_params={"default": str}
    )


@csrf_exempt
def add_student_old_fifth_ec_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fifth_ec"]
        counter_collection = db["old_fifth_ec_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fifth_ec(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_ec"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fifth_ec(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_ec"]

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


@csrf_exempt
def add_student_old_fifth_civil_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fifth_civil"]
        counter_collection = db["old_fifth_civil_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fifth_civil(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_civil"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fifth_civil(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_civil"]

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


@csrf_exempt
def add_student_old_fifth_ep_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fifth_ep"]
        counter_collection = db["old_fifth_ep_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fifth_ep(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_ep"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fifth_ep(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_ep"]

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


@csrf_exempt
def add_student_old_fifth_it_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fifth_it"]
        counter_collection = db["old_fifth_it_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fifth_it(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_it"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fifth_it(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_it"]

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


@csrf_exempt
def add_student_old_fifth_me_admin(request):
    if request.method == "POST":
        data = {
            "engname1": request.POST.get("engname1"),
            "rollno": request.POST.get("rollno"),
            "phone_no1": request.POST.get("phone_no1"),
        }
        """ photo = request.FILES["photo"] """
        print("Received data:", data)
        client = MongoClient(
            "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority",
            connectTimeoutMS=30000,
        )

        db = client["test"]
        collection = db["old_fifth_me"]
        counter_collection = db["old_fifth_me_counter"]

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


# Delete Old Fourth Year Civil Data
@csrf_exempt
def delete_document_old_fifth_me(request, student_id):
    if request.method == "DELETE":
        try:
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_me"]

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


# Update Old Fourth Year Civil
@csrf_exempt
def update_document_old_fifth_me(request, student_id):
    if request.method == "PATCH":
        try:
            student_id = int(student_id)
            client = MongoClient(
                "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/online_student_registration_db?retryWrites=true&w=majority"
            )

            db = client["test"]
            collection = db["old_fifth_me"]

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


# civil register
@csrf_exempt
def match_burmese_data_fifth_year(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    collection = db["fifth_year_civil_register"]
    collection2 = db["old_fifth_civil"]

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
        new_doc["myanname"] = request.POST.get("myanname")
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


# Sign In For Admin
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


# Sign Up For Admin
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


# Show in Table Old First Year Civil
def student_list(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]  # Replace <database_name> with your database name
    collection = db["old_first_civil"]
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


@csrf_exempt
def match_burmese_data(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    # Civil
    insert_collection1 = db["new_second_civil"]
    insert_collection2 = db["third_year_civil_student"]
    insert_collection3 = db["fourth_year_civil_student"]
    insert_collection4 = db["fifth_year_civil_student"]
    insert_collection5 = db["sixth_year_civil_student"]
    collection0 = db["old_first_civil"]
    collection1 = db["old_second_civil"]
    collection2 = db["old_third_civil"]
    collection3 = db["old_fourth_civil"]
    collection4 = db["old_fifth_civil"]

    # ec
    insert_collection_ec1 = db["new_second_ec"]
    insert_collection_ec2 = db["third_year_ec_student"]
    insert_collection_ec3 = db["fourth_year_ec_student"]
    insert_collection_ec4 = db["fifth_year_ec_student"]
    insert_collection_ec5 = db["sixth_year_ec_student"]
    ec_collection1 = db["old_first_ec"]
    ec_collection2 = db["old_second_ec"]
    ec_collection3 = db["old_third_ec"]
    ec_collection4 = db["old_fourth_ec"]
    ec_collection5 = db["old_fifth_ec"]

    insert_collection_ep1 = db["new_second_ep"]
    insert_collection_ep2 = db["third_year_ep_student"]
    insert_collection_ep3 = db["fourth_year_ep_student"]
    insert_collection_ep4 = db["fifth_year_ep_student"]
    insert_collection_ep5 = db["sixth_year_ep_student"]
    ep_collection1 = db["old_first_ep"]
    ep_collection2 = db["old_second_ep"]
    ep_collection3 = db["old_third_ep"]
    ep_collection4 = db["old_fourth_ep"]
    ep_collection5 = db["old_fifth_ep"]

    insert_collection_it1 = db["new_second_ec"]
    insert_collection_it2 = db["third_year_ec_student"]
    insert_collection_it3 = db["fourth_year_ec_student"]
    insert_collection_it4 = db["fifth_year_ec_student"]
    insert_collection_it5 = db["sixth_year_ec_student"]
    it_collection1 = db["old_first_ec"]
    it_collection2 = db["old_second_ec"]
    it_collection3 = db["old_third_ec"]
    it_collection4 = db["old_fourth_ec"]
    it_collection5 = db["old_fifth_ec"]

    insert_collection_mechanical1 = db["new_second_mechanical"]
    insert_collection_mechanical2 = db["third_year_mechanical_student"]
    insert_collection_mechanical3 = db["fourth_year_mechanical_student"]
    insert_collection_mechanical4 = db["fifth_year_mechanical_student"]
    insert_collection_mechanical5 = db["sixth_year_mechanical_student"]
    mechanical_collection1 = db["old_first_mechanical"]
    mechanical_collection2 = db["old_second_mechanical"]
    mechanical_collection3 = db["old_third_mechanical"]
    mechanical_collection4 = db["old_fourth_mechanical"]
    mechanical_collection5 = db["old_fifth_mechanical"]

    b = request.POST.get("passedseat_no", None)
    print("Seatno", b)
    # civil
    matched_doc0 = collection0.find_one({"rollno": b})
    matched_doc = collection1.find_one({"rollno": b})
    matched_doc1 = collection2.find_one({"rollno": b})
    matched_doc2 = collection3.find_one({"rollno": b})
    matched_doc3 = collection4.find_one({"rollno": b})

    # ec
    matched_ec = ec_collection1.find_one({"rollno": b})
    matched_ec1 = ec_collection2.find_one({"rollno": b})
    matched_ec2 = ec_collection3.find_one({"rollno": b})
    matched_ec3 = ec_collection4.find_one({"rollno": b})
    matched_ec4 = ec_collection5.find_one({"rollno": b})

    # ep
    matched_ep = ep_collection1.find_one({"rollno": b})
    matched_ep1 = ep_collection2.find_one({"rollno": b})
    matched_ep2 = ep_collection3.find_one({"rollno": b})
    matched_ep3 = ep_collection4.find_one({"rollno": b})
    matched_ep4 = ep_collection5.find_one({"rollno": b})

    # it
    matched_it = it_collection1.find_one({"rollno": b})
    matched_it1 = it_collection2.find_one({"rollno": b})
    matched_it2 = it_collection3.find_one({"rollno": b})
    matched_it3 = it_collection4.find_one({"rollno": b})
    matched_it4 = it_collection5.find_one({"rollno": b})

    # ec
    matched_mechanical = mechanical_collection1.find_one({"rollno": b})
    matched_mechanical1 = mechanical_collection2.find_one({"rollno": b})
    matched_mechanical2 = mechanical_collection3.find_one({"rollno": b})
    matched_mechanical3 = mechanical_collection4.find_one({"rollno": b})
    matched_mechanical4 = mechanical_collection5.find_one({"rollno": b})

    new_doc = {}

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
    new_doc["seatno"] = request.POST.get("seatno")
    new_doc["score"] = request.POST.get("score")
    new_doc["passedseat_no"] = request.POST.get("passedseat_no")
    new_doc["currentseat_no"] = request.POST.get("currentseat_no")
    new_doc["myanfathername"] = request.POST.get("myanfathername")
    new_doc["engfathername"] = request.POST.get("engfathername")
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
    new_doc["fee"] = request.POST.get("fee")

    target_collection_name = determine_target_collection(
        matched_doc0,
        matched_doc,
        matched_doc1,
        matched_doc2,
        matched_doc3,
        matched_ec,
        matched_ec1,
        matched_ec2,
        matched_ec3,
        matched_ec4,
        matched_ep,
        matched_ep1,
        matched_ep2,
        matched_ep3,
        matched_ep4,
        matched_it,
        matched_it1,
        matched_it2,
        matched_it3,
        matched_it4,
        matched_mechanical,
        matched_mechanical1,
        matched_mechanical2,
        matched_mechanical3,
        matched_mechanical4,
    )
    counter_collection = db["counter"]

    counter_field_map = {
        "insert_collection1": "counter1",
        "insert_collection2": "counter2",
        "insert_collection3": "counter3",
        "insert_collection4": "counter4",
        "insert_collection5": "counter5",
        "insert_collection_ec1": "counter6",
        "insert_collection_ec2": "counter7",
        "insert_collection_ec3": "counter8",
        "insert_collection_ec4": "counter9",
        "insert_collection_ec5": "counter10",
        "insert_collection_ep1": "counter11",
        "insert_collection_ep2": "counter12",
        "insert_collection_ep3": "counter13",
        "insert_collection_ep4": "counter14",
        "insert_collection_ep5": "counter15",
        "insert_collection_it1": "counter16",
        "insert_collection_it2": "counter17",
        "insert_collection_it3": "counter18",
        "insert_collection_it4": "counter19",
        "insert_collection_it5": "counter20",
        "insert_collection_mechanical1": "counter21",
        "insert_collection_mechanical2": "counter22",
        "insert_collection_mechanical3": "counter23",
        "insert_collection_mechanical4": "counter24",
        "insert_collection_mechanical5": "counter25",
    }

    counter_field = counter_field_map.get(target_collection_name)

    if counter_field:
        # Increment the respective counter and get the next _id value
        counter_collection = db["counter"]
        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {counter_field: 1}},
            upsert=True,
            return_document=True,
        )
        next_doc_id = counter_doc.get(counter_field, 1)

        # Create a new_doc with the generated _id
        new_doc["_id"] = next_doc_id
    print("Data", new_doc)

    try:
        target_collection = db[target_collection_name]
        print("target_collection", target_collection)
        target_collection.insert_one(new_doc)
        print("Error inerting data:", str(e))
        return JsonResponse({"message": "Data updated successfully"})
    except Exception as e:
        print("Inserted data:", new_doc["_id"])
        return JsonResponse({"message": "No matching document found"})


def determine_target_collection(
    matched_doc0,
    matched_doc,
    matched_doc1,
    matched_doc2,
    matched_doc3,
    matched_ec,
    matched_ec1,
    matched_ec2,
    matched_ec3,
    matched_ec4,
    matched_ep,
    matched_ep1,
    matched_ep2,
    matched_ep3,
    matched_ep4,
    matched_it,
    matched_it1,
    matched_it2,
    matched_it3,
    matched_it4,
    matched_mechanical,
    matched_mechanical1,
    matched_mechanical2,
    matched_mechanical3,
    matched_mechanical4,
):
    # Implement your logic here to determine the target collection name based on the matched documents
    # For example, you can use the matched documents to decide the target collection
    if matched_doc0:
        return "insert_collection1"
    elif matched_doc:
        return "insert_collection2"
    elif matched_doc1:
        return "insert_collection3"
    elif matched_doc2:
        return "insert_collection4"
    elif matched_doc3:
        return "insert_collection5"
    elif matched_ec:
        return "insert_collection_ec1"
    elif matched_ec1:
        return "insert_collection_ec2"
    elif matched_ec2:
        return "insert_collection_ec3"
    elif matched_ec3:
        return "insert_collection_ec4"
    elif matched_ec4:
        return "insert_collection_ec5"
    elif matched_ep:
        return "insert_collection_ep1"
    elif matched_ep1:
        return "insert_collection_ep2"
    elif matched_ep2:
        return "insert_collection_ep3"
    elif matched_ep3:
        return "insert_collection_ep4"
    elif matched_ep4:
        return "insert_collection_ep5"
    elif matched_it:
        return "insert_collection_it1"
    elif matched_it1:
        return "insert_collection_it2"
    elif matched_it2:
        return "insert_collection_it3"
    elif matched_it3:
        return "insert_collection_it4"
    elif matched_it4:
        return "insert_collection_it5"
    elif matched_mechanical:
        return "insert_collection_mechanical1"
    elif matched_mechanical1:
        return "insert_collection_mechanical2"
    elif matched_mechanical2:
        return "insert_collection_mechanical3"
    elif matched_mechanical3:
        return "insert_collection_mechanical4"
    elif matched_mechanical4:
        return "insert_collection_mechanical5"
    else:
        return "error"


# Register For New First Year Civil
@csrf_exempt
def match_burmese_data_first_year(request):
    client = MongoClient(
        "mongodb+srv://myatmonthantorg:myatmonthant123@cluster0.hagfqf4.mongodb.net/test?retryWrites=true&w=majority"
    )
    db = client["test"]
    first_collection = db["first_year_civil_student"]

    old_first_collection = db["exam_result_civil"]

    b = request.POST.get("nrc", None)
    print("nrc", b)
    matched_doc_civil = old_first_collection.find_one({"nrc1": b})

    print("matched", matched_doc_civil)
    new_doc = {}

    photo = request.FILES.get("photo")
    if photo:
        photo_data = {
            "name": photo.name,
            "my_photo": photo.content_type,
            "data": base64.b64encode(photo.read()).decode("utf-8"),
        }

        new_doc["photo"] = photo_data
    new_doc["myanname"] = request.POST.get("myanname")
    new_doc["engname"] = request.POST.get("engname")
    new_doc["nrc"] = request.POST.get("nrc")
    new_doc["birthDay"] = request.POST.get("birthDay")
    new_doc["nation"] = request.POST.get("nation")
    new_doc["seatno"] = request.POST.get("seatno")
    new_doc["department"] = request.POST.get("department")
    new_doc["score"] = request.POST.get("score")
    new_doc["myanfathername"] = request.POST.get("myanfathername")
    new_doc["engfathername"] = request.POST.get("engfathername")
    new_doc["fathernrc"] = request.POST.get("fathernrc")
    new_doc["fathernation"] = request.POST.get("fathernation")
    new_doc["fatherjob"] = request.POST.get("fatherjob")
    new_doc["mothername"] = request.POST.get("mothername")
    new_doc["mothernrc"] = request.POST.get("mothernrc")
    new_doc["mothernation"] = request.POST.get("mothernation")
    new_doc["motherjob"] = request.POST.get("motherjob")
    new_doc["address"] = request.POST.get("address")
    new_doc["phone_no"] = request.POST.get("phone_no")
    new_doc["email"] = request.POST.get("email")
    new_doc["selectedValue"] = request.POST.get("selectedValue")
    new_doc["selectedValue2"] = request.POST.get("selectedValue2")
    new_doc["selectedValue3"] = request.POST.get("selectedValue3")
    new_doc["selectedValue4"] = request.POST.get("selectedValue4")
    new_doc["selectedValue5"] = request.POST.get("selectedValue5")
    new_doc["fee"] = request.POST.get("fee")

    target_collection_name_first = determine_target_collection_first(
        matched_doc_civil,
    )

    counter_collection = db["counter_first"]

    counter_field_map = {
        "first_collection": "counter1",
    }

    counter_field = counter_field_map.get(target_collection_name_first)

    if counter_field:
        # Increment the respective counter and get the next _id value
        counter_collection = db["counter_first"]
        counter_doc = counter_collection.find_one_and_update(
            {"_id": "counters"},
            {"$inc": {counter_field: 1}},
            upsert=True,
            return_document=True,
        )
        next_doc_id = counter_doc.get(counter_field, 1)

        # Create a new_doc with the generated _id
        new_doc["_id"] = next_doc_id

        print("Data", new_doc)
    try:
        target_collection = db[target_collection_name_first]
        print("target_collection", target_collection)
        target_collection.insert_one(new_doc)
        print("Error inerting data:", str(e))

        return JsonResponse({"message": "Data updated successfully"})
    except Exception as e:
        print("Inserted data:", new_doc["_id"])
        return JsonResponse({"message": "No matching document found"})


def determine_target_collection_first(
    matched_doc_civil,
):
    # Implement your logic here to determine the target collection name based on the matched documents
    # For example, you can use the matched documents to decide the target collection
    if matched_doc_civil:
        return "first_collection"
    else:
        return "first_collection"

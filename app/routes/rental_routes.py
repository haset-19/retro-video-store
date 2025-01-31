from app import db
from app.models.customer import Customer
from .customer_routes import customer_bp
from .video_routes import video_bp
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response,request, abort
from dotenv import load_dotenv
import os
from datetime import date, timedelta, datetime


load_dotenv()
rental_bp = Blueprint("rental", __name__,url_prefix="/rentals")

#Helper function
def valid_int(number):
    try:
        return int(number)     
    except:
        abort(make_response({"error": f"{number} must be an int"}, 400))
   
#Helper function
def get_object_from_id(obj, id):
    id = valid_int(id) 
    obj1 = obj.query.get(id)
    if obj1:
        return obj1
    else:       
        abort(make_response(jsonify({"message": f"{obj.__str__(obj)} {id} was not found"}), 404))
#Helper function
def response_dict(obj,  available_inventory):  
    return {
        "customer_id": obj.customer_id,
        "video_id": obj.video_id,
        "videos_checked_out_count": obj.videos_checked_out_count,
        "available_inventory":available_inventory,
        "due_date" : obj.calculate_due_date(),
        "checked_in_status":obj.checked_in
        }

@rental_bp.route("/check-out", methods=["POST"])
def create_customer_video():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response({"message" : "bad request"}, 400)   
    else:
        customer_id = request_body["customer_id"]
        video_id = request_body["video_id"]
        get_object_from_id(Customer, customer_id)
        video_to_be_checked_out = get_object_from_id(Video, video_id)
        total_inventory = video_to_be_checked_out.total_inventory
        new_rental = Rental(customer_id=customer_id, video_id=video_id)
        if "videos_checked_out_count" in request_body:
            new_rental.videos_checked_out_count = request_body["videos_checked_out_count"]
        available_inventory = total_inventory - new_rental.videos_checked_out_count
        video_to_be_checked_out.total_inventory = available_inventory

        if total_inventory < new_rental.videos_checked_out_count:
            return jsonify({"message":"Could not perform checkout"}), 400   
        else:
                db.session.add(new_rental)
                db.session.commit()
        
        return response_dict(new_rental, available_inventory)


@rental_bp.route("/check-in", methods=["POST"])
def checkin_video():
    
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response({"message" : "bad request"}, 400)
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    get_object_from_id(Customer, customer_id)
    get_object_from_id(Video, video_id)
    rental_record = db.session.query(Rental).filter(Rental.customer_id==customer_id,Rental.video_id== Rental.video_id).first()
    if not rental_record:
            return make_response({"message": "No outstanding rentals for customer 1 and video 1"}, 400)
    else:
        this_video = Video.query.get(video_id)
        total_inventory = this_video.total_inventory
        available_inventory = total_inventory + rental_record.videos_checked_out_count      
        rental_record.videos_checked_out_count = rental_record.videos_checked_out_count - 1 #previously\
        # # checked out count minus the count customer returned
        rental_record.checked_in = True
        this_video.total_inventory = available_inventory
        response = response_dict(rental_record, available_inventory)
        db.session.commit()

        return make_response(response)


@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def rentals_by_customers(customer_id):

    one_customer = get_object_from_id(Customer, customer_id) 
    cust_videos = [video.to_dict() for video in one_customer.videos]
    return make_response(jsonify(cust_videos))


@video_bp.route("/<video_id>/rentals", methods=["GET"])
def rentals_by_video(video_id):
    one_video = get_object_from_id(Video, video_id)
    video_customers = [customer.to_dict() for customer in one_video.customers]
    return make_response(jsonify(video_customers))

@rental_bp.route("/overdue", methods=["GET"])
def get_overdue_rentals():
    response_list = Rental.query.all()
    return_overdues = []
    overdue_list = [rental for rental in response_list if rental.calculate_due_date() < datetime.today()]
    for rental in overdue_list:
        customer = Customer.query.get(rental.customer_id)
        video = Video.query.get(rental.video_id)
        return_overdues.append({"video_id":rental.video_id, "customer_id":rental.customer_id, "title":video.title,
        "name":customer.name, "postal_code":customer.postal_code, "checkout_date":rental.rental_date, "due_date":rental.calculate_due_date()})
       
    return make_response(jsonify(return_overdues))
    
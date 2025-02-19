from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_cors import CORS
import logging
import os
import speech_recognition as sr
import tempfile
from datetime import datetime, UTC
from models import *
import json
import openai
import haversine as hs
from geopy.distance import geodesic as GD
from datetime import datetime, timedelta
from sqlalchemy import and_
import time
import pytz




BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'audio_reports')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created audio reports directory at: {UPLOAD_FOLDER}")


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False  # Preserve JSON key order
CORS(app)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

logging.basicConfig(
    filename='emergency_reports.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def wait_for_db(retries=5, delay=2):
    with app.app_context():
        for attempt in range(retries):
            try:
                db.create_all()
                print(f"Database connection successful! (Attempt {attempt + 1})")
                print(f"Current time (UTC): 2025-02-17 00:16:55")
                print(f"Current user: nicknet06")
                return True
            except OperationalError as e:
                if attempt == retries - 1:
                    print(f"Could not connect to database after {retries} attempts: {e}")
                    raise
                print(f"Database connection attempt {attempt + 1} failed, retrying in {delay} seconds...")
                time.sleep(delay)
        return False


# def bind_service_resources(service, required_specialties, required_equipment):
#     """
#     Bind required equipment and specialties for a service for 6 hours.
#     Returns a tuple of (success, message).
#     """
#     try:
#         current_time = datetime.utcnow()
#         end_time = current_time + timedelta(hours=6)
#
#         available_personnel = Personnel.query.filter(
#             and_(
#                 Personnel.service_id == service.id,
#                 Personnel.status == 'on-duty',
#                 Personnel.speciality.in_(required_specialties)
#             )
#         ).all()
#
#         available_equipment = Equipment.query.filter(
#             and_(
#                 Equipment.service_id == service.id,
#                 Equipment.name.in_(required_equipment),
#                 Equipment.available > 0
#             )
#         ).all()
#
#         found_specialties = set(p.speciality for p in available_personnel)
#         found_equipment = set(e.name for e in available_equipment)
#
#         missing_specialties = set(required_specialties) - found_specialties
#         missing_equipment = set(required_equipment) - found_equipment
#
#         if missing_specialties or missing_equipment:
#             return (False, f"Missing resources - Specialties: {missing_specialties}, Equipment: {missing_equipment}")
#
#         for personnel in available_personnel:
#             resource_request = ResourceRequest(
#                 service_id=service.id,
#                 personnel_id=personnel.id,
#                 requester='Emergency System',
#                 purpose='Emergency Response',
#                 start_time=current_time,
#                 end_time=end_time,
#                 status='approved'
#             )
#             db.session.add(resource_request)
#
#         for equipment in available_equipment:
#             equipment.available -= 1
#
#             resource_request = ResourceRequest(
#                 service_id=service.id,
#                 equipment_id=equipment.id,
#                 requester='Emergency System',
#                 purpose='Emergency Response',
#                 start_time=current_time,
#                 end_time=end_time,
#                 status='approved'
#             )
#             db.session.add(resource_request)
#
#         db.session.commit()
#         return (True, "Resources successfully bound for 6 hours")
#
#     except Exception as e:
#         db.session.rollback()
#         return (False, f"Error binding resources: {str(e)}")
@app.route('/')
def home():
    return render_template('home.html',
                           current_time="2025-02-17 00:16:55",
                           current_user="nicknet06")


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        try:
            logging.info("Received chat POST request")
            logging.info(f"Form data: {request.form}")

            name = request.form.get('name', 'Anonymous')
            contact = request.form.get('contact', 'Not provided')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            description = request.form.get('description')
            audio_filename = request.form.get('audio_filename')

            logging.info(f"Processing emergency report with audio: {audio_filename}")
            name = request.form.get('name', 'Anonymous')
            contact = request.form.get('contact', 'Not provided')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            description = request.form.get('description')
            audio_filename = request.form.get('audio_filename')

            if not description and not audio_filename:
                raise ValueError("Either description or audio recording is required")

            report = EmergencyReport(
                name=name,
                contact=contact,
                latitude=latitude,
                longitude=longitude,
                description=description,
                audio_filename=audio_filename
            )

            try:
                db.session.add(report)
                db.session.commit()
                logging.info(f"Emergency report saved with ID: {report.id}")
            except Exception as db_error:
                db.session.rollback()
                logging.error(f"Database error: {str(db_error)}")
                raise
            print("process started")
            client = openai.OpenAI(api_key = "your openai api key")

            system_message = """You are an emergency response AI assistant. Analyze the emergency situation and provide:
                        1. Verification if it's a genuine emergency (true/false) (the field name is genuine_emergency)(type boolean)
                        2. Severity level (1-5, where 5 is most severe) (the field name is severity_level)(type int)
                        3. Required services (hospital/police/fire) (the field name is required_services) (type array of strings)
                        4. Required specialties choose from here(Emergency Medicine,Pediatrics,Surgery,Cardiology,Traffic,Investigation,Patrol,Special Operations,Hazmat,Rescue,Emergency Medical,Firefighting) (the field name is required_specialties)(type array of strings)
                        5. Required equipment choose from here (MRI Machine,X-Ray Machine,Ventilator,Body Camera,Radar Gun,Fire Hose,Breathing Apparatus,Thermal Camera) (the field name is required_equipment)(type array of strings)
                        6. Brief response for the user, how to handle the situation (the field name is response)(string)
                        7. First assesment of the situation so the emergency services be prepared(the field name is assessment)(string)
                        Format the response as JSON."""

            user_message = f"""Location: {latitude}, {longitude}
                        Description: {description}
                        """

            # Get AI assessment
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"}
            )

            # # Parse AI response
            ai_assessment = json.loads(response.choices[0].message.content)
            # print(ai_assessment)
            # with open("copy.txt", "w") as file:
            #     file.write(str(ai_assessment))
            location = f"coordinates: {latitude}, {longitude}" if latitude and longitude else "location pending"

            services = []
            for service_type in ai_assessment["required_services"]:
                try:
                    # First, get all active services of the required type
                    active_services = EmergencyService.query.filter_by(
                        service_type=service_type,
                        is_active=True
                    ).all()

                    if not active_services:
                        logging.warning(f"No active {service_type} services found")
                        continue

                    try:
                        user_lat = float(latitude) if latitude else None
                        user_lng = float(longitude) if longitude else None
                    except (ValueError, TypeError) as e:
                        logging.error(f"Error converting coordinates: {e}")
                        user_lat = None
                        user_lng = None

                    if user_lat and user_lng:
                        # Sort services by distance
                        sorted_services = sorted(
                            active_services,
                            key=lambda s: GD(
                                (float(s.latitude), float(s.longitude)),
                                (user_lat, user_lng)
                            ).km
                        )

                        # Get the two closest services
                        closest_services = sorted_services[:2]

                        if len(closest_services) > 0:
                            # Start with the closest service
                            selected_service = closest_services[0]

                            if len(closest_services) > 1:
                                # Compare required specialties with service capabilities
                                service_matches = []
                                for service in closest_services:
                                    # Get personnel with matching specialties
                                    matching_specialties = Personnel.query.filter(
                                        Personnel.service_id == service.id,
                                        Personnel.status == 'on-duty',
                                        Personnel.speciality.in_(ai_assessment.get("required_specialties", []))
                                    ).count()

                                    # Get available equipment
                                    matching_equipment = Equipment.query.filter(
                                        Equipment.service_id == service.id,
                                        Equipment.name.in_(ai_assessment.get("required_equipment", [])),
                                        Equipment.available > 0
                                    ).count()

                                    # Calculate total match score
                                    service_matches.append({
                                        'service': service,
                                        'score': matching_specialties + matching_equipment
                                    })

                                # Select service with highest match score
                                if service_matches:
                                    max_score = max(match['score'] for match in service_matches)
                                    best_matches = [
                                        match['service'] for match in service_matches
                                        if match['score'] == max_score
                                    ]

                                    # If there's a tie, keep the closest one
                                    selected_service = best_matches[0]

                            services.append(selected_service)
                            logging.info(f"Selected {service_type} service: {selected_service.name}")
                    else:
                        # If no location provided, just take the first active service
                        services.append(active_services[0])
                        logging.info(
                            f"No location provided. Selected first active {service_type} service: {active_services[0].name}")

                except Exception as e:
                    logging.error(f"Error processing {service_type} services: {str(e)}")
                    continue
            print("NOW")
            print(str([service.name for service in services]))
            new_incident = Incident(
                is_genuine_emergency=ai_assessment.get('genuine_emergency', False),
                severity_level=int(ai_assessment.get('severity_level', 1)),
                description=description,
                location=location,
                latitude=latitude,
                longitude=longitude,
                required_services=','.join(map(str, ai_assessment.get('required_services', []))),
                selected_services=','.join(map(str, services)),  # Ensure all items are strings
                required_specialties=','.join(map(str, ai_assessment.get('required_specialties', []))),
                required_equipment=','.join(map(str, ai_assessment.get('required_equipment', []))),
                user_response=str(ai_assessment.get('response', '')),
                situation_assessment=str(ai_assessment.get('assessment', ''))
            )
            try:
                db.session.add(new_incident)
                db.session.commit()
            except Exception as e:
                db.session.rollback()




            log_message = f"""
            Emergency Report:
            ID: {report.id}
            Name: {name}
            Contact: {contact}
            Location: {location}
            Description: {description}
            Audio Recording: {audio_filename if audio_filename else 'No audio recorded'}
            Timestamp: {datetime.utcnow()}
            """
            logging.info(log_message)

            response_data = {
                'status': 'success',
                'message': str(ai_assessment.get('response', ''))+"The help is coming. Activated services:"+str([service.name for service in services]),
                'location': location,
                'eta': 'f'
            }

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(response_data), 200
            else:
                flash(str(ai_assessment.get('response', ''))+str([service.name for service in services ]), 'success')
                return redirect(url_for('chat'))

        except ValueError as ve:
            logging.error(f"Validation error: {str(ve)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': str(ve)}), 400
            else:
                flash(str(ve), 'error')
                return redirect(url_for('chat'))
        except Exception as e:
            logging.error(f"Error processing emergency report: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': 'Failed to process emergency report'}), 500
            else:
                flash('Error processing emergency report. Please try again.', 'error')
                return redirect(url_for('chat'))

    return render_template('chat.html',
                         current_time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                         current_user="nicknet06")

@app.route('/admin/dashboard')
def admin_dashboard():
    try:
        reports = EmergencyReport.query.order_by(EmergencyReport.created_at.desc()).all()
        services = EmergencyService.query.filter_by(is_active=True).all()
        return render_template('admin_dashboard.html',
                             reports=reports,
                             services=services,
                             current_time="2025-02-17 01:07:12",
                             current_user="nicknet06")
    except Exception as e:
        flash(f'Error accessing database: {str(e)}', 'error')
        return redirect(url_for('home'))

@app.route('/api/services')
def get_services():
    try:
        with app.app_context():
            print("Attempting to fetch services...")
            services = EmergencyService.query.filter_by(is_active=True).all()
            print(f"Found {len(services)} active services")
            result = []
            for service in services:
                service_dict = {
                    'id': service.id,
                    'name': service.name,
                    'service_type': service.service_type,
                    'city': service.city,
                    'latitude': float(service.latitude),
                    'longitude': float(service.longitude),
                    'address': service.address,
                    'phone': service.phone,
                    'is_active': service.is_active,
                    'created_at': service.created_at.isoformat() if service.created_at else None
                }
                print(f"Converting service: {service_dict['name']}")
                result.append(service_dict)
            print(f"Converted {len(result)} services to JSON")
            return jsonify(result)
    except Exception as e:
        print(f"Error in get_services: {str(e)}")
        logging.error(f"Error fetching services: {str(e)}")
        return jsonify({'error': 'Failed to fetch services', 'details': str(e)}), 500


@app.route('/api/incidents/recent')
def get_recent_incidents():
    try:
        # Get current time in UTC
        now_utc = datetime.now(pytz.UTC)
        time_threshold = now_utc - timedelta(hours=3)

        print(f"Current UTC time: {now_utc}")
        print(f"Time Threshold UTC: {time_threshold}")

        # Get incidents for the last 3 hours
        incidents = Incident.query.filter(
            Incident.created_at >= time_threshold
        ).order_by(Incident.created_at.desc()).all()

        for incident in incidents:
            print(f"Incident {incident.id} created at: {incident.created_at}")

        return jsonify({
            'incidents': [incident.to_dict() for incident in incidents],
            'timestamp': now_utc.isoformat(),
            'timezone': 'UTC',
            'user': "nicknet06"
        })
    except Exception as e:
        print(f"Error in get_recent_incidents: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now(pytz.UTC).isoformat(),
            'timezone': 'UTC',
            'user': "nicknet06"
        }), 500

@app.route('/api/incidents/<int:incident_id>')
def get_incident_details(incident_id):
    try:
        incident = Incident.query.get_or_404(incident_id)
        return jsonify(incident.to_dict())
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            'user': "nicknet06"
        }), 500
@app.route('/api/services/<int:service_id>/incidents')
def get_service_incidents(service_id):
    try:
        # Get incidents where this service is in the selected_services
        incidents = Incident.query.filter(
            Incident.selected_services.like(f'%{service_id}%')
        ).order_by(Incident.created_at.desc()).all()

        return jsonify({
            'incidents': [incident.to_dict() for incident in incidents]
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/services/<int:service_id>/resources')
def get_service_resources(service_id):
    try:
        # Get basic resources
        equipment = Equipment.query.filter_by(service_id=service_id).all()
        vehicles = Vehicle.query.filter_by(service_id=service_id).all()
        personnel = Personnel.query.filter_by(service_id=service_id).all()

        # Calculate time threshold for last 3 hours
        time_threshold = datetime.utcnow() - timedelta(hours=3)

        # Get incidents for the last 3 hours
        incidents = Incident.query.filter(
            Incident.created_at >= time_threshold
        ).filter(
            Incident.selected_services.contains(f"<EmergencyService {service_id}>")
        ).order_by(Incident.created_at.desc()).all()

        return jsonify({
            'equipment': [e.to_dict() for e in equipment],
            'vehicles': [v.to_dict() for v in vehicles],
            'personnel': [p.to_dict() for p in personnel],
            'incidents': [incident.to_dict() for incident in incidents],
            'timestamp': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            'user': "nicknet06"
        })
    except Exception as e:
        print(f"Error in get_service_resources: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            'user': "nicknet06"
        }), 500

@app.route('/api/resources/request', methods=['POST'])
def request_resource():
    try:
        data = request.get_json()

        new_request = ResourceRequest(
            service_id=data['service_id'],
            equipment_id=data.get('equipment_id'),
            vehicle_id=data.get('vehicle_id'),
            personnel_id=data.get('personnel_id'),
            requester=data['requester'],
            purpose=data['purpose'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            status='pending'
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify({
            'message': 'Request submitted successfully',
            'request_id': new_request.id,
            'status': 'pending',
            'timestamp': "2025-02-17 00:16:55",
            'user': "nicknet06"
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': "2025-02-17 00:16:55",
            'user': "nicknet06"
        }), 500


@app.route('/api/debug/db')
def debug_db():
    try:
        with app.app_context():
            # Test basic database connectivity
            db_test = EmergencyService.query.first()
            total_count = EmergencyService.query.count()
            active_count = EmergencyService.query.filter_by(is_active=True).count()

            return jsonify({
                'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
                'connection_test': 'success' if db_test else 'no data but connected',
                'first_record': db_test.to_dict() if db_test else None,
                'total_records': total_count,
                'active_records': active_count,
                'timestamp': "2025-02-17 00:16:55",
            })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'database_uri': app.config['SQLALCHEMY_DATABASE_URI'],
            'timestamp': "2025-02-17 00:16:55",
        }), 500


@app.route('/api/statistics')
def get_statistics():
    try:
        with app.app_context():
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

            total_services = EmergencyService.query.count()
            print(f"Total services: {total_services}")

            active_services = EmergencyService.query.filter_by(is_active=True).count()
            print(f"Active services: {active_services}")

            hospitals = EmergencyService.query.filter_by(service_type='hospital', is_active=True).count()
            print(f"Hospitals: {hospitals}")

            police = EmergencyService.query.filter_by(service_type='police', is_active=True).count()
            print(f"Police stations: {police}")

            fire = EmergencyService.query.filter_by(service_type='fire', is_active=True).count()
            print(f"Fire stations: {fire}")

            total_reports = EmergencyReport.query.count()
            print(f"Total reports: {total_reports}")

            recent_reports = EmergencyReport.query.filter(
                EmergencyReport.created_at >= datetime.utcnow().date()
            ).count()
            print(f"Recent reports: {recent_reports}")

            stats = {
                'total_services': total_services,
                'active_services': active_services,
                'hospitals': hospitals,
                'police_stations': police,
                'fire_stations': fire,
                'total_reports': total_reports,
                'recent_reports': recent_reports,
                'database_uri': app.config['SQLALCHEMY_DATABASE_URI']
            }
            return jsonify(stats)
    except Exception as e:
        logging.error(f"Error fetching statistics: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch statistics',
            'details': str(e),
            'database_uri': app.config['SQLALCHEMY_DATABASE_URI']
        }), 500


@app.route('/admin/reports')
def admin_reports():
    try:
        reports = EmergencyReport.query.order_by(EmergencyReport.created_at.desc()).all()
        return render_template('admin_reports.html',
                               reports=reports,
                               current_time="2025-02-17 00:16:55",
                               current_user="nicknet06")
    except Exception as e:
        flash(f'Error accessing database: {str(e)}', 'error')
        return redirect(url_for('home'))





@app.route('/upload-audio', methods=['POST', 'OPTIONS'])
def upload_audio():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
    else:
        try:
            logging.info(f"Upload folder path: {app.config['UPLOAD_FOLDER']}")

            if 'audio' not in request.files:
                logging.error("No audio file in request")
                return jsonify({'error': 'No audio file'}), 400

            # Get the audio file and form data
            audio_file = request.files['audio']
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f'emergency_recording_{timestamp}.wav'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            logging.info(f"Attempting to save audio file to: {filepath}")

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            audio_file.save(filepath)

            if not os.path.exists(filepath):
                raise Exception(f"Failed to save file at {filepath}")

            logging.info(f"Audio file successfully saved: {filename}")

            # Create emergency report from form data
            name = request.form.get('name', 'Anonymous')
            contact = request.form.get('contact', 'Not provided')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            description = request.form.get('description', 'Audio emergency report')

            report = EmergencyReport(
                name=name,
                contact=contact,
                latitude=float(latitude) if latitude else None,
                longitude=float(longitude) if longitude else None,
                description=description,
                audio_filename=filename,
                created_at=datetime.utcnow()
            )

            # Save to db
            try:
                db.session.add(report)
                db.session.commit()
                logging.info(f"Emergency report created with ID: {report.id}")

                return jsonify({
                    'filename': filename,
                    'message': 'Audio uploaded and emergency report created successfully',
                    'report_id': report.id,
                    'timestamp': '2025-02-17 13:42:04',
                    'user': 'nicknet06'
                }), 200

            except Exception as db_error:
                db.session.rollback()
                logging.error(f"Database error: {str(db_error)}")
                raise

        except Exception as e:
            logging.error(f"Error in upload process: {str(e)}")
            return jsonify({
                'error': str(e),
                'timestamp': '2025-02-17 13:42:04',
                'user': 'nicknet06'
            }), 500

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response


@app.route('/api/resources/requests/<int:request_id>', methods=['PUT'])
def update_resource_request(request_id):
    try:
        data = request.get_json()
        resource_request = ResourceRequest.query.get(request_id)

        if not resource_request:
            return jsonify({
                'error': 'Request not found',
                'timestamp': "2025-02-17 00:22:26",
                'user': "nicknet06"
            }), 404

        resource_request.status = data['status']
        db.session.commit()

        return jsonify({
            'message': 'Request updated successfully',
            'status': resource_request.status,
            'timestamp': "2025-02-17 00:22:26",
            'user': "nicknet06"
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': "2025-02-17 00:22:26",
            'user': "nicknet06"
        }), 500


@app.route('/api/resources/requests', methods=['GET'])
def list_resource_requests():
    try:
        requests = ResourceRequest.query.all()
        return jsonify({
            'requests': [request.to_dict() for request in requests],
            'timestamp': "2025-02-17 00:22:26",
            'user': "nicknet06"
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': "2025-02-17 00:22:26",
            'user': "nicknet06"
        }), 500


@app.route('/api/services/<int:service_id>/availability', methods=['GET'])
def get_service_availability(service_id):
    try:
        equipment_available = Equipment.query.filter_by(
            service_id=service_id
        ).with_entities(
            db.func.sum(Equipment.available).label('available'),
            db.func.sum(Equipment.quantity).label('total')
        ).first()

        vehicles_available = Vehicle.query.filter_by(
            service_id=service_id,
            status='available'
        ).count()
        total_vehicles = Vehicle.query.filter_by(service_id=service_id).count()

        personnel_available = Personnel.query.filter_by(
            service_id=service_id,
            status='on-duty'
        ).count()
        total_personnel = Personnel.query.filter_by(service_id=service_id).count()

        return jsonify({
            'equipment': {
                'available': equipment_available.available or 0,
                'total': equipment_available.total or 0
            },
            'vehicles': {
                'available': vehicles_available,
                'total': total_vehicles
            },
            'personnel': {
                'available': personnel_available,
                'total': total_personnel
            },
            'timestamp': "2025-02-17 00:22:26",
            'user': "nicknet06"
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': "2025-02-17 00:22:26",
            'user': "nicknet06"
        }), 500


@app.route('/api/resources/maintenance', methods=['POST'])
def schedule_maintenance():
    try:
        data = request.get_json()
        equipment = Equipment.query.get(data['equipment_id'])

        if not equipment:
            return jsonify({
                'error': 'Equipment not found',
                'timestamp': "2025-02-17 00:22:26",
                'user': "nicknet06"
            }), 404

        equipment.condition = 'maintenance'
        equipment.available = max(0, equipment.available - 1)
        equipment.last_maintenance = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'message': 'Maintenance scheduled successfully',
            'equipment_id': equipment.id,
            'new_condition': equipment.condition,
            'available': equipment.available,
            'timestamp': "2025-02-17 00:22:26",
            'user': "nicknet06"
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': "2025-02-17 00:22:26",
            'user': "nicknet06"
        }), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html',
                           current_time="2025-02-17 00:22:26",
                           current_user="nicknet06"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html',
                           current_time="2025-02-17 00:22:26",
                           current_user="nicknet06"), 500


def init_app():
    """Initialize the Flask application."""
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("Database tables created successfully")


if __name__ == '__main__':
    print("\nApplication Startup Information:")
    print("--------------------------------")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Base directory: {BASE_DIR}")
    print(f"Template folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Current time (UTC): 2025-02-17 00:22:26")
    print(f"Current user: nicknet06")

    if os.path.exists(app.template_folder):
        print(f"Available templates: {os.listdir(app.template_folder)}")
    else:
        print(f"Warning: Template folder not found at {app.template_folder}")

    print("\nStarting database connection...")
    wait_for_db()
    init_app()

    print("\nStarting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
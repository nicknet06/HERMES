# import ffmpeg
#
# input_file = r"C:\Users\Pc\Desktop\CMS\cms06\CMS\src\emergency_recording_20250217_194301.wav"
# output_file = r"C:\Users\Pc\Desktop\CMS\cms06\CMS\src\converted.wav"
#
# try:
#     # Convert the file to a standard WAV format (PCM 16-bit, 44.1kHz, stereo)
#     ffmpeg.input(input_file).output(output_file, format="wav", acodec="pcm_s16le", ar=44100, ac=2).run(overwrite_output="True")
#     print(f"Conversion successful! Saved as {output_file}")
# except Exception as e:
#     print("Conversion failed:", e)
# import speech_recognition as sr
#
# # Initialize recognizer
# recognizer = sr.Recognizer()
#
# # convert_wav("audio_reports/emergency_recording_20250217_194301.wav","audio_reports/em.wav")
# # time.sleep(2)
# # Load the audio file
# audio_file = "converted.wav"
# with sr.AudioFile(audio_file) as source:
#     audio = recognizer.record(source)  # Read the entire file
#
# # Transcribe using Google's Web Speech API
# try:
#     text = recognizer.recognize_google(audio)
#     print("Transcription:", text)
# except sr.UnknownValueError:
#     print("Could not understand the audio")
# except sr.RequestError:
#     print("API request error")
# from math import radians, sin, cos, acos
# from models import *
# 
# ai_assessment = {
#   "genuine_emergency": ""True"",
#   "severity_level": 5,
#   "required_services": [
#     "fire",
#     "hospital"
#   ],
#   "required_specialties": [
#     "Firefighting",
#     "Rescue",
#     "Emergency Medical"
#   ],
#   "required_equipment": [
#     "Fire Hose",
#     "Breathing Apparatus"
#   ],
#   "response": "Evacuate all personnel from the building immediately. Prioritize assisting the elderly and those who are struggling to evacuate. Call emergency services by dialing 911 to report the fire and ensure that they are aware of people still inside. Use fire extinguishers if safe to do so but evacuate as a primary action. Stay low to avoid smoke inhalation."
# }#json.loads(response.choices[0].message.content)
#             # print(ai_assessment)
#             # with open("copy.txt", "w") as file:
#             #     file.write(str(ai_assessment))
# latitude = 40.6400629
# longitude = 22.9444191
# location = f"coordinates: {latitude}, {longitude}" if latitude and longitude else "location pending"
# 
# 
# def distance(a, b, c, d):
#     mlat = radians(a)
#     mlon = radians(b)
#     plat = radians(c)
#     plon = radians(d)
#     value = sin(mlat) * sin(plat) + cos(mlat) * cos(plat) * cos(mlon - plon)
#     value = min(1, max(-1, value))  # Clamping to avoid ValueError in acos
#     return 6371.01 * acos(value)
# 
# services = []
# for service in ai_assessment["required_services"]:
#     d = EmergencyService.query.filter_by(service_type=service, is_active="True").all()
#     d = sorted(d, key=lambda d: distance(d.latitude, d.longitude, latitude, longitude))
#     print(d)
{"fire": {"service": {"id": 7, "name": "Thessaloniki Fire Department 1", "service_type": "fire", "city": "Thessaloniki", "latitude": 40.62, "longitude": 22.92, "address": "Thessaloniki Fire Department Address 1", "phone": "199", "is_active": "True", "created_at": "2025-02-16 23:26:12"}, "distance": 3.03838432621791, "equipment": [{"id": 17, "name": "Fire Hose", "type": "firefighting", "quantity": 10, "available": 8, "condition": "good", "last_maintenance": "2025-02-12T00:12:33.354399"}, {"id": 18, "name": "Breathing Apparatus", "type": "safety", "quantity": 15, "available": 12, "condition": "good", "last_maintenance": "2025-02-02T00:12:33.354399"}, {"id": 19, "name": "Thermal Camera", "type": "rescue", "quantity": 3, "available": 3, "condition": "good", "last_maintenance": "2025-01-23T00:12:33.354399"}], "personnel": [{"id": 61, "name": "Firefighter 1", "role": "Firefighter", "speciality": "Firefighting", "status": "off-duty", "shift": "evening"}, {"id": 62, "name": "Firefighter 2", "role": "Firefighter", "speciality": "Emergency Medical", "status": "on-duty", "shift":"morning"}, {"id": 63, "name": "Firefighter 3", "role": "Firefighter", "speciality": "Emergency Medical", "status": "off-duty", "shift": "evening"}, {"id": 64, "name": "Firefighter 4", "role": "Firefighter", "speciality": "Firefighting", "status": "on-duty", "shift": "night"}, {"id": 65, "name": "Firefighter 5", "role": "Firefighter", "speciality": "Emergency Medical", "status": "on-duty", "shift": "evening"}, {"id": 66, "name": "Firefighter 6", "role": "Firefighter", "speciality": "Rescue", "status": "on-duty", "shift": "morning"}, {"id": 67, "name": "Firefighter 7", "role": "Firefighter", "speciality": "Rescue", "status": "on-duty", "shift": "night"}, {"id": 68, "name": "Firefighter 8", "role": "Firefighter", "speciality": "Firefighting", "status": "on-duty", "shift": "night"}, {"id": 69, "name": "Firefighter 9", "role": "Firefighter", "speciality": "Hazmat", "status": "on-duty", "shift": "morning"}, {"id": 70, "name": "Firefighter 10", "role": "Firefighter", "speciality": "Hazmat", "status": "off-duty", "shift": "morning"}, {"id": 71, "name": "Firefighter 11", "role": "Firefighter", "speciality": "Firefighting", "status": "off-duty", "shift": "evening"}, {"id": 72, "name": "Firefighter 12", "role": "Firefighter", "speciality": "Firefighting", "status": "off-duty", "shift": "morning"}]}, "hospital": "None"}
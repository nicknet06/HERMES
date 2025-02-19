from app import app, db
from models import EmergencyService

def check_and_fix_services():
    with app.app_context():
        # Get all services
        all_services = EmergencyService.query.all()
        
        print("\nCurrent Services Status:")
        print("------------------------")
        if not all_services:
            print("No services found in database!")
            return
            
        inactive_count = 0
        for service in all_services:
            status = "ACTIVE" if service.is_active else "INACTIVE"
            print(f"ID: {service.id} | Name: {service.name} | Type: {service.service_type} | Status: {status}")
            if not service.is_active:
                inactive_count += 1
                
        print(f"\nFound {len(all_services)} total services, {inactive_count} are inactive")
        
        if inactive_count > 0:
            choice = input("\nWould you like to activate all services? (yes/no): ")
            if choice.lower() == 'yes':
                for service in all_services:
                    service.is_active = True
                db.session.commit()
                print("All services have been activated!")
            else:
                print("No changes made to services.")

if __name__ == '__main__':
    check_and_fix_services()
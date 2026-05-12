from app.extensions import db
from app.models.messages import Reminder, Notes
from app.utils.decorators import role_required
from datetime import datetime
from flask_login import login_required, current_user
from flask import request, jsonify
from . import admin_bp

@admin_bp.route("/reminders", methods=["POST", "PUT"])
@login_required
@role_required("Admin")
def manage_reminder():
    try:
        data = request.get_json()
        
        title = data.get("title", "").strip()
        message = data.get("description", "").strip()  
        priority = data.get("priority", "medium")      
        icon = data.get("icon", "fa-user")            
        color = data.get("color", "blue")               
        due_date_str = data.get("due_date")
        
       
        if not title:
            return jsonify({"error": "Reminder title is required"}), 400
        
        
        remind_at = datetime.utcnow() 
        if due_date_str:
            try:
              
                remind_at = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                remind_at = datetime.utcnow()
        
        reminder_id = data.get("id")
        
        if reminder_id:
            # UPDATE existing reminder
            reminder = Reminder.query.get_or_404(reminder_id)
            reminder.title = title
            reminder.message = message
            reminder.remind_at = remind_at
            reminder.priority = priority      
            reminder.icon = icon              
            reminder.color = color            
        else:
            # CREATE new reminder
            reminder = Reminder(
                title=title,
                message=message,
                remind_at=remind_at,
                priority=priority,
                icon=icon,
                color=color,
                user_id=current_user.id,
                is_done=False
            )
            db.session.add(reminder)
        
        db.session.commit()
        return jsonify({"success": True, "id": reminder.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@admin_bp.route("/notes", methods=["POST", "PUT"])
@login_required
@role_required("Admin")
def manage_note():
    try:
        data = request.get_json()
        
        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        color = data.get("color", "indigo")  
        note_id = data.get("id")
        
        # Validation
        if not title or not content:
            return jsonify({"error": "Title and content are required"}), 400
        
        if note_id:
            # UPDATE
            note = Notes.query.get_or_404(note_id)
            note.title = title
            note.content = content
            note.color = color  
        else:
            # CREATE
            note = Notes(
                title=title,
                content=content,
                color=color, 
                user_id=current_user.id
            )
            db.session.add(note)
        
        db.session.commit()
        return jsonify({"success": True, "id": note.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@login_required
@role_required("Admin")
def delete_note(note_id):
    try:
        note = Notes.query.get_or_404(note_id) 
        db.session.delete(note)
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
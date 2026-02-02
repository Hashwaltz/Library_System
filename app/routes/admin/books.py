from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.utils.decorators import role_required
from app.extensions import db
from app.models.book import Book, Section, SubjectType, Edition
from app.utils.helpers import log_audit

from . import admin_bp

# -----------------------------
# LIST ALL BOOKS
# -----------------------------
@admin_bp.route('/books')
@role_required("Admin")
def list_books():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # number of books per page

    pagination = Book.query.filter_by(is_archived=False).order_by(Book.title.asc()).paginate(page=page, per_page=per_page)
    books = pagination.items
    sections = Section.query.all()
    subject_types = SubjectType.query.all()
    editions = Edition.query.all()
    return render_template('admin/books.html', 
                           books=books,
                           sections=sections,
                           subject_types=subject_types,
                           editions=editions,
                           pagination=pagination)

# -----------------------------
# ADD NEW BOOK
# -----------------------------
@admin_bp.route('/books/add', methods=['POST'])
@role_required("Admin")
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        assecion_number = request.form['assecion_number']
        call_number = request.form['call_number']
        publisher = request.form.get('publisher')
        year_published = request.form.get('year_published')
        classification_id = request.form.get('classification_id')
        section_id = request.form.get('section_id') or None
        subject_type_id = request.form.get('subject_type_id') or None
        edition_id = request.form.get('edition_id') or None

        new_book = Book(
            title=title,
            author=author,
            assecion_number=assecion_number,
            call_number=call_number,
            publisher=publisher,
            year_published=year_published,
            classification_id=classification_id,
            section_id=section_id,
            subject_type_id=subject_type_id,
            edition_id=edition_id,
        )

        db.session.add(new_book)
        db.session.commit()

        # --- Audit log ---
        log_audit(
            action="ADD BOOK",
            table_name="book",
            record_id=new_book.id,
            new_data={
                "title": title,
                "author": author,
                "assecion_number": assecion_number,
                "call_number": call_number,
                "publisher": publisher,
                "year_published": year_published,
                "classification_id": classification_id,
                "section_id": section_id,
                "subject_type_id": subject_type_id,
                "edition_id": edition_id
            }
        )

        flash('Book added successfully!', 'success')
        return redirect(url_for('admin.list_books'))

    return redirect(url_for('admin.list_books'))

# -----------------------------
# EDIT BOOK
# -----------------------------
@admin_bp.route('/books/edit/<int:book_id>', methods=['POST'])
@role_required("Admin")
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    # Save old data
    old_data = {
        "title": book.title,
        "author": book.author,
        "assecion_number": book.assecion_number,
        "call_number": book.call_number,
        "publisher": book.publisher,
        "year_published": book.year_published,
        "classification_id": book.classification_id,
        "section_id": book.section_id,
        "subject_type_id": book.subject_type_id,
        "edition_id": book.edition_id
    }

    book.title = request.form['title']
    book.author = request.form['author']
    book.assecion_number = request.form['assecion_number']
    book.call_number = request.form['call_number']
    book.publisher = request.form.get('publisher')
    book.year_published = request.form.get('year_published')
    book.classification_id = request.form.get('classification_id')
    book.section_id = request.form.get('section_id') or None
    book.subject_type_id = request.form.get('subject_type_id') or None
    book.edition_id = request.form.get('edition_id') or None

    db.session.commit()

    # --- Audit log ---
    log_audit(
        action="EDIT BOOK",
        table_name="book",
        record_id=book.id,
        old_data=old_data,
        new_data={
            "title": book.title,
            "author": book.author,
            "assecion_number": book.assecion_number,
            "call_number": book.call_number,
            "publisher": book.publisher,
            "year_published": book.year_published,
            "classification_id": book.classification_id,
            "section_id": book.section_id,
            "subject_type_id": book.subject_type_id,
            "edition_id": book.edition_id
        }
    )

    flash('Book updated successfully!', 'success')
    return redirect(url_for('admin.list_books'))

# -----------------------------
# DELETE BOOK
# -----------------------------
@admin_bp.route('/books/delete/<int:book_id>', methods=['POST'])
@role_required("Admin")
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    # Save old data
    old_data = {
        "title": book.title,
        "author": book.author,
        "assecion_number": book.assecion_number,
        "call_number": book.call_number
    }

    book.is_archived = True
    db.session.commit()

    # --- Audit log ---
    log_audit(
        action="DELETE BOOK",
        table_name="book",
        record_id=book.id,
        old_data=old_data
    )

    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin.list_books'))

# -----------------------------
# ARCHIVED BOOKS PAGE
# -----------------------------
@admin_bp.route('/books/archived')
@role_required("Admin")
def archived_books():
    page = request.args.get('page', 1, type=int)
    books_query = Book.query.filter_by(is_archived=True).order_by(Book.id.desc())
    pagination = books_query.paginate(page=page, per_page=10)
    books = pagination.items
    return render_template(
        'admin/archived_books.html',
        books=books,
        pagination=pagination
    )

# -----------------------------
# RESTORE BOOK
# -----------------------------
@admin_bp.route('/books/restore/<int:book_id>', methods=['POST'])
@role_required("Admin")
def restore_book(book_id):
    book = Book.query.get_or_404(book_id)

    # Save old data
    old_data = {"is_archived": True}

    book.is_archived = False
    db.session.commit()

    # --- Audit log ---
    log_audit(
        action="RESTORE BOOK",
        table_name="book",
        record_id=book.id,
        old_data=old_data,
        new_data={"is_archived": False}
    )

    flash('Book restored successfully!', 'success')
    return redirect(url_for('admin.archived_books'))

from . import routes
from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
from dotenv import load_dotenv
import flask
import flask_login
from src.models.user import user_loader, request_loader
from src.models.user import User
from src.models.boards import get_boards_by_user, delete_board, duplicate_board, create_board, get_board, update_board


@flask_login.login_required
@routes.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method == 'POST':    
        if 'new' in request.form:
            create_board(flask_login.current_user.email, "New Board")
            flash('New board created successfully', 'success')
        elif 'delete' in request.form:
            delete_board(request.form['delete'])
            flash('Board deleted successfully', 'success')
        elif 'duplicate' in request.form:
            duplicate_board(request.form['duplicate'])
            flash('Board duplicated successfully', 'success')
        elif 'edit' in request.form:
            return redirect(url_for('routes.edit_board', board_id=request.form['edit']))
        return redirect(url_for('routes.profile'))

    try:
        boards = list(get_boards_by_user(flask_login.current_user.email))
    except Exception as e:
        flash(f'Error fetching boards: {str(e)}', 'error')
        return redirect(url_for('routes.login'))

    return render_template('profile.html', username=flask_login.current_user.username, boards=boards)

@routes.route('/account_settings')
@flask_login.login_required
def account_settings():
    return render_template('account-setting.html')
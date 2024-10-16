from . import routes
from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
from dotenv import load_dotenv
import flask
import flask_login
from src.models.user import user_loader, request_loader
from src.models.user import User
from src.models.boards import *
from src.app import get_db
from bson.objectid import ObjectId


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
        privacy = flask_login.current_user.privacy
    except Exception as e:
        flash(f'Error fetching boards: {str(e)}', 'error')
        return redirect(url_for('routes.login'))

    return render_template('profile.html', username=flask_login.current_user.username, boards=boards, privacy=privacy)


@routes.route('/account_settings', methods=['GET', 'POST'])
@flask_login.login_required
def account_settings():
    return render_template('account-setting.html')


@routes.route('/update_account', methods=['POST'])
@flask_login.login_required
def update_account():
    print("Update Account route triggered")
    username = request.form.get('username')
    email = request.form.get('email')
    privacy = request.form.get('privacy')
    password = request.form.get('password')
    needLogin = False

    current_user_id = flask_login.current_user.get_id()
    user = get_db().users.find_one({'email': current_user_id})

    update_fields = {}
    if email:
        if email != current_user_id:
            existing_user = get_db().users.find_one({'email': email})
            if existing_user:
                flash(
                    "Email already in use. Please select a different email", "error")
                return redirect(url_for('routes.account_settings'))

            else:
                change_board_email(current_user_id, email)
                needLogin = True
    if username:
        update_fields['username'] = username
    if privacy:
        update_fields['privacy'] = privacy
    if password:
        update_fields['password'] = password
        if password != user.get('password'):
            needLogin = True

    if update_fields:
        get_db().users.update_one(
            {'email': current_user_id},
            {'$set': update_fields}
        )
    if needLogin:
        return redirect(url_for('routes.login'))

    return redirect(url_for('routes.account_settings'))


@routes.route('/edit_board/<board_id>', methods=["GET", "POST"])
@flask_login.login_required
def edit_board(board_id):
    try:
        board = get_board(ObjectId(board_id))
    except Exception:
        flash('Invalid Board ID.', 'error')
        return redirect(url_for('routes.profile'))

    if not board:
        flash('Board not found', 'error')
        return redirect(url_for('routes.profile'))

    board['_id'] = str(board['_id'])

    if request.method == 'POST':
        name = request.form.get('name')
        pedal_data = request.form.getlist('pedals')

        pedals = board.get('pedals', [None] * 10)

        for index, data in enumerate(pedal_data):
            isDeleted = request.form.get(f'pedal_deleted_{index}') == '1'
            if isDeleted:
                pedals[index] = None
            elif data:
                try:
                    pedal_name, pedal_image = data.split('|')
                    pedals[index] = {'name': pedal_name,
                                     'image_url': pedal_image}
                except ValueError:
                    continue

        update_board(board_id, name, pedals)

        flash('Board updated successfully', 'success')
        return redirect(url_for('routes.profile'))

    pedal_name = request.args.get("pedal_name", "")
    pedal_image = request.args.get("pedal_image", "")
    slot_index = request.args.get("slot_index")

    if slot_index is not None:
        try:
            slot_index = int(slot_index)
        except ValueError:
            flash('Invalid slot index.', 'error')
            return redirect(url_for('routes.profile'))

        if 'pedals' not in board or not board['pedals']:
            board['pedals'] = [None] * 10  # Assume 10 slots

        if pedal_name == "" and pedal_image == "":
            board['pedals'][slot_index] = None
        else:
            if slot_index < len(board['pedals']):
                board['pedals'][slot_index] = {
                    'name': pedal_name, 'image_url': pedal_image}

        update_board(board_id, board['name'], board['pedals'])

    return render_template('edit_board.html', board=board)


@routes.route('/view_board/<board_id>', methods=["GET"])
def view_board(board_id):
    try:
        board = get_board(ObjectId(board_id))
    except Exception:
        flash('Invalid Board ID.', 'error')
        return redirect(url_for('routes.profile'))

    if not board:
        flash('Board not found', 'error')
        return redirect(url_for('routes.profile'))

    return render_template('view_board.html', board=board)

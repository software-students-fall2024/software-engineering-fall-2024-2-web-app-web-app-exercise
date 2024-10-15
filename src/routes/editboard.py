from . import routes
from flask import render_template, request, redirect, url_for, flash
import flask_login
from src.app import get_db
from src.models.boards import get_board, update_board
from bson.objectid import ObjectId

@routes.route('/edit_board/<board_id>', methods=["GET", "POST"])
@flask_login.login_required
def edit_board(board_id):
    pedal_name = request.args.get("pedal_name")
    pedal_image = request.args.get("pedal_image")
    
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

        
        pedals = []
        for data in pedal_data:
            try:
                pedal_name, pedal_image = data.split('|')
                pedals.append({'name': pedal_name, 'image_url': pedal_image})
            except ValueError:
                continue  

        
        update_board(board_id, name, pedals)

        
        flash('Board updated successfully', 'success')
        return redirect(url_for('routes.profile'))


    if pedal_name and pedal_image:
       
        if 'pedals' not in board:
            board['pedals'] = []

        
        existing_pedal = next((p for p in board['pedals'] if p['name'] == pedal_name and p['image_url'] == pedal_image), None)
        if not existing_pedal:
            board['pedals'].append({'name': pedal_name, 'image_url': pedal_image})
            
            update_board(board_id, board['name'], board['pedals'])

   
    return render_template('edit_board.html', board=board)
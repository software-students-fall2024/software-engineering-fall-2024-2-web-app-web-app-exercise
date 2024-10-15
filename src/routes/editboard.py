from . import routes
from flask import render_template, request, redirect, url_for, flash
import flask_login
from src.app import get_db
from src.models.boards import get_board, update_board

from . import routes
from flask import render_template, request, redirect, url_for, flash
import flask_login
from src.app import get_db
from src.models.boards import get_board, update_board

@routes.route('/edit_board/<board_id>', methods=["GET", "POST"])
@flask_login.login_required
def edit_board(board_id):
    
    board = get_board(board_id)
    
    
    if not board:
        flash('Board not found', 'error')
        return redirect(url_for('routes.profile'))
    
    
    if request.method == 'POST':
       
        name = request.form.get('name')
        pedals = request.form.getlist('pedals')

        
        update_board(board_id, name, pedals)

        
        flash('Board updated successfully', 'success')
        return redirect(url_for('routes.profile'))

    
    pedal_name = request.args.get("pedal_name")
    pedal_image = request.args.get("pedal_image")

    
    if pedal_name and pedal_image:
        
        if 'pedals' not in board:
            board['pedals'] = []
        board['pedals'].append({'name': pedal_name, 'image_url': pedal_image})
    
    
    return render_template('edit_board.html', board=board)
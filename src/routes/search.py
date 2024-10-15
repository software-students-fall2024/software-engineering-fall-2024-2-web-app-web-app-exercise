from . import routes
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from dotenv import load_dotenv
import flask
import flask_login
from src.models.user import user_loader, request_loader
from src.models.user import User

@routes.route('/search', methods=["GET"])
@flask_login.login_required
def search():

    query = request.args.get('query', '')
    board_id = request.args.get('board_id', '')


  
    all_pedals = [
        {'name': 'Boss TU-3 Chromatic Tuner', 'description': 'Industry-standard tuner for precise tuning.', 'image_url': '..src/data/images/boss_tu_3_chromatic_tuner.webp'},
        {'name': 'Boss CE-2 Chorus', 'description': 'Classic analog chorus for warm, swirling sounds.', 'image_url': '../data/images/boss_ce_2_chorus.webp'},
        {'name': 'Boss DD-8 Digital Delay', 'description': 'Versatile digital delay with multiple modes.', 'image_url': '../data/images/boss_dd_8_digital_delay.webp'},
        {'name': 'Boss DD-3T Digital Delay', 'description': 'Compact digital delay for studio-quality effects.', 'image_url': '../data/images/boss_dd_3t_digital_delay.webp'},
        {'name': 'Boss DM-2 Delay', 'description': 'Vintage analog delay for rich, warm echoes.', 'image_url': '../data/images/boss_dm_2_delay.webp'},
        {'name': 'Boss DS-1 Distortion', 'description': 'Iconic distortion pedal with a unique tonal edge.', 'image_url': '../data/images/boss_ds_1_distortion.webp'},
        {'name': 'Boss DS-2 Distortion', 'description': 'Turbo-charged version of the classic DS-1.', 'image_url': '../data/images/boss_ds_2_distortion.webp'},
        {'name': 'Boss FZ-1W Fuzz', 'description': 'Authentic vintage fuzz tones with modern features.', 'image_url': '../data/images/boss_fz_1w_fuzz.webp'},
        {'name': 'Boss GE-7 Equalizer', 'description': '7-band EQ to shape your sound with precision.', 'image_url': '../data/images/boss_ge_7_equalizer.webp'},
        {'name': 'Boss OC-3 Super Octave', 'description': 'Generates octave sounds for deep bass tones.', 'image_url': '../data/images/boss_oc_3_super_octave.webp'},
        {'name': 'Boss OD-320 Overdrive', 'description': 'Smooth and creamy overdrive for classic rock tones.', 'image_url': '../data/images/boss_od_320_overdrive.webp'},
        {'name': 'Boss RE-2 Space Echo', 'description': 'Spacey delay and reverb effects for ambient sounds.', 'image_url': '../data/images/boss_re_2_space_echo.webp'},
        {'name': 'Boss RV-6 Reverb', 'description': 'Professional-grade reverb effects in a compact box.', 'image_url': '../data/images/boss_rv_6_reverb.webp'},
        {'name': 'Boss SDE-3 Dual Digital Delay', 'description': 'Dual delay for rich, layered soundscapes.', 'image_url': '../data/images/boss_sde_3_dual_digital_delay.webp'},
        {'name': 'Boss SL-2 Slicer', 'description': 'Unique modulation effects with rhythmic slicing.', 'image_url': '../data/images/boss_sl_2_slicer.webp'}
    ]

   
    pedals = [pedal for pedal in all_pedals if query.lower() in pedal['name'].lower()]

   
    return render_template('search.html', pedals=pedals, board_id=board_id)
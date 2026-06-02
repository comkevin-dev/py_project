import os
import requests as http
from flask import render_template, request, redirect, url_for, flash, jsonify
from config import PROJECTS, SKILLS, PROFILE
from database import get_db


def register_routes(app):

    @app.route('/')
    def home():
        return render_template('index.html', projects=PROJECTS, skills=SKILLS, profile=PROFILE)

    @app.route('/api/weather')
    def weather():
        city = request.args.get('city', 'Seoul')
        try:
            res = http.get(f'https://wttr.in/{city}?format=j1', timeout=5)
            data = res.json()
            current = data['current_condition'][0]
            return jsonify({
                'city': city,
                'temp_c': current['temp_C'],
                'desc': current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'feels_like': current['FeelsLikeC'],
            })
        except Exception:
            return jsonify({'error': '날씨 정보를 가져올 수 없습니다.'}), 503

    @app.route('/contact', methods=['POST'])
    def contact():
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, message]):
            flash('모든 항목을 입력해 주세요.', 'error')
        else:
            with get_db() as conn:
                conn.execute(
                    'INSERT INTO messages (name, email, message) VALUES (?, ?, ?)',
                    (name, email, message)
                )
            flash(f'{name}님, 메시지가 전송되었습니다. 감사합니다!', 'success')

        return redirect(url_for('home') + '#contact')

    @app.route('/admin/messages')
    def admin_messages():
        pw       = request.args.get('pw', '')
        admin_pw = os.environ.get('ADMIN_PASSWORD', 'admin1234')
        if pw != admin_pw:
            return '접근 권한이 없습니다. (?pw=비밀번호)', 403
        with get_db() as conn:
            msgs = conn.execute(
                'SELECT * FROM messages ORDER BY created_at DESC'
            ).fetchall()
        return render_template('admin.html', messages=msgs)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

from jardiquest.controller import app
from flask_login import login_required, current_user
from flask import redirect, url_for, flash

@app.get('/blog')
@login_required
def blog():
    """Print the blog page"""
    garden = current_user.jardin
    if garden is None:
        flash("Vous devez d'abord créer ou rejoindre un jardin pour accéder à cette page", 'error')
        return redirect(url_for('controller.garden'))
    from jardiquest.model.path.blog_model import render_blog
    return render_blog()


@app.post('/blog')
def add_blog():
    """Post a new message on the blog page"""    
    from jardiquest.model.path.blog_model import add_new_message
    return add_new_message()



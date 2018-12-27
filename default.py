# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
import json



@request.restful()
def api():
    response.view = 'generic.json'

    def GET(tablename, id):
        if not tablename == 'person':
            raise HTTP(400)
        return dict(person = db.person(id))

    def POST(table_name, **vars):
        if table_name == 'image':
            return dict(db.person.validate_and_insert(**vars))
        else:
            raise HTTP(400)
    return locals()

@request.restful()
def api2():
    response.view = 'generic.json'

    def GET(tablename, id):
        if not tablename == 'images':
            raise HTTP(400)
        return dict(image = db.images(id))

    def POST(table_name, **vars):
        if table_name == 'android_image':
            return dict(db.android_image.validate_and_insert(**vars))
        else:
            raise HTTP(400)
    return locals()

# get image from database
def index1():
    images = db().select(db.image.ALL, orderby=db.image.title)  
    return dict(images=images)


# To show the image and comment
def show():
    image= db.image(request.args(0, cast=int)) or redirect(URL('index1'))
    db.post.image_id.default= image.id
    form= SQLFORM(db.post)
    if form.process().accepted:
        response.flash= 'Your comment is posted'
    comments= db(db.post.image_id == image.id).select(orderby= db.post.id)
    return dict(image=image, comments= comments, form=form)

def download():
    return response.download(request, db)




def index2():
    image = db().select(db.android_image.ALL)
    return dict(image=image)

def show2():
    image= db.android_image(request.args(0, cast=int)) or redirect(URL('index2'))
    return dict(image=image)

def download():
    return response.download(request, db)

def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def Nasrin():
    return "Nasrin"




# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

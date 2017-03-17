# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


@auth.requires_signature()
def del_listing():
    db(db.listing.id == request.vars.listing_id).delete()
    session.flash = (T('Your listing has been deleted'))
    return "ok"


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    listings = []
    num_listings = 0
    for listing in db().select(db.listing.ALL, orderby=~db.listing.created_on):
        listings.append(listing)
        num_listings += 1
    if num_listings == 0:
        return dict(listings='none')
    else:
        return dict(listings=listings, get_name=get_name)



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


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def add():
    if request.vars.listing_type:
        db.listing.insert(
            name=request.vars.name,
            email=request.vars.email,
            phone=request.vars.phone,
            title=request.vars.title,
            listing_type=request.vars.listing_type,
            start_date=request.vars.start_date,
            end_date=request.vars.end_date,
            start_time=request.vars.start_time,
            end_time=request.vars.end_time,
            monday=request.vars.monday,
            tuesday=request.vars.tuesday,
            wednesday=request.vars.wednesday,
            thursday=request.vars.thursday,
            friday=request.vars.friday,
            saturday=request.vars.saturday,
            sunday=request.vars.sunday,
            location_from=request.vars.location_from,
            location_to=request.vars.location_to,
            mileage_difference=request.vars.mileage_difference,
            housing_type=request.vars.housing_type,
            housing_desired=request.vars.housing_desired,
            housing_available=request.vars.housing_available,
            money=request.vars.money,
            v_type=request.vars.v_type,
            ve_type=request.vars.ve_type,
            vbors=request.vars.vbors,
            v_model=request.vars.model,
            v_year=request.vars.year,
            v_price=request.vars.v_price,
            description=request.vars.description,
            picture=request.vars.picture
        )
        session.flash = (T('Your listing has been added'))
        redirect(URL('index'))
    return dict(get_name=get_name, get_email=get_email, get_phone=get_phone)


def get_name():
    if auth.is_logged_in():
        name = ' '.join([auth.user.first_name, auth.user.last_name])
        return name
    else:
        return 'None'


def get_email():
    if auth.is_logged_in():
        return auth.user.email
    else:
        return 'None'


def get_phone():
    if auth.is_logged_in():
        return auth.user.phone
    else:
        return 'None'


def get_listings():

    logged_in = auth.user_id is not None
    t = request.vars.q.strip()
    if request.vars.q:
        q = ((db.listing.title.contains(t)) |
              db.listing.description.contains(t))
    else:
        q = db.listing.id > 0
    listings = db(q).select(db.listing.ALL, orderby=~db.listing.created_on)

    for l in listings:
        l.picture_url = URL('default/download', l.picture)

    return response.json(dict(
        listings=listings,
        logged_in=logged_in
    ))

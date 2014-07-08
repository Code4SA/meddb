from backend import logger, app, db
import models
from flask import Flask, flash, redirect, url_for, request, render_template, g
from flask.ext.admin import Admin, expose, AdminIndexView, helpers
from flask.ext.admin.model.template import macro
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.sqla.filters import FilterEqual
from wtforms import form, fields, validators, BooleanField
from datetime import datetime

HOST = app.config['HOST']

@app.context_processor
def inject_paths():
    return dict(HOST=HOST)

@app.template_filter('add_commas')
def jinja2_filter_add_commas(quantity):
    out = ""
    quantity_str = str(quantity)
    while len(quantity_str) > 3:
        tmp = quantity_str[-3::]
        out = "," + tmp + out
        quantity_str = quantity_str[0:-3]
    return quantity_str + out


country_choices = [
    ("BWA", "Botswana"),
    ("MWI", "Malawi"),
    ("SYC", "Seychelles"),
    ("ZAF", "South Africa"),
    ("TZA", "Tanzania"),
    ("ZMB", "Zambia"),
    ]


class MyModelView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    page_size = app.config['RESULTS_PER_PAGE']
    list_template = "admin/custom_list_template.html"
    column_exclude_list = []

    def is_accessible(self):
        if g.user is not None:
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            return redirect('/admin/login/', code=302)


class MyRestrictedModelView(MyModelView):

    def is_accessible(self):
        if g.user is not None and g.user.is_admin:
            return True
        return False


class UserView(MyRestrictedModelView):
    can_create = False
    column_list = ['country', 'email', 'is_admin', 'activated']
    column_exclude_list = ['password']
    form_excluded_columns = ['password', 'procurements_added', 'procurements_approved']


class ProcurementView(MyModelView):
    column_list = [
        'country',
        'medicine',
        'pack_size',
        'unit_of_measure',
        'container',
        'pack_price_usd',
        'quantity',
        'supplier',
        'manufacturer',
        'date',
        'source',
        'approved'
    ]
    form_excluded_columns = [
        'country',
        'approved_by',
        'added_by',
        'added_on',
        ]

    column_formatters = dict(
        country=macro('render_country'),
        medicine=macro('render_procurement_medicine'),
        manufacturer=macro('render_procurement_manufacturer'),
        pack_price_usd=macro('render_price'),
        start_date=macro('render_date'),
        quantity=macro('render_quantity'),
        date=macro('render_procurement_date'),
        approved=macro('render_approve'),
        )
    column_sortable_list = [
        ('country', models.Country.name),
        ('medicine', models.Medicine.name),
        ('pack_size', models.Procurement.pack_size),
        ('unit_of_measure', models.Procurement.unit_of_measure),
        ('container', models.Procurement.container),
        ('pack_price_usd', models.Procurement.pack_price_usd),
        ('quantity', models.Procurement.quantity),
        ('source', models.Source.name),
        ('approved', models.Procurement.approved),
        ('supplier', models.Supplier.name),
        ]

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.country_id = g.user.country.country_id if g.user.country else None
            model.added_by = g.user

    def get_list(self, page, sort_column, sort_desc, search, filters, execute=True):
        # Todo: add some custom logic here?
        count, query = super(ProcurementView, self).get_list(page, sort_column, sort_desc, search, filters, execute=False)
        query = query.all()
        return count, query


class MedicineView(MyRestrictedModelView):
    column_list = [
        'name',
        'dosage_form',
        ]
    column_sortable_list = [
        ('name', models.Medicine.name),
        ('dosage_form', models.DosageForm.name),
        ]
    form_excluded_columns = [
        'benchmarks',
        'products',
        'added_by',
        ]

    def after_model_change(self, form, model, is_created):
        if is_created:
            model.added_by = g.user


class ManufacturerView(MyModelView):
    column_exclude_list = [
        'added_by',
        ]
    form_excluded_columns = [
        'added_by',
        ]
    column_sortable_list = [
        ('country', models.Country.name),
        ]
    column_searchable_list = [
        'name',
        ]
    column_formatters = dict(
        country=macro('render_country'),
        )

    def after_model_change(self, form, model, is_created):
        if is_created:
            model.added_by = g.user


class SupplierView(MyModelView):
    column_list = [
        'name',
        'street_address',
        'website',
        'contact',
        ]
    column_sortable_list = [
        ('name', models.Supplier.name),
        ('contact', models.Supplier.contact),
        ('street_address', models.Supplier.street_address),
        ('website', models.Supplier.website),
        ]
    form_excluded_columns = [
        'added_by',
        'authorized',
        'procurements',
        ]
    column_searchable_list = [
        'name',
        'street_address',
        'website',
        'contact',
        ]


# Customized index view that handles login & registration
class HomeView(AdminIndexView):

    @expose('/')
    def index(self):
        # if not g.user.is_authenticated():
        #     return redirect(HOST + "login/")
        return self.render('admin/home.html')
        # return render_template('admin/home.html')

    # @expose('/logout/')
    # def logout_view(self):
    #     login.logout_user()
    #     return redirect(url_for('.index'))


admin = Admin(app, name='Medicine Prices Database', base_template='admin/my_master.html', index_view=HomeView(name='Home'))

admin.add_view(UserView(models.User, db.session, name="Users", endpoint='user'))

admin.add_view(MyRestrictedModelView(models.DosageForm, db.session, name="Dosage Forms", endpoint='dosage_form', category='Medicines'))
admin.add_view(MyRestrictedModelView(models.Ingredient, db.session, name="Medicine Components", endpoint='ingredient', category='Medicines'))
admin.add_view(MedicineView(models.Medicine, db.session, name="Available Medicines", endpoint='medicine', category='Medicines'))
admin.add_view(MyRestrictedModelView(models.BenchmarkPrice, db.session, name="Benchmark Prices", endpoint='benchmark_price', category='Medicines'))

admin.add_view(MyRestrictedModelView(models.Incoterm, db.session, name="Incoterms", endpoint='incoterm', category='Form Options'))
admin.add_view(MyRestrictedModelView(models.AvailableContainers, db.session, name="Containers", endpoint='container', category='Form Options'))
admin.add_view(MyRestrictedModelView(models.AvailableUnits, db.session, name="Units of Measure", endpoint='units', category='Form Options'))
admin.add_view(MyRestrictedModelView(models.AvailableProcurementMethods, db.session, name="Procurement Methods", endpoint='procurement_method', category='Form Options'))

admin.add_view(ManufacturerView(models.Manufacturer, db.session, name="Manufacturer", endpoint='manufacturer'))
admin.add_view(SupplierView(models.Supplier, db.session, name="Supplier", endpoint='supplier'))
admin.add_view(ProcurementView(models.Procurement, db.session, name="Procurements", endpoint='procurement'))
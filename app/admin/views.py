from flask import url_for, abort, render_template, redirect, flash
from flask_login import login_required, current_user

from . import admin_blueprint as admin
from forms import DepartmentForm, RoleForm, UserAssignForm
from app import db
from app.models import Department, Role, User

from app.helper.decorator import admin_required


# add admin dashboard view
@admin.route('/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    print(dir(current_user))
    print(current_user.username)
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        abort(403)

    return render_template('admin/admin_dashboard.html', title="Admin Dashboard")


# Department Views


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
@admin_required
def list_departments():
    """
    List all departments
    """


    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    """
    Add a department to the database
    """

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_department(id):
    """
    Edit a department
    """

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)  # pass obj to the form (To edit the form, load data from database to fill the form)
    if form.validate_on_submit(): # method is POST ( only if the form is submitted)
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_department(id):
    """
    Delete a department from the database
    """

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


@admin.route('/roles')
@login_required
@admin_required
def list_roles():
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')



@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_role():
    """
    Add a role to the database
    """

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_role(id):
    """
    Edit a role
    """

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_role(id):
    """
    Delete a role from the database
    """

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")



# Employee Views

@admin.route('/employees')
@login_required
@admin_required
def list_employees():
    """
    List all employees
    """

    employees = User.query.filter_by(is_employee=True).all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """

    employee = User.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = UserAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')
{
    'name': 'hms',
    'summary': 'Hospitals Management System',
    'author': 'Youmna',
    'category': 'Services',
    'version': '0.1',
    'depends': ['base','crm'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'reports/report_action.xml',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_customer_views.xml',
        'reports/patient_report.xml',

    ],
    'installable': True,
    'application': True,
}


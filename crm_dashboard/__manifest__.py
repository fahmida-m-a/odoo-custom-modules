{
    'name': 'CRM Dashboard',
    'version': '19.0.1.0',
    'sequence':'2',
    'depends':['base','web','crm','sale'],
    'installable': True,
    'application': True,
'data': [
       'security/user_groups.xml',
       'views/crm_dashboard_menu.xml',
       'views/crm_team.xml',
   ],'assets': {
       'web.assets_backend': [
           'crm_dashboard/static/src/js/dashboard.js',
           'crm_dashboard/static/src/xml/dashboard.xml',
           'https://cdn.jsdelivr.net/npm/chart.js',
       ],
},
}


# 'assets': {
#     'web.assets_backend': [
#         'your_module/static/src/js/your_chart_component.js',
#         # Include a local Chart.js library if you are not using Odoo's built-in version
#         # '/your_module/static/src/js/libs/chart.js',
#     ],
# },
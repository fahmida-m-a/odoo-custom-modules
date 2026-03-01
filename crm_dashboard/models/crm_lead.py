from odoo import models, api
from datetime import datetime, date, timedelta

class CrmLead(models.Model):
   _inherit = 'crm.lead'

   @api.model
   def get_crm_dashboard_data(self, period='year'):
       user = self.env.user
       uid = user.id
       is_manager = user.has_group("crm_dashboard.crm_dashboard_manager")
       print("Is manager",is_manager)
       print("uid",user.name)
       # domain2=[]
       # print("orders",self.order_ids)


       today = date.today()
       if period == 'week':
           start_date = today - timedelta(days=today.weekday())
           print(start_date)
       elif period == 'month':
           start_date = today.replace(day=1)
           print(start_date)
       elif period == 'quarter':
           quarter = (today.month - 1) // 3 + 1
           start_date = datetime(today.year, 3 * quarter - 2, 1).date()
           print(start_date)
       else:
           start_date = today.replace(month=1, day=1)
           print(start_date)

       domain = [('create_date', '>=', start_date),('user_id', '=', uid)]

       # if not is_manager:
       #     domain.append(('user_id', '=', uid))
       # leads = self.read_group([('create_date', '>=', start_date),('user_id', '=', uid),('type', '=', 'lead')],
       #     ['id','partner_name','contact_name'],
       #     ['id'])

       leads = self.search([('create_date', '>=', start_date), ('user_id', '=', uid), ('type', '=', 'lead')]).read(['id','name','partner_name','contact_name','probability'])
       print("leaads",leads)
       leads_count = self.search_count(domain + [('type', '=', 'lead')])
       print(leads_count,"leads")
       opps_count = self.search_count(domain + [('type', '=', 'opportunity')])
       opps = self.search(domain + [('type', '=', 'opportunity')])
       expected_revenue = sum(opps.mapped('expected_revenue'))


       invoice_domain = [('move_type', '=', 'out_invoice'),('state', '=', 'posted'),('invoice_date', '>=', start_date),('invoice_user_id', '=', uid)]
       revenue = sum(self.env['account.move'].search(invoice_domain).mapped('amount_total_signed'))
       won_count = self.search_count(domain + [('probability', '=', 100)])
       lost_count = self.search_count(domain + [('active', '=', False), ('probability', '=', 0)])
       total_finished = won_count + lost_count
       win_ratio = round((won_count / total_finished) * 100, 2) if total_finished else 0



       # if not is_manager:
       #     invoice_domain.append(('invoice_user_id', '=', uid))


       if is_manager:
           domain2 = [('create_date', '>=', start_date), ]
           invoice_domain2 = [('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),('invoice_date', '>=', start_date), ]

           all_leads_count = self.search_count(domain2 + [('type', '=', 'lead')])
           all_opps_count = self.search_count(domain2 + [('type', '=', 'opportunity')])
           all_opps = self.search(domain2 + [('type', '=', 'opportunity')])
           all_expected_revenue = sum(all_opps.mapped('expected_revenue'))

           all_revenue = sum(self.env['account.move'].search(invoice_domain2).mapped('amount_total_signed'))

           all_won_count = self.search_count(domain2 + [('probability', '=', 100)])
           all_lost_count = self.search_count(domain2 + [('active', '=', False), ('probability', '=', 0)])
           all_total_finished = all_won_count + all_lost_count
           all_win_ratio = round((all_won_count / all_total_finished) * 100, 2) if all_total_finished else 0

           return {
               'user': self.env.user,
               'domain': domain,
               'domain2': domain2,
               'start_date': start_date,
               'all_leads_count': all_leads_count,
               'all_opps_count': all_opps_count,
               'leads_count': leads_count,
               'leads':leads,
               'opps_count': opps_count,
               'expected_revenue': expected_revenue,
               'all_expected_revenue': all_expected_revenue,
               'revenue': revenue,
               'all_revenue': all_revenue,
               'win_ratio': win_ratio,
               'all_win_ratio': all_win_ratio,
               'won_count': won_count,
               'all_won_count': all_won_count,
               'lost_count': lost_count,
               'all_lost_count': all_lost_count,
               'currency': self.env.company.currency_id.symbol,
               'is_manager': is_manager,
           }
       else:
           return {
               'user': self.env.user,
               'domain': domain,
               'start_date': start_date,
               'leads_count': leads_count,
               'leads': leads,
               'opps_count': opps_count,
               'expected_revenue': expected_revenue,
               'revenue': revenue,
               'win_ratio': win_ratio,
               'won_count': won_count,
               'lost_count': lost_count,
               'currency': self.env.company.currency_id.symbol,
               'is_manager': is_manager,
           }


   @api.model
   def get_leads_by_month(self):
        self.env.cr.execute("""
            SELECT to_char(create_date, 'Mon YYYY') AS month, count(id)
            FROM crm_lead
            GROUP BY month
            ORDER BY month
        """)
        return self.env.cr.fetchall()

   @api.model
   def get_activity_pie(self):
       return self.env['mail.activity'].read_group(
           [],
           ['activity_type_id'],
           ['activity_type_id']
       )

   @api.model
   def get_lost_data(self):
       return self.read_group([('active', '=', False)], ['id','expected_revenue'], ['id'])

   @api.model
   def get_leads_by_medium(self):
       return self.read_group([], ['medium_id'], ['medium_id'])

   @api.model
   def get_leads_by_campaign(self):
       return self.read_group([], ['campaign_id'], ['campaign_id'])









   # @api.model
   # def get_lost_data(self):
   #     data = self.search([('active', '=', False)])
   #     print("lost data", data)
   #     return {
   #         'data': data,
   #         'count': len(data),
   #         'lost':data.mapped('id'),
   #         'amount': sum(data.mapped('expected_revenue')),
   #     }









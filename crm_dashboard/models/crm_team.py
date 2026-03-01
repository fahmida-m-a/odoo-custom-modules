from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    crm_state = fields.Many2one('crm.stage',string='CRM State')
    print("crm_state")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.opportunity_id and order.team_id.crm_state:
                print("ooooohhh!!")
                if order.opportunity_id.stage_id != order.team_id.crm_state:
                    order.opportunity_id.stage_id = order.team_id.crm_state
        return res
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_view_bom_structure(self):
        print("action_view_bom_structure")

        # for rec in self.bom_id.bom_line_ids:
        #  print("rec_id:",rec.product_id)

        action = {
            'view_mode': 'list,form',
            'res_model': 'mrp.bom.line',
            # 'res_model': 'report.mrp.report_bom_structure',
            # 'views': [(False, 'list'),(False, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': 2,
                  }
        return action
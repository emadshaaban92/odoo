from odoo import fields, models


class StageTimeMixin(models.AbstractModel):
    _name = "stage.time.mixin"
    _description = "Mixin to compute the time a record spent in each stage"

    time_per_stage = fields.Char(compute="_compute_time_per_stage", help="JSON string that maps stage ids to ms and days")

    def _compute_time_per_stage(self):
        for record in self:
            record.time_per_stage = record._get_json_time_in_stages('stage_id')

    def _get_stages_order(self, state_field_name):
        dic = {}
        order = 0

        for stage in self.env[self._fields[state_field_name]._related_comodel_name].search([]):
            dic[stage.id] = order
            order += 1
        return dic

    def _link_tracking_to_order(self, mail_tracking_value_records, state_field_name):
        tracking_records_with_order = []
        stages_order = self._get_stages_order(state_field_name)

        for record in mail_tracking_value_records:
            if record.old_value_integer in stages_order and record.new_value_integer in stages_order:
                tracking_records_with_order.append({
                    'record': record,
                    'old_order': stages_order[record.old_value_integer],
                    'new_order': stages_order[record.new_value_integer],
                })
        return tracking_records_with_order

    def _get_time_in_stage(self, trackings):
        current_stage_order = trackings[0]['new_order']
        get_value = False
        stage_id_with_time = {}
        record = self.env['mail.tracking.value']

        for tracking in trackings:
            if get_value is True:
                stage_id_with_time[record.old_value_integer] = record.create_date - tracking['record'].create_date
                get_value = False
            if current_stage_order == 0:
                break
            if (tracking['old_order'] < current_stage_order and tracking['new_order'] >= current_stage_order):
                record = tracking['record']
                current_stage_order = tracking['old_order']
                get_value = True
        if get_value is True:
            stage_id_with_time[record.old_value_integer] = record.create_date - self.create_date
        return stage_id_with_time

    def _json_stage_id_with_time(self, stages_time):
        """Return json"""
        total_json = "{"

        for stage_id in stages_time:
            if total_json != "{":
                total_json += ','
            values = f'"ms":{stages_time[stage_id].seconds * 1000 + stages_time[stage_id].microseconds / 1000},'\
                     f'"days":{stages_time[stage_id].days}'
            json = f'"{stage_id}":{{{values}}}'
            total_json += json
        return total_json + "}"

    def _get_json_time_in_stages(self, state_field_name):
        """ Returns a JSON in a string that can be parsed by the client-side to map each stage to a time spent

        :param state_field_name: string, the name of the field for stages
        :return: a string containing a JSON object {stage_id: ms, days}
        """
        stages_with_time_json = "{}"
        mail_tracking_records = self.env['mail.tracking.value'].search([
            ('mail_message_id.res_id', '=', self.id),
            ('mail_message_id.model', '=', self._name),
            ('field', '=', self.env.ref(f'{self._original_module}.field_{self._table}__{state_field_name}').id)
        ], order='create_date desc')

        if mail_tracking_records:
            tracking_records_with_order = self._link_tracking_to_order(mail_tracking_records, state_field_name)
            if tracking_records_with_order:
                time_in_stage = self._get_time_in_stage(tracking_records_with_order)
                if time_in_stage:
                    stages_with_time_json = self._json_stage_id_with_time(time_in_stage)
        return stages_with_time_json

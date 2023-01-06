

import random
import time
import json
import inspect


from odoo import models
from odoo.tests.common import TransactionCase, tagged
from collections import defaultdict
from statistics import fmean, stdev

NB_TIME = 10

@tagged('post_install', '-at_install')
class TestCompute(TransactionCase):

    def all_compute(self, match, file):
        self.env.invalidate_all()
        rng = random.Random("a")
        sizes = [1] * NB_TIME + [3] * NB_TIME + [80] * NB_TIME + [1000] * NB_TIME

        res = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for model_name in self.env.registry:
            Model: models.BaseModel = self.env[model_name]
            if Model._abstract or not Model._auto:
                continue

            records = Model.with_context(active_test=False).search([], order='id')
            for field in Model._fields.values():
                if field.store or not field.compute or not records:
                    continue

                func = field.compute
                if isinstance(field.compute, str):
                    func = getattr(records, field.compute)

                source = inspect.getsource(func)
                if match not in source and field.name not in ('qty_available'):
                    continue

                for size in sizes:
                    if size > len(records):
                        continue
                    rec = Model.browse(rng.sample(records._ids, size))

                    begin = time.time_ns()
                    res_mapped = rec.mapped(field.name)
                    end = time.time_ns()

                    res[Model._name][field.name][size].append((
                        (end - begin) / 1_000_000,
                        rec._ids,
                        str(res_mapped)
                    ))

                    self.env.invalidate_all()

        with open(file, 'wt') as fw:
            print(f"Save result {len(res)}")
            json.dump(res, fw)

    def test_all_compute_aggregate(self):
        self.all_compute('aggregate(', 'res_compute_aggregate.json')

    def test_all_compute_read_group(self):
        self.all_compute('read_group(', 'res_compute_read_group.json')

    def test_summarize_result(self):
        with open('res_compute_aggregate.json', 'rt') as fw:
            res_agg = json.load(fw)

        with open('res_compute_read_group.json', 'rt') as fw:
            res_gro = json.load(fw)

        def x_bests(values, x):
            return sorted(values)[:x]

        for model_name, res_m in res_agg.items():
            for field_name, res_f in res_m.items():
                print(f"For {model_name}..{field_name}:")
                for size, res_size in res_f.items():
                    if model_name not in res_gro or field_name not in res_gro[model_name]:
                        continue
                    # 1 is read_group
                    # 2 is aggregate
                    sample_1, rec_1, compute_1 = zip(*res_gro[model_name][field_name][size])
                    sample_2, rec_2, compute_2 = zip(*res_size)

                    if rec_1 != rec_2:
                        print(f"Different records {rec_1} != {rec_2}")
                    if compute_1 != compute_2 and rec_1 == rec_2:
                        print(f"Different values {compute_1} != {compute_2} for {rec_1}")

                    sample_1 = x_bests(sample_1, 5)
                    sample_2 = x_bests(sample_2, 5)
                    # print(f"\t- ({size}): {fmean(sample_1):.2f} ms -+ {stdev(sample_1):.2f} => {fmean(sample_2):.2f} ms -+ {stdev(sample_2):.2f}")

/** @odoo-module **/

import { Domain } from "@web/core/domain";
import { makeWithSearch } from "./helpers";
import { patchDate } from "../../helpers/utils";
import { serviceRegistry } from "@web/webclient/service_registry";
import { ormService } from "@web/services/orm_service";
import { viewService } from "@web/views/view_service";
import { makeFakeLocalizationService, makeFakeUserService } from "../../helpers/mock_services";

const { Component, tags } = owl;
const { xml } = tags;

class TestComponent extends Component {}
TestComponent.template = xml`<div class="o_test_component"/>`;

async function makeSearchModel(params, props) {
  const withSearchProps = Object.assign(
    {
      Component: TestComponent,
      modelName: "foo",
    },
    props
  );
  if (!withSearchProps.fields) {
    /** @todo we should avoid that: review load_views and parsing in search model */
    withSearchProps.fields = testConfig.serverData.models[withSearchProps.modelName].fields;
  }
  const component = await makeWithSearch(params, withSearchProps);
  return component.env.searchModel;
}

function sanitizeSearchItems(model) {
  const searchItems = Object.values(model.searchItems); // We should not access searchItems but there is a problem with getSearchItems --> comparisons are not sent back in some cases
  return searchItems.map((searchItem) => {
    const copy = Object.assign({}, searchItem);
    delete copy.groupId;
    delete copy.groupNumber;
    delete copy.id;
    return copy;
  });
}

let testConfig;

QUnit.module("SearchModel", (hooks) => {
  hooks.beforeEach(() => {
    const serverData = {
      models: {
        foo: {
          fields: {
            display_name: { string: "Displayed name", type: "char" },
            foo: {
              string: "Foo",
              type: "char",
              default: "My little Foo Value",
              store: true,
              sortable: true,
            },
            date_field: { string: "Date", type: "date", store: true, sortable: true },
            float_field: { string: "Float", type: "float" },
            bar: { string: "Bar", type: "many2one", relation: "partner" },
          },
          records: [],
        },
        partner: {
          fields: {
            foo: { string: "Foo", type: "char" },
            bar: { string: "Bar", type: "boolean" },
            int_field: { string: "Int Field", type: "integer", group_operator: "sum" },
            company_id: { string: "company", type: "many2one", relation: "company" },
            company_ids: { string: "Companies", type: "many2many", relation: "company" },
            category_id: { string: "category", type: "many2one", relation: "category" },
            state: {
              string: "State",
              type: "selection",
              selection: [
                ["abc", "ABC"],
                ["def", "DEF"],
                ["ghi", "GHI"],
              ],
            },
          },
          records: [
            {
              id: 1,
              bar: true,
              foo: "yop",
              int_field: 1,
              company_ids: [3],
              company_id: 3,
              state: "abc",
              category_id: 6,
            },
            {
              id: 2,
              bar: true,
              foo: "blip",
              int_field: 2,
              company_ids: [3],
              company_id: 5,
              state: "def",
              category_id: 7,
            },
            {
              id: 3,
              bar: true,
              foo: "gnap",
              int_field: 4,
              company_ids: [],
              company_id: 3,
              state: "ghi",
              category_id: 7,
            },
            {
              id: 4,
              bar: false,
              foo: "blip",
              int_field: 8,
              company_ids: [5],
              company_id: 5,
              state: "ghi",
              category_id: 7,
            },
          ],
        },
        company: {
          fields: {
            name: { string: "Display Name", type: "char" },
            parent_id: { string: "Parent company", type: "many2one", relation: "company" },
            category_id: { string: "Category", type: "many2one", relation: "category" },
          },
          records: [
            { id: 3, name: "asustek", category_id: 6 },
            { id: 5, name: "agrolait", category_id: 7 },
          ],
        },
        category: {
          fields: {
            name: { string: "Category Name", type: "char" },
          },
          records: [
            { id: 6, name: "gold" },
            { id: 7, name: "silver" },
          ],
        },
      },
    };

    const fakeLocalizationService = makeFakeLocalizationService();
    const fakeUserService = makeFakeUserService();

    serviceRegistry.add("localization", fakeLocalizationService);
    serviceRegistry.add("orm", ormService);
    serviceRegistry.add("user", fakeUserService);
    serviceRegistry.add("view", viewService);

    testConfig = { serverData, serviceRegistry };
  });

  QUnit.test("parsing empty arch", async function (assert) {
    const model = await makeSearchModel({ testConfig });
    assert.deepEqual(sanitizeSearchItems(model), []);
  });

  QUnit.test("parsing one field tag", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <field name="bar"/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Bar",
        fieldName: "bar",
        fieldType: "many2one",
        type: "field",
      },
    ]);
  });

  QUnit.test("parsing one separator tag", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <separator/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), []);
  });

  QUnit.test("parsing one separator tag and one field tag", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <separator/>
            <field name="bar"/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Bar",
        fieldName: "bar",
        fieldType: "many2one",
        type: "field",
      },
    ]);
  });

  QUnit.test("parsing one filter tag", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="filter" string="Hello" domain="[]"/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Hello",
        domain: new Domain("[]"),
        type: "filter",
      },
    ]);
  });

  QUnit.test("parsing one filter tag with date attribute", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="date_filter" string="Date" date="date_field"/>
        </search>
      `,
      }
    );
    const dateFilterId = model.getSearchItems((f) => f.type === "dateFilter")[0].id;
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        defaultGeneratorId: "this_month",
        description: "Date",
        fieldName: "date_field",
        fieldType: "date",
        type: "dateFilter",
      },
      {
        comparisonOptionId: "previous_period",
        dateFilterId,
        description: "Date: Previous Period",
        type: "comparison",
      },
      {
        comparisonOptionId: "previous_year",
        dateFilterId,
        description: "Date: Previous Year",
        type: "comparison",
      },
    ]);
  });

  QUnit.test("parsing one groupBy tag", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="groupby" string="Hi" context="{ 'group_by': 'date_field:day'}"/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        defaultIntervalId: "day",
        description: "Hi",
        fieldName: "date_field",
        fieldType: "date",
        type: "dateGroupBy",
      },
    ]);
  });

  QUnit.test("parsing two filter tags", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="filter_1" string="Hello One" domain="[]"/>
            <filter name="filter_2" string="Hello Two" domain="[('bar', '=', 3)]"/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Hello One",
        domain: new Domain("[]"),
        type: "filter",
      },
      {
        description: "Hello Two",
        domain: new Domain("[('bar', '=', 3)]"),
        type: "filter",
      },
    ]);
  });

  QUnit.test("parsing two filter tags separated by a separator", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="filter_1" string="Hello One" domain="[]"/>
            <separator/>
            <filter name="filter_2" string="Hello Two" domain="[('bar', '=', 3)]"/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Hello One",
        domain: new Domain("[]"),
        type: "filter",
      },
      {
        description: "Hello Two",
        domain: new Domain("[('bar', '=', 3)]"),
        type: "filter",
      },
    ]);
  });

  QUnit.test("parsing one filter tag and one field", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="filter" string="Hello" domain="[]"/>
            <field name="bar"/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Hello",
        domain: new Domain("[]"),
        type: "filter",
      },
      {
        description: "Bar",
        fieldName: "bar",
        fieldType: "many2one",
        type: "field",
      },
    ]);
  });

  QUnit.test("parsing two field tags", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <field name="foo"/>
            <field name="bar"/>
        </search>
      `,
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Foo",
        fieldName: "foo",
        fieldType: "char",
        type: "field",
      },
      {
        description: "Bar",
        fieldName: "bar",
        fieldType: "many2one",
        type: "field",
      },
    ]);
  });

  QUnit.test("parsing a searchpanel tag", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <searchpanel/>
        </search>
      `,
        loadSearchPanel: true,
      }
    );
    assert.deepEqual(model.getSections(), []);
  });

  QUnit.test("parsing a searchpanel field select one", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <searchpanel>
              <field name="company_id"/>
            </searchpanel>
        </search>
      `,
        modelName: "partner",
        loadSearchPanel: true,
      }
    );
    const sections = model.getSections();
    for (const section of sections) {
      section.values = [...section.values];
    }
    assert.deepEqual(sections, [
      {
        activeValueId: false,
        color: null,
        description: "company",
        empty: false,
        enableCounters: false,
        expand: false,
        fieldName: "company_id",
        hierarchize: true,
        icon: "fa-folder",
        id: 1,
        limit: 200,
        parentField: "parent_id",
        rootIds: [false, 3, 5],
        type: "category",
        values: [
          [
            false,
            {
              bold: true,
              childrenIds: [],
              display_name: "All",
              id: false,
              parentId: false,
            },
          ],
          [
            3,
            {
              childrenIds: [],
              display_name: "asustek",
              id: 3,
              parentId: false,
              parent_id: false,
            },
          ],
          [
            5,
            {
              childrenIds: [],
              display_name: "agrolait",
              id: 5,
              parentId: false,
              parent_id: false,
            },
          ],
        ],
      },
    ]);
  });

  QUnit.test("parsing a searchpanel field select one", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
          <search>
              <searchpanel>
                <field name="company_id" select="multi"/>
              </searchpanel>
          </search>
        `,
        modelName: "partner",
        loadSearchPanel: true,
      }
    );
    const sections = model.getSections();
    for (const section of sections) {
      section.values = [...section.values];
    }
    assert.deepEqual(sections, [
      {
        color: null,
        description: "company",
        domain: "[]",
        empty: false,
        enableCounters: false,
        expand: false,
        fieldName: "company_id",
        groupBy: null,
        icon: "fa-filter",
        id: 1,
        limit: 200,
        type: "filter",
        values: [
          [
            3,
            {
              checked: false,
              display_name: "asustek",
              id: 3,
            },
          ],
          [
            5,
            {
              checked: false,
              display_name: "agrolait",
              id: 5,
            },
          ],
        ],
      },
    ]);
  });

  QUnit.test("process search default group by", async function (assert) {
    assert.expect(1);
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="group_by" context="{ 'group_by': 'foo'}"/>
        </search>
      `,
        context: { search_default_group_by: 14 },
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        defaultRank: 14,
        description: "Foo",
        fieldName: "foo",
        fieldType: "char",
        type: "groupBy",
        isDefault: true,
      },
    ]);
  });

  QUnit.test("process favorite filters", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        irFilters: [
          {
            user_id: [2, "Mitchell Admin"],
            name: "Sorted filter",
            id: 5,
            context: `{"group_by":["foo","bar"]}`,
            sort: '["foo", "-bar"]',
            domain: "[('user_id', '=', uid)]",
            is_default: false,
            model_id: "res.partner",
            action_id: false,
          },
        ],
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        context: {},
        description: "Sorted filter",
        domain: new Domain("[('user_id', '=', uid)]"),
        groupBys: ["foo", "bar"],
        orderBy: [
          {
            asc: true,
            name: "foo",
          },
          {
            asc: false,
            name: "bar",
          },
        ],
        removable: true,
        serverSideId: 5,
        type: "favorite",
        userId: 2,
      },
    ]);
  });

  QUnit.test("process dynamic filters", async function (assert) {
    assert.expect(1);
    const model = await makeSearchModel(
      { testConfig },
      {
        dynamicFilters: [
          {
            description: "Quick search",
            domain: [["id", "in", [1, 3, 4]]],
          },
        ],
      }
    );
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Quick search",
        domain: new Domain([["id", "in", [1, 3, 4]]]),
        isDefault: true,
        type: "filter",
      },
    ]);
  });

  QUnit.test("toggle a filter", async function (assert) {
    assert.expect(3);
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="filter" string="Filter" domain="[['foo', '=', 'a']]"/>
        </search>
      `,
      }
    );
    const filterId = Object.keys(model.searchItems).map((key) => Number(key))[0];
    assert.deepEqual([], model.domain);
    model.toggleSearchItem(filterId);
    assert.deepEqual([["foo", "=", "a"]], model.domain);
    model.toggleSearchItem(filterId);
    assert.deepEqual([], model.domain);
  });

  QUnit.test("toggle a date filter", async function (assert) {
    patchDate(2019, 0, 6, 15, 0, 0);
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="date_filter" date="date_field" string="DateFilter"/>
        </search>
      `,
      }
    );
    const filterId = Object.keys(model.searchItems).map((key) => Number(key))[0];
    model.toggleDateFilter(filterId);
    assert.deepEqual(
      ["&", ["date_field", ">=", "2019-01-01"], ["date_field", "<=", "2019-01-31"]],
      model.domain
    );
    model.toggleDateFilter(filterId, "first_quarter");
    assert.deepEqual(
      [
        "|",
        "&",
        ["date_field", ">=", "2019-01-01"],
        ["date_field", "<=", "2019-01-31"],
        "&",
        ["date_field", ">=", "2019-01-01"],
        ["date_field", "<=", "2019-03-31"],
      ],
      model.domain
    );
    model.toggleDateFilter(filterId, "this_year");
    assert.deepEqual([], model.domain);
  });

  QUnit.test("toggle a groupBy", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="groupBy" string="GroupBy" context="{'group_by': 'foo'}"/>
        </search>
      `,
      }
    );
    const filterId = Object.keys(model.searchItems).map((key) => Number(key))[0];
    assert.deepEqual(model.groupBy, []);
    model.toggleSearchItem(filterId);
    assert.deepEqual(model.groupBy, ["foo"]);
    model.toggleSearchItem(filterId);
    assert.deepEqual(model.groupBy, []);
  });

  QUnit.test("toggle a date groupBy", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
            <filter name="date_groupBy" string="DateGroupBy" context="{'group_by': 'date_field:day'}"/>
        </search>
      `,
      }
    );
    const filterId = Object.keys(model.searchItems).map((key) => Number(key))[0];
    assert.deepEqual(model.groupBy, []);
    model.toggleDateGroupBy(filterId);
    assert.deepEqual(model.groupBy, ["date_field:day"]);
    model.toggleDateGroupBy(filterId, "week");
    assert.deepEqual(model.groupBy, ["date_field:week", "date_field:day"]);
    model.toggleDateGroupBy(filterId);
    assert.deepEqual(model.groupBy, ["date_field:week"]);
    model.toggleDateGroupBy(filterId, "week");
    assert.deepEqual(model.groupBy, []);
  });

  QUnit.test("create a new groupBy", async function (assert) {
    const model = await makeSearchModel({ testConfig });
    model.createNewGroupBy({ name: "foo", string: "Foo", type: "char" });
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Foo",
        fieldName: "foo",
        fieldType: "char",
        type: "groupBy",
      },
    ]);
    assert.deepEqual(model.groupBy, ["foo"]);
  });

  QUnit.test("create a new dateGroupBy", async function (assert) {
    const model = await makeSearchModel(
      { testConfig },
      {
        arch: `
        <search>
          <filter name="foo" string="Foo" context="{'group_by': 'foo'}"/>
        </search>
      `,
      }
    );
    model.createNewGroupBy({ name: "date_field", type: "date" });
    assert.deepEqual(sanitizeSearchItems(model), [
      {
        description: "Foo",
        fieldName: "foo",
        fieldType: "char",
        type: "groupBy",
      },
      {
        defaultIntervalId: "month",
        description: "date_field",
        fieldName: "date_field",
        fieldType: "date",
        type: "dateGroupBy",
      },
    ]);
    assert.deepEqual(model.groupBy, ["date_field:month"]);
  });
});

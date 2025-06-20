<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";

const generatorViewStore = useGeneratorViewStore();
const mainStore = useMainStore();

const {
  cafData,
} = storeToRefs(generatorViewStore)

const {
  mira_id,
} = storeToRefs(mainStore)

import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {GeneratorListData} from "src/types";
import {useRouter} from "vue-router";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import GeneratorManageDialog from "pages/generator/components/dialogs/GeneratorManageDialog.vue";
import LayoutHCF from "components/LayoutHCF.vue";

const $q = useQuasar()
const router = useRouter()
const listData = ref<GeneratorListData[]>([])

const currentData = ref(null);

const columns = [
  { name: 'discode', align: 'center', label: 'Код', field: 'discode', sortable: true },
  { name: 'discpl', align: 'center', label: 'Дисциплина', field: 'discpl', sortable: true },
  { name: 'person', align: 'center', label: 'Составитель', field: 'person', sortable: true },
  { name: 'kaf', align: 'center', label: 'Кафедра', field: 'kafcode', sortable: true },
  { name: 'rukprog', align: 'center', label: 'Согласован', field: 'rukprog', sortable: true },
  { name: 'zavkaf', align: 'center', label: 'Утвержден', field: 'zavkaf', sortable: true },
  { name: 'status_verbose', align: 'center', label: 'Статус', field: 'status_verbose', sortable: true },
  { name: 'control', align: 'center', label: 'Управление', field: 'type', sortable: false },
];

const typeFilterLabel = {
  rop: 'Руководитель ОП',
  fac: 'Директор',
  zav: 'Заведующий кафедры',
  person: 'Разработчик РПД',
}

const STATUSES = {
  "Назначен": {
    color: "grey-2",
    textColor: "black",
    index: 1,
    title: "Назначен",
  },
  "Заполняется": {
    color: "cyan-5",
    textColor: "white",
    index: 2,
    title: "Заполняется",
  },
  "Требует моего согласования/утверждения": {
    color: "amber-6",
    textColor: "black",
    index: 3,
    title: "Требует моего согласования/утверждения",
  },
  "Отправлен на проверку": {
    color: "light-green-6",
    textColor: "white",
    index: 3,
    title: "Отправлен на проверку",
  },
  "Требуются правки": {
    color: "red-5",
    textColor: "white",
    index: 4,
    title: "Требуются правки",
  },
  "Утвержден": {
    color: "green-5",
    textColor: "white",
    index: 5,
    title: "Утвержден",
  },
}

const statusFilter = ref();
const groupFilter = ref($q.localStorage.getItem("surp_groupfilter") ? $q.localStorage.getItem("surp_groupfilter") : '')
const discplFilter = ref($q.localStorage.getItem("surp_discplfilter") ? $q.localStorage.getItem("surp_discplfilter") : '')
const myFilter = ref(LocalStorage.getItem('surp_myfilter') || 0)
const textFilter = ref<String>(LocalStorage.getItem('surp_rpdfilter') || '')

const filteredListData = computed(() => {
  let txtFilter = textFilter.value.trim().toLowerCase();

  return _(listData.value)
    .filter(x => {
      return (myFilter.value == 0 || x.type.includes('person'))
        && ((txtFilter == '' || x.person.toLowerCase().includes(txtFilter))
          || (txtFilter == '' || x.abbr.toLowerCase().includes(txtFilter))
          || (txtFilter == '' || x.discode.toLowerCase().includes(txtFilter))
          || (txtFilter == '' || x.discpl.toLowerCase().includes(txtFilter)))
        && (!statusFilter.value || x.status_verbose == statusFilter.value)
    })
    .orderBy(x => [x.abbr, x.yr, x.discode], 'asc')
    .groupBy(x => `${x.abbr}-${x.yr.toString().slice(-2)}`)
    .toPairs()
    .map((item) => {
      let items = item[1];
      return [
        item[0],
        {
          items: items,
          types: _(items).map(x => x.type).flatten().uniq().value(),
          statuses: _(items).orderBy(x => STATUSES[x["status_verbose"]].index).groupBy('status_verbose').value(),
        }
      ]
    })
    .fromPairs()
    .value()
})


function openManageDialog(id, item) {
  $q.dialog({
    component: GeneratorManageDialog,
    componentProps: {
      id: id,
      data: item,
    }
  }).onOk(() => {
    getProgramData()
  })
}

async function getProgramData() {
  listData.value = []
  let r = await api.get("/api/generator/get-program-list/")
  listData.value = r.data
}

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

function getEditRules(type) {
  const rules = ['person']
  return type.some(q => rules.includes(q))
}

function getViewRules(type) {
  const rules = ['rop', 'fac', 'zav']
  return type.some(q => rules.includes(q))
}

function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-3' : 'bg-white'
}

watch([discplFilter, groupFilter, myFilter, textFilter], () => {
  $q.localStorage.setItem("surp_discplfilter", discplFilter.value)
  $q.localStorage.setItem("surp_groupfilter", groupFilter.value)
  $q.localStorage.setItem("surp_myfilter", myFilter.value)
  $q.localStorage.setItem("surp_rpdfilter", textFilter.value)
});

onBeforeMount(async () => {
  $q.loading.show({message: "Загрузка дисциплин"})
  await getProgramData()
  $q.loading.hide()
});

function rowClassFn (row) {
  return `rpd-row status-${row.status}`;
}

</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr 220px auto; gap: 8px">
          <q-input outlined label="Поиск по аббревиатуре, дисциплине, разработчику программы" v-model="textFilter"/>
          <!--        <q-input outlined label="Дисциплина" v-model="discplFilter"/>-->
          <q-select v-model="statusFilter"
                    label="Статус"
                    :options="_.map(STATUSES)"
                    option-label="title"
                    option-value="title"
                    emit-value
                    map-options
                    clearable
          />
          <q-toggle outlined label="Только мои" v-model="myFilter" :true-value="1" :false-value="0"/>
        </div>
      </div>
    </template>
    <template #content>
      <div v-if="_.size(filteredListData) > 0"
           style="display: grid; grid-template-columns: 300px 1fr; overflow: hidden;height: 100%"
      >
        <q-list
          style="overflow-y:auto; height: 100%; box-shadow: 0 0 8px silver; z-index: 100"
          separator
        >
          <q-item
            v-for="(value, key) in filteredListData"
            clickable
            style="display: grid; grid-template-rows: auto auto; gap: 8px"
            :active="currentKey === key"
            @click="currentData = value"
          >
            <div style="display: grid; grid-template-columns: 100px 1fr">
              <div style="display: flex; justify-content: center; align-content: center; font-size: 1.25rem;">
                {{ key }}
              </div>

              <div style="display: flex; flex-wrap: wrap; gap: 8px">
                <q-badge v-for="type in value.types">
                  {{ typeFilterLabel[type] }}
                </q-badge>
              </div>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: start">
              <q-badge
                :text-color="STATUSES[status].textColor"
                :color="STATUSES[status].color"
                v-for="(status_items, status) in value.statuses"
              >
                {{ status_items.length }}
                <q-tooltip
                  style="font-size: 12px; background-color: white; color: black"
                >
                  {{ status }}: {{ status_items.length }}
                </q-tooltip>
              </q-badge>
            </div>
          </q-item>
        </q-list>

    <q-table
      v-if="currentData !== null"
      :rows="currentData.items"
      :columns="columns"
      virtual-scroll
      style="overflow-y: auto; height: 100%;"
      wrap-cells
      row-key="discode"
      flat
      bordered
      separator="cell"
      :rows-per-page-options="[0]"
      :table-row-class-fn="rowClassFn"
    >
      <template #body-cell-kaf="props">
        <q-td>
          {{ cafDataById[props.row.kafcode]?.label }}
        </q-td>
      </template>

      <template #body-cell-rukprog="props">
        <q-td>
          <div :style="{color: props.row.user_confirmed_name === null ? 'grey' : ''}">
            <q-icon
              v-if="props.row.user_confirmed_name !== null"
              name="check"
              color="green"
              size="15px"
            >
            </q-icon>
            {{ props.row.rukprog }}
          </div>
        </q-td>
      </template>

      <template #body-cell-zavkaf="props">
        <q-td>
          <div :style="{color: props.row.user_accepted_name === null ? 'grey' : ''}">
            <q-icon
              v-if="props.row.user_accepted_name !== null"
              name="check"
              color="green"
              size="15px"
            >
            </q-icon>
            {{ props.row.zavkaf }}
          </div>
        </q-td>
      </template>

      <template #body-cell-control="props">
        <q-td>
          <q-btn v-if="getEditRules(props.row.type)" dense flat color="primary" icon="mdi-pencil"
               label="заполнить" @click="router.push(`/generator/${props.row.id}/main`)"/>
          <q-btn v-if="getViewRules(props.row.type)" dense flat color="secondary" icon="mdi-briefcase-eye"
                 label="просмотр" @click="openManageDialog(props.row.id, props.row)"/>
        </q-td>
      </template>
    </q-table>
        <!--          <q-list-->
        <!--            separator-->
        <!--            class="col-3"-->
        <!--          >-->
        <!--            <q-item-->
        <!--              v-for="(value, key) in filteredListData"-->
        <!--              clickable-->
        <!--              v-ripple-->
        <!--              :active="activeElement === key"-->
        <!--              @click="activeElement = key"-->
        <!--            >-->
        <!--             <div class="q-item__section column q-item__section&#45;&#45;main justify-center">-->
        <!--                    <div class="q-item__label">-->
        <!--                      <div style="display: flex; gap: 8px; justify-content: space-between; flex-wrap: wrap;">-->
        <!--                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">-->
        <!--                          <div style="width: 70px">{{ key }}</div>-->

        <!--                          <q-badge v-for="type in value.types">-->
        <!--                            {{ typeFilterLabel[type] }}-->
        <!--                          </q-badge>-->
        <!--                        </div>-->

        <!--                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">-->
        <!--                          <q-badge :text-color="STATUSES[status].textColor" :color="STATUSES[status].color" v-for="(status_items, status) in value.statuses">-->
        <!--                            {{ status }}: {{ status_items.length }}-->
        <!--                          </q-badge>-->
        <!--                        </div>-->
        <!--                      </div>-->
        <!--                    </div>-->

        <!--                  </div>-->
        <!--            </q-item>-->
        <!--          </q-list>-->
        <!--            <q-list-->
        <!--              bordered-->
        <!--              separator-->
        <!--            >-->
        <!--              <q-expansion-item-->
        <!--                v-for="(value, key) in filteredListData"-->
        <!--                :label="key"-->
        <!--                group="programs"-->
        <!--              >-->
        <!--                <template #header class="col-3">-->
        <!--                  <div class="q-item__section column q-item__section&#45;&#45;main justify-center">-->
        <!--                    <div class="q-item__label">-->
        <!--                      <div style="display: flex; gap: 8px; justify-content: space-between">-->
        <!--                        <div style="display: flex; gap: 8px;">-->
        <!--                          <div style="width: 70px">{{ key }}</div>-->

        <!--                          <q-badge v-for="type in value.types">-->
        <!--                            {{ typeFilterLabel[type] }}-->
        <!--                          </q-badge>-->
        <!--                        </div>-->

        <!--                        <div style="display: flex; gap: 8px;">-->
        <!--                          <q-badge :text-color="STATUSES[status].textColor" :color="STATUSES[status].color" v-for="(status_items, status) in value.statuses">-->
        <!--                            {{ status }}: {{ status_items.length }}-->
        <!--                          </q-badge>-->
        <!--                        </div>-->
        <!--                      </div>-->
        <!--                    </div>-->

        <!--                  </div>-->
        <!--                </template>-->

        <!--              <q-card class="col-auto">-->
        <!--                <q-card-section>-->
        <!--                  <div class="rpd-container">-->
        <!--                    <div class="rpd-row rpd-row__header text-weight-bold text-center">-->
        <!--                      <div>Код</div>-->
        <!--                      <div>Дисциплина</div>-->
        <!--                      <div>Составитель</div>-->
        <!--                      <div>Кафедра</div>-->
        <!--                      <div>Согласован</div>-->
        <!--                      <div>Утвержден</div>-->
        <!--                      <div>Статус</div>-->
        <!--                      <div>Управление</div>-->
        <!--                    </div>-->
        <!--                    <div :class="{[`status-${item.status}`]: true}" class="rpd-row rpd-row__body text-center" v-for="(item, key) in value.items">-->
        <!--                      &lt;!&ndash;                       @click="router.push(`/generator/${item.id}/main`)"&ndash;&gt;-->
        <!--                      <div>{{ item.discode }}</div>-->
        <!--                      <div>{{ item.discpl }}</div>-->
        <!--                      <div>{{ item.person }}</div>-->
        <!--                      <div>{{ cafDataById[item.kafcode]?.label }}</div>-->
        <!--                      <div>{{ item.user_confirmed_name }}</div>-->
        <!--                      <div>{{ item.user_accepted_name }}</div>-->
        <!--                      <div>{{ item.status_verbose }}</div>-->
        <!--                      <div>-->
        <!--                        <q-btn v-if="getEditRules(item.type)" dense flat color="primary" icon="mdi-pencil"-->
        <!--                               label="заполнить" @click="router.push(`/generator/${item.id}/main`)"/>-->
        <!--                        <q-btn v-if="getViewRules(item.type)" dense flat color="secondary" icon="mdi-briefcase-eye"-->
        <!--                               label="просмотр" @click="openManageDialog(item.id, item)"/>-->
        <!--                      </div>-->
        <!--                    </div>-->
        <!--                  </div>-->
        <!--                </q-card-section>-->
        <!--              </q-card>-->
        <!--            </q-expansion-item>-->
        <!--          </q-list>-->
        <!--        </div>-->
        <!--        <div v-else class="text-h6">-->
        <!--          <span v-if="_.size(listData) > 0">Не найдены дисциплины с текущими фильтрами</span>-->
        <!--          <span v-else>Дисциплины не назначены</span>-->
        <!--        </div>-->
      </div>
    </template>
  </layout-h-c-f>

</template>

<style scoped lang="scss">
.rpd-container {
  display: grid;
  grid-template-columns: auto repeat(5, 1fr) auto auto;
}

:deep(.rpd-row) {
  //display: contents;

  &.status-0 > td { // "Назначен"
    background: white;
  }

  &.status-1 > td { // "Заполняется"
    background: $light-blue-1;
  }

  &.status-2 > td { // "Отправлен на проверку"
    background: $amber-1;
  }

  &.status-3 > td { // "Утвержден"
    background: $green-1;
  }

  &.status-4 > td { // "Требуются правки"
    background: $red-1;
  }


  //$border: solid 1px silver;
  //
  //> div {
  //  padding: 0.5rem;
  //  border: $border;
  //  border-right: none;
  //  border-bottom: none;
  //
  //  &:last-child {
  //    border-right: $border;
  //  }
  //}
  //
  //&:last-child {
  //  > div {
  //    border-bottom: $border;
  //  }
  //}

  &.rpd-row__body {
    //&:hover {
    //  > div {
    //    background: $info !important;
    //  }
    //}
  }
}

</style>

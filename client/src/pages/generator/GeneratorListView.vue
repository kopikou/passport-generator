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
})

onBeforeMount(async () => {
  $q.loading.show({message: "Загрузка дисциплин"})
  await getProgramData()
  $q.loading.hide()
})

</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="text-center text-h6 q-mb-md">Список рабочих программ дисциплин ИРНИТУ</div>
        <div class="flex justify-between q-mb-sm q-px-sm"
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
      <div class="q-pa-md">
        <div v-if="_.size(filteredListData) > 0">
          <q-list
            bordered
            separator
          >
            <q-expansion-item
              v-for="(value, key) in filteredListData"
              :label="key"
              group="programs"
            >
              <template #header>
                <div class="q-item__section column q-item__section--main justify-center">
                  <div class="q-item__label">
                    <div style="display: flex; gap: 8px; justify-content: space-between">
                      <div style="display: flex; gap: 8px;">
                        <div style="width: 70px">{{ key }}</div>

                        <q-badge v-for="type in value.types">
                          {{ typeFilterLabel[type] }}
                        </q-badge>
                      </div>

                      <div style="display: flex; gap: 8px;">
                        <q-badge :text-color="STATUSES[status].textColor" :color="STATUSES[status].color" v-for="(status_items, status) in value.statuses">
                          {{ status }}: {{ status_items.length }}
                        </q-badge>
                      </div>
                    </div>
                  </div>

                </div>
              </template>
              <q-card>
                <q-card-section>
                  <div class="rpd-container">
                    <div class="rpd-row rpd-row__header text-weight-bold text-center">
                      <div>Код</div>
                      <div>Дисциплина</div>
                      <div>Составитель</div>
                      <div>Кафедра</div>
                      <div>Согласован</div>
                      <div>Утвержден</div>
                      <div>Статус</div>
                      <div>Управление</div>
                    </div>
                    <div :class="{[`status-${item.status}`]: true}" class="rpd-row rpd-row__body text-center" v-for="(item, key) in value.items">
                      <!--                       @click="router.push(`/generator/${item.id}/main`)"-->
                      <div>{{ item.discode }}</div>
                      <div>{{ item.discpl }}</div>
                      <div>{{ item.person }}</div>
                      <div>{{ cafDataById[item.kafcode]?.label }}</div>
                      <div>{{ item.user_confirmed_name }}</div>
                      <div>{{ item.user_accepted_name }}</div>
                      <div>{{ item.status_verbose }} {{item.only_zav_required}}</div>
                      <div>
                        <q-btn v-if="getEditRules(item.type)" dense flat color="primary" icon="mdi-pencil"
                               label="заполнить" @click="router.push(`/generator/${item.id}/main`)"/>
                        <q-btn v-if="getViewRules(item.type)" dense flat color="secondary" icon="mdi-briefcase-eye"
                               label="просмотр" @click="openManageDialog(item.id, item)"/>
                      </div>
                    </div>
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
        </div>
        <div v-else class="text-h6">
          <span v-if="_.size(listData) > 0">Не найдены дисциплины с текущими фильтрами</span>
          <span v-else>Дисциплины не назначены</span>
        </div>
      </div>
    </template>
  </layout-h-c-f>

</template>

<style scoped lang="scss">
.rpd-container {
  display: grid;
  grid-template-columns: auto repeat(5, 1fr) auto auto;
}

.rpd-row {
  display: contents;

  &.status-0 > div { // "Назначен"
    background: white;
  }
  &.status-1 > div { // "Заполняется"
    background: $light-blue-1;
  }
  &.status-2 > div { // "Отправлен на проверку"
    background: $amber-1;
  }
  &.status-3 > div { // "Утвержден"
    background: $green-1;
  }
  &.status-4 > div { // "Требуются правки"
    background: $red-1;
  }


  $border: solid 1px silver;

  > div {
    padding: 0.5rem;
    border: $border;
    border-right: none;
    border-bottom: none;

    &:last-child {
      border-right: $border;
    }
  }

  &:last-child {
    > div {
      border-bottom: $border;
    }
  }

  &.rpd-row__body {
    //&:hover {
    //  > div {
    //    background: $info !important;
    //  }
    //}
  }

}

</style>

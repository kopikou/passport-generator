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
import {useQuasar} from "quasar";
import {GeneratorListData} from "src/types";
import {useRouter} from "vue-router";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import GeneratorManageDialog from "pages/generator/components/dialogs/GeneratorManageDialog.vue";

const $q = useQuasar()
const router = useRouter()
const listData = ref<GeneratorListData[]>([])

const typeFilter = [
  {label: 'Руководитель программы', value: 'rop'},
  {label: 'Директор', value: 'fac'},
  {label: 'Заведующий кафедры', value: 'zav'},
  {label: 'Преподаватель', value: 'person'},
]

const type = ref($q.localStorage.getItem('surp_typeFilter') ? $q.localStorage.getItem('surp_typeFilter') : ['person'])

const filteredListData = computed(() => {
  return _(listData.value)
    .filter(x => {
      return x.type.some(q => type.value.includes(q));
    })
    .orderBy(x => x.discode, 'asc')
    .groupBy(x => x.abbr)
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

watch(type, () => {
  $q.localStorage.setItem('surp_typeFilter', type.value)
})

onBeforeMount(async () => {
  $q.loading.show()
  await getProgramData()
  $q.loading.hide()
})

</script>

<template>
  <div class="q-pa-lg">
    <div class="text-center text-h6 q-mb-md">Список рабочих программ дисциплин ИРНИТУ</div>
    <div>
      <div>
        <div class="text-center text-subtitle1">Список РПД</div>
        <q-select
          class="q-mb-sm"
          v-model="type"
          :options="typeFilter"
          label="Фильтр"
          option-label="label"
          option-value="value"
          stack-label
          multiple
          use-chips
          map-options
          emit-value
          outlined
        />
        <q-list
          bordered
          separator
        >
          <q-expansion-item
            v-for="items, key in filteredListData"
            :label="key"
          >
            <q-card>
              <q-card-section>
                <div class="rpd-container">
                  <div class="rpd-row rpd-row__header text-weight-bold text-center">
                    <div>Код</div>
                    <div>Дисциплина</div>
                    <div>Составитель</div>
                    <div>Кафедра</div>
                    <div>Статус</div>
                    <div>Управление</div>
                  </div>
                  <div class="rpd-row rpd-row__body text-center" v-for="item, key in items">
<!--                       @click="router.push(`/generator/${item.id}/main`)"-->
                    <div :class="getRowColor(key)">{{ item.discode }}</div>
                    <div :class="getRowColor(key)">{{ item.discpl }}</div>
                    <div :class="getRowColor(key)">{{ item.person }}</div>
                    <div :class="getRowColor(key)">{{ cafDataById[item.kafcode]?.label }}</div>
                    <div :class="getRowColor(key)">{{ item.status_verbose }}</div>
                    <div :class="getRowColor(key)">
                      <q-btn v-if="getEditRules(item.type)" dense flat color="primary" icon="mdi-pencil" label="заполнить" @click="router.push(`/generator/${item.id}/main`)"/>
                      <q-btn v-if="getViewRules(item.type)" dense flat color="secondary" icon="mdi-briefcase-eye" label="просмотр" @click="openManageDialog(item.id, item)"/>
                    </div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-expansion-item>
        </q-list>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.rpd-container {
  display: grid;
  grid-template-columns: auto repeat(3, 1fr) auto auto;
}

.rpd-row {
  display: contents;

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
